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

def create_chat_room(name, username, userinfo):
    """Create a chat room and register it in the database."""
    generated_at = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    
    if not name or database.find_room({'roomName': name}, 'id'):
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

"""
def delete_chat_room(room_name, user):
    Delete the chat room selected by the owner or admin
    rooms = database.find_room({"roomName": room_name}, 'id')
    made_by = rooms.get("generatedBy")
    username = user["displayName"]
    date_str = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    
    if made_by == user["username"] or "Debugpass" in user["SPermission"]:
        if len(rooms.get("roomid", "")) == 20:
            return ("reason", 3, "delete")
        response = delete_room(rooms.get("roomid", ""))
        logmessage = f"{username} deleted {room_name} at {date_str}" if made_by == user["username"] \
                     else f"{username} deleted {room_name} owned by {made_by} at {date_str}"
    else:
        logmessage = f"{username} tried to delete {room_name} at {date_str}"
        response = ("reason", 1, "delete")

    if response[1] == 0:
        emit("force_room_update", broadcast=True)

    chat_room_log(logmessage)
    return response

def delete_room(roomid):
    Delete the chat room from the database
    database.delete_room({"roomid": roomid})
    return ("reason", 0, "delete")
"""
def check_roomids(roomid):
    """Check if the room ID exists."""
    return bool(database.find_room({"roomid": roomid}, 'id'))
