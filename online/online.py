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
socketids = {}

# @sio.event
# async def connect(sid, environ):
#     """Handle connection."""
#     namespace = environ.get("PATH_INFO", "/")

#     if namespace != "/":@sio.on("chatpage")
# async def connect(sid):@sio.on("chatpage")
@sio.on("chatpage")
async def connect(sid):
    """Handle startup system."""
    await sio.emit("online", {"update": "full", "data": userlist}, to=sid)
    await sio.emit("room_list", {"rooms": Chat.all_chats}, to=sid)

@sio.event
async def disconnect(sid):
    """Handle disconnections."""
    print(f"Client disconnected (SID: {sid})")


@sio.on("heartbeat")
async def heartbeat(sid):
    """Handle heartbeat events."""
    await sio.emit("heartbeat", to=sid)


@sio.on("online")
async def online(sid, suuid, status):
    """Handle online events."""
    print("online", suuid, status)
    uuid = User.Users[suuid].uuid
    update({"status": status}, uuid)
    # socketids[uuid] = sid

    await sio.emit("online", {"update": 'partial', "data": userlist[uuid]}, to=sid)


def update(data, uuid):
    """Update the online status of all users."""
    for key, value in data.items():
        if key == 'status' and userlist[uuid]['status'] == 'offline-locked':
            continue
        userlist[uuid][key] = value
