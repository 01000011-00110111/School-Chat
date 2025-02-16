"""chat/message.py: Backend functions for message handling.
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in app.py or the LICENSE file.
"""
from datetime import datetime
from chat.chat import Chat
from chat.filtering import run_filter_chat
from socketio_confg import sio


@sio.on("message")
async def client_message(_, data):
    """
    This function is called when a client sends a message to the server.
    """
    message = run_filter_chat(data["user"], data["room"], data["message"], data["roomid"], data["user"]["uuid"])
    print(message)
    await Chat.get_chat(data["roomid"]).send_message(message)
    # await sio.emit("message", {"message": response})
