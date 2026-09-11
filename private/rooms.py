"""chat/rooms.py: Backend functions for message handling.
    Copyright (C) 2023-2025  cserver45, cseven, CastyiGlitchxz
    License info can be viewed in app.py or the LICENSE file.
"""
# from datetime import datetime
from private.private import Private
from chat.chat import Chat
# import chat.database as chatdb
from user.user import User
from user.login import check_suuid
from socketio_confg import sio

@sio.on("join_room_private")
async def join_room(sid, data):
    """
    This function is called when a client joins a room.
    """
    chat = None
    suuid = data["suuid"]
    display_name = data["other_user"]
    check = check_suuid(suuid)

    if check:
        user = User.Users[suuid]
        other_uuid = User.usernames[display_name]
        userlist = tuple(sorted([user.uuid, other_uuid]))
        pmid = Private.check_created(userlist)

        if not pmid:
            if userlist[0] != userlist[1]:
                chat = Private.create_chat(userlist)
        else:
            chat = Private.add_chat(pmid)

        if chat is not None:
            for chat_dict in (Chat.chats, Private.chats):
                for _, old_chat in chat_dict.items():
                    if user.suuid in old_chat.sids:
                        old_chat.sids.pop(user.suuid)
                        break

            if user.suuid not in chat.sids:
                chat.sids[user.suuid] = sid

                await sio.emit("load_chat",
                [{"messages": chat.messages, "roomid": chat.pmid, "name": "Private Chat"}, True],
                to=sid)
    else:
        await sio.emit("send_to_login", to=sid)
