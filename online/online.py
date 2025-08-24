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
# from datetime import datetime
# from logs.logs import log_user_connected, log_user_disconnected

userlist = get_online_data()
socketids = {}


async def user_list():
    """Return a secure user list."""
    securelist = {
        user["displayName"]: user.copy()
        for user in userlist.values()
    }
    return securelist

async def get_user(uuid):
    """Return a secure version of user data for a given UUID."""
    if uuid in userlist:
        user_copy = userlist[uuid].copy()
        return {user_copy["displayName"]: user_copy}

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
    if user.status != "offline-lockced":
         update({"status": 'active'}, uuid)
    securelist = await user_list()
    await sio.emit("online", {"update": "full", "data": securelist}, to=sid)
    await sio.emit("user_data", user_data, to=sid)
    await sio.emit("room_list", {"rooms": Chat.get_all_chats(user.perm)}, to=sid)

@sio.on("refresh")
async def refresh_list(sid, suuid):
    user = User.Users.get(suuid)
    if not user:
        print(f"❌ Invalid or expired user SUUID: {suuid}")
        await sio.emit("send_to_login", to=sid)
        return
    securelist = await user_list()
    await sio.emit("online", {"update": "full", "data": securelist}, to=sid)

@sio.event
async def disconnect(sid):
    """Handle disconnection of a client."""
    for suuid, user in User.Users.items():
        if user.active:
            user.active = False
            update({"status": "offline"}, user.uuid)
            # log_user_disconnected(user.uuid)
            securelist = await get_user(user.uuid)
            await sio.emit("online", {"update": "partial", "data": securelist})
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
                securelist = await get_user(uuid)
                await sio.emit("online", {"update": "partial", "data": securelist})

@sio.on("beat")
async def beat(sid, data):
    """Handle heartbeat responses from clients."""
    suuid = data.get("suuid")
    user = User.Users.get(suuid)

    if user:
        update({"status": data.get("status", "active")}, user.uuid)

        if user.uuid in heartbeat_flags:
            heartbeat_flags[user.uuid] = True
            securelist = await user_list()
            await sio.emit("online", {"update": "full", "data": securelist}, to=sid)
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
    securelist = await user_list()
    await sio.emit("online", {"update": 'partial', "data": securelist})



@sio.on("update")
async def handle_update(sid, data):
    """Handle update events."""
    suuid = data['suuid']
    del data['suuid']
    if suuid in User.Users:
        uuid = User.Users[suuid].uuid
        update(data, uuid)
        securelist = await get_user(uuid)
        await sio.emit("online", {"update": 'partial', "data": securelist})
    else:
        await sio.emit("send_to_login", to=sid)


def update(data, uuid):
    """Update the online status of all users."""
    for key, value in data.items():
        if key == 'status' and userlist[uuid]['status'] == 'offline-locked':
            continue
        userlist[uuid][key] = value
