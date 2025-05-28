"""online/online.py: Backend functions for message handling.
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in app.py or the LICENSE file.
"""
# import asyncio
from socketio_confg import sio
# from user import user, database
from user.database import get_online_data
from user.user import User
from chat.rooms import Chat

userlist = get_online_data()
# print(userlist)
socketids = {}

@sio.on("chatpage")
async def connect(sid, data):
    """Handle startup system."""
    user = User.Users[data["suuid"]]
    uuid = user.uuid
    user_data = {
        "displayName": user.display_name,
        "role": user.role,
        "profile": user.profile,
        "theme": user.theme
    }
    # print(f"Client connected (SID: {sid, uuid})")
    update({"status": 'active'}, uuid)
    await sio.emit("online", {"update": "full", "data": userlist}, to=sid)
    await sio.emit("user_data", user_data, to=sid)
    await sio.emit("room_list", {"rooms": Chat.all_chats}, to=sid)

@sio.event
async def disconnect(sid):
    """Handle disconnections."""
    # print(f"Client disconnected (SID: {sid})")


@sio.on("heartbeat")
async def handle_heartbeat(sid, _, roomid, suuid):
    """Handle heartbeat from the client."""
    if suuid is not None:
        # User.Users[suuid]['status'] = status
        # await sio.emit("online", {"update": "partial", "data": User.Users[suuid]}, to=sid)
        if roomid is not None:
            if roomid in Chat.all_chats:
                chat = Chat.all_chats[roomid]
                if sid not in chat.sids:
                    chat.sids.append(sid)
        # await sio.emit("online", {"update": "full", "data": User.Users}, to=sid)


@sio.on("online")
async def online(sid, suuid, status):
    """Handle online events."""
    # print("online", suuid, status)
    uuid = User.Users[suuid].uuid
    update({"status": status}, uuid)
    # socketids[uuid] = sid

    await sio.emit("online", {"update": 'partial', "data": userlist[uuid]})


@sio.on("update")
async def handle_update(sid, data):
    """Handle update events."""
    # print("update", data)
    suuid = data['suuid']
    if suuid in User.Users:
        uuid = User.Users[suuid]
        update(data, uuid)
        await sio.emit("online", {"update": 'partial', "data": userlist[uuid]})
    else:
        await sio.emit("send_to_login", to=sid)


def update(data, uuid):
    """Update the online status of all users."""
    for key, value in data.items():
        if key == 'status' and userlist[uuid]['status'] == 'offline-locked':
            continue
        userlist[uuid][key] = value

# def handle_forced_disconnect(userid, disconnect_callback):
#     """Mark the user as offline if no heartbeat is received in time."""
#     if userid in user_connections:
#         for socketid in list(user_connections[userid]):
#             disconnect_callback(socketid, userid)
#         del user_connections[userid]

#     try:
#         try:
#             u = User.get_user_by_id(userid)
#             if u and u.status != "offline-locked":
#                 u.status = "offline"
#             database.set_offline(userid)
#             update_userlist(None, {"status": "offline"}, userid)
#         except TypeError as e:
#             print(f"Error in forced disconnect: {e}")
#     except RuntimeError as e:
#         print(f"Runtime error in forced disconnect: {e}")
