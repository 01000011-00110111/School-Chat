"""rooms.py: Bakcend management of chat rooms.
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
import random
from datetime import datetime
from string import ascii_uppercase

from flask_socketio import emit

import database
# from chat import Chat


def chat_room_log(message):
    """Logs all deletes, creations, and edits done to chat rooms."""
    with open('backend/chat-rooms_log.txt', 'a', encoding="utf8") as file:
        file.write(f'{message}\n')

def generate_unique_code(length):
    """Generate a unique room code."""
    rooms = database.distinct_roomids()
    while True:
        code = ''.join(random.choices(ascii_uppercase, k=length))
        if code not in rooms:
            return code

def create_chat_room(name, message, user):
    """Create a chat room and register it in the database."""
    generated_at = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    code = generate_unique_code(5)
    database.add_rooms(code, user.username, user.display_name, generated_at, name, message)
    emit("force_room_update", namespace='/chat', broadcast=True)

    chat_room_log(f"{user.username} made a room named {name} at {generated_at}")
    return (0, "chat")

# ADD BACK DELETING CHAT ROOMS

def check_roomids(roomid):
    """Check if the room ID exists."""
    return bool(database.find_room({"roomid": roomid}, 'vid'))
