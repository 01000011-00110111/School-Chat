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
import asyncio
from datetime import datetime
# from logs.logs import log_user_connected, log_user_disconnected

userlist = get_online_data()
# print(userlist)
socketids = {}

@sio.on("chatpage")
async def connect(sid, data):
    """Handle startup system."""
    suuid = data.get("suuid")
    user = User.Users.get(suuid)

    if not user:
        print(f"❌ Invalid or expired user SUUID: {suuid}")
        await sio.emit("send_to_login", to=sid)
        return
    
    uuid = user.uuid
    user_data = {
        "displayName": user.display_name,
        "role": user.role,
        "profile": user.profile,
        "theme": user.theme
    }
    # print(f"Client connected (SID: {sid, uuid})")
    update({"status": 'active'}, uuid)
    # log_user_connected(uuid)
    await sio.emit("online", {"update": "full", "data": userlist}, to=sid)
    await sio.emit("user_data", user_data, to=sid)
    await sio.emit("room_list", {"rooms": Chat.all_chats}, to=sid)

@sio.event
async def disconnect(sid):
    """Handle disconnection of a client."""
    for suuid, user in User.Users.items():
        if user.active:
            user.active = False
            update({"status": "offline"}, user.uuid)
            # log_user_disconnected(user.uuid)
            await sio.emit("online", {"update": "partial", "data": userlist[user.uuid]})
            # print(f"User {suuid} disconnected, status updated to offline.")

heartbeat_flags = {}

async def heartbeat_loop():
    """Periodically check if users are online."""
    print("✅ heartbeat_loop task started")
    global heartbeat_flags
    while True:
        # print("💓 Heartbeat loop called")
        heartbeat_flags = {}

        for uuid, status in userlist.items():
            if status["status"] in ["active", "idle"]:
                heartbeat_flags[uuid] = False  # False means not responded yet

        await sio.emit("heartbeat")  # Broadcast to all

        await asyncio.sleep(5)

        for uuid, responded in heartbeat_flags.items():
            if not responded:
                print(f"❌ User {uuid} did not respond to heartbeat, marking as offline.")
                update({"status": "offline"}, uuid)
                # log_user_disconnected(uuid)
                await sio.emit("online", {"update": "partial", "data": userlist[uuid]})

@sio.on("beat")
async def beat(sid, data):
    """Handle heartbeat responses from clients."""
    suuid = data.get("suuid")
    user = User.Users.get(suuid)

    if user:
        update({"status": data.get("status", "active")}, user.uuid)

        if user.uuid in heartbeat_flags:
            heartbeat_flags[user.uuid] = True

        await sio.emit("online", {"update": "full", "data": userlist}, to=sid)
    else:
        await sio.emit("send_to_login", to=sid)

# @sio.on("online")
async def online(_, data):
    """Handle online events."""
    suuid = data['suuid']
    status = data['status']
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
        uuid = User.Users[suuid].uuid
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

# def update(data, uuid):
#     """Update the online status of a user."""
#     if uuid not in userlist:
#         return
#     update_all(data, uuid)
#     sio.emit("online", {"update": "partial", "data": userlist[uuid]}, to=socketids.get(uuid, None))

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



