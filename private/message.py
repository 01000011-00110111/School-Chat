"""private/message.py: Backend functions for message handling.
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in app.py or the LICENSE file.
"""
from datetime import datetime
from private.private import Private
from socketio_confg import sio


@sio.on("message_private")
async def client_message(_, data):
    """
    This function is called when a client sends a message to the server.
    """
    # print(f"Message from client {sid}: {data}")
    profile = "<img class='user_profile_picture' src='/icons/favicon.ico'></img>"
    user_string = "<p style='color: #ff7f00;'>[SYSTEM]</p>"
    message_string = f"<p style='color: #ffffff;'>{data['message']}</p>"
    role_string = "<p style='background:\
#ff7f00; color: #ffffff;' class='badge'>System</p>"
    date_str = datetime.now().strftime("%a %I:%M %p ")
    message = {
        'profile': profile,
        'user': user_string,
        'message': message_string,
        'badges': [role_string, None],
        'date': date_str
    }
    await Private.get_chat(data["pmid"]).send_message(message)
    # await sio.emit("message", {"message": response})
