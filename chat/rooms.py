"""chat/rooms.py: Backend functions for message handling.
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in app.py or the LICENSE file.
"""
# from datetime import datetime
from chat.chat import Chat
# import chat.database as chatdb
from user.user import User
from user.login import check_suuid
from socketio_confg import sio

@sio.on("join_room")
async def join_room(sid, data):
    """
    This function is called when a client joins a room.
    """
    suuid = data["suuid"]
    roomid = data["roomid"]
    check = check_suuid(suuid)
    if check:
        if roomid in Chat.chats:
            chat = Chat.get_chat(roomid)
        else:
            chat = Chat.add_chat(roomid)

        user = User.Users[suuid]

        for _, old_chat in Chat.chats.items():
            if user.suuid in old_chat.sids:
                old_chat.sids.pop(user.suuid)
                break

        if user.suuid not in chat.sids:
            chat.sids[user.suuid] = sid

        await sio.emit("load_chat",
                    {"messages": chat.messages, "roomid": chat.vid, "name": chat.name},
                    to=sid)
    else:
        await sio.emit("send_to_login", to=sid)
