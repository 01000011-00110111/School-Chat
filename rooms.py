"""rooms.py: Bakcend management of chat rooms.
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
import random
from datetime import datetime
from string import ascii_uppercase

from flask_socketio import emit

import database
from chat import Chat


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

def create_chat_room(name, username, _userinfo):
    """Create a chat room and register it in the database."""
    generated_at = datetime().strftime("%Y-%m-%dT%H:%M:%S")

    if not name or database.find_room({'roomName': name}, 'vid'):
        log = f"Failed: Invalid Room Name ({username} room creation) {generated_at}"
        response = (3, "chat") if not name else (4, "chat")
    else:
        code = generate_unique_code(5)
        database.add_rooms(code, username, generated_at, name)
        Chat.create_or_get_chat(code)
        log = f"{username} made a room named {name} at {generated_at}"
        response = (0, "chat")
        emit("force_room_update", broadcast=True)

    chat_room_log(log)
    return response

# ADD BACK DELETING CHAT ROOMS

def check_roomids(roomid):
    """Check if the room ID exists."""
    return bool(database.find_room({"roomid": roomid}, 'vid'))
