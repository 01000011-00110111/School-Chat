"""private.py - Prive Messaging"""
from flask_socketio import SocketIO, emit
import random
from string import ascii_uppercase
import database

def get_messages(sender, receiver):
    """gets the chats with 2 users."""
    userlist = sorted([sender, receiver], key=lambda x: (not x[0].isdigit(), x[0].lower()))
    chat = database.find_private_messages(userlist, sender)
    # database.update_private_messages(userlist, chat['pmid'])
    # print(chat)

    if chat is None:
        code = generate_unique_code(12)
        database.create_private_chat(userlist, code)
        chat = database.find_private_messages(userlist, sender)

    return chat

def generate_unique_code(length):
    """Make a room code that doesen't exist yet."""
    rooms = database.distinct_pmid()
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)

        if code not in rooms:
            break

    return code
    