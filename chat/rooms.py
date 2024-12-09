"""rooms.py: Backend functions for message handling.
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in app.py or the LICENSE file.
"""
from datetime import datetime
from chat import Chat
import database
from socketio_confg import sio

@sio.on("join_room")
async def join_room(sid, roomid):
    if roomid in Chat.chats:
        chat = Chat.get_chat("ilQvQwgOhm9kNAOrRqbr")
    else:
        chat = Chat.add_chat("ilQvQwgOhm9kNAOrRqbr")

    await sio.emit("load_chat", {"messages": chat.messages, "roomid": chat.vid, "name": chat.name})
    # await sio.emit("load_chat", {"messages": Chat.get_chat(data["roomid"]).messages, "roomid": data["roomid"]})
