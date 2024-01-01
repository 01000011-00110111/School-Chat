from flask_socketio import SocketIO, emit

import database

def get_messages(sender, receiver):
    """gets the chats with 2 users."""
    chat = database.find_private_messages([sender, receiver])
    if chat is None:
        database.create_private_chat([sender, receiver])

    return chat
    