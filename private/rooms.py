"""chat/rooms.py: Backend functions for message handling.
    Copyright (C) 2023-2025  cserver45, cseven, CastyiGlitchxz
    License info can be viewed in app.py or the LICENSE file.
"""
# from datetime import datetime
from private.private import Private
# import chat.database as chatdb
from user.user import User
from user.login import check_suuid
from socketio_confg import sio


@sio.on("leave_room_private")

def format_userlist(uuid1, uuid2):
    """Formats the userlist value."""
    return sorted([uuid1, uuid2], key=lambda x: (not x.isdigit(), x.lower()))

@sio.on("join_room_private")
async def join_room(sid, data):
    """
    This function is called when a client joins a room.
    """
    suuid = data["suuid"]
    display_name = data["display_name"]
    check = check_suuid(suuid)
    if check:
        user = User.Users[suuid]
        uuid = user.uuid
        uuid2 = User.usernames(display_name)
        pmid = Private.chats_userlist[tuple(format_userlist(uuid, uuid2))]

        if pmid in Private.chats:
            chat = Private.get_chat(pmid)
        else:
            chat = Private.add_chat(pmid)

        for _, old_chat in Private.chats.items():
            if user.suuid in old_chat.sids:
                old_chat.sids.pop(user.suuid)
                break

        if user.suuid not in chat.sids:
            chat.sids[user.suuid] = sid
            # chat.sids.append(sid)

        await sio.emit("load_chat",
                    {"messages": chat.messages, "pmid": chat.pmid, "name": chat.name},
                    to=sid)
    else:
        await sio.emit("send_to_login", to=sid)
