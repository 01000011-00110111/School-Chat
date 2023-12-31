"""Handles creations, deletions, and edits of chat rooms.
    Copyright (C) 2023  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
import random
from string import ascii_uppercase
from datetime import datetime
from flask_socketio import emit
import database
#import main
#forgot about bool for a sec

def chat_room_log(message):
    """logs all deletes, creations, and edits done to chat rooms"""
    with open('backend/chat-rooms_log.txt', 'a', encoding="utf8") as file:
        file.write(f'{message}\n')


def generate_unique_code(length):
    """Make a room code that doesen't exist yet."""
    rooms = database.distinct_roomids()
    # ^^ I have no idea if this will work well or not (it does!)
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)

        if code not in rooms:
            # the code does not already exist if this is true
            break

    return code


def get_chat_rooms():
    """Return all available rooms."""
    return database.get_rooms()

def create_rooms(name, user, username):
    """Someone wants to make a chat room."""
    if len(name) > 10:
        result = ('reason', 1, "create")
        return result

    result = create_chat_room(username, name, user)
    if result[1] == 0:
        emit("force_room_update", broadcast=True)

    return result


def create_chat_room(username, name, userinfo):
    """Make a chat room, register in the db."""
    user = userinfo["username"]
    possible_room = database.find_room({"generatedBy": user}, 'id')
    generated_at = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    if possible_room is not None and userinfo["SPermission"] != "Debugpass":
        logmessage = f"{username} failed to make a room named {name} at {generated_at} because {username} has made a room before."
        response = ('reason', 2, "create")
    elif name == '':
        logmessage = f"{username} failed to make a room at {generated_at} because the name was empty."
        response = ('reason', 3, "create")
    elif database.find_room({'roomName': name}, 'id') is not None:
        logmessage = f"{username} failed to make a room named {name} at {generated_at} because the name was taken."
        response = ('reason', 4, "create")
    else:
        code = generate_unique_code(5)
        insert_room(code, user, generated_at, name, username)
        logmessage = f"{username} made a room named {name} at {generated_at}"
        response = ('reason', 0, "create")
    chat_room_log(logmessage)
    return response


def insert_room(code, user, generated_at, name, username):
    """Create a room in the db."""
    database.add_account(code, username, generated_at, name,)


def delete_chat_room(room_name, user):
    """Deletes the chat room the chat room owner or dev selected"""
    rooms = database.find_room({"roomName": room_name}, 'id')
    made_by = rooms["generatedBy"]
    username = user["displayName"]
    date_str = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    if made_by == user["username"]:
        if len(rooms["roomid"]) == 20:
            return ("reason", 3, "delete")
        response = delete_room(rooms["roomid"])
        logmessage = f"{username} deleted {room_name} at {date_str}"
    elif user["SPermission"] == "Debugpass":
        if len(rooms["roomid"]) == 20:
            return ("reason", 2, "delete")
        response = delete_room(rooms["roomid"])
        logmessage = f"{username} deleted {room_name} owned by {made_by} at {date_str}"
    else:
        logmessage = f"{username} tried to delete {room_name} at {date_str}"
        response = ("reason", 1, "delete")

    if response[1] == 0:
        emit("force_room_update", broadcast=True)

    chat_room_log(logmessage)
    return response


def delete_room(roomid):
    """Deletes the chat room off the database"""
    database.delete_room({"roomid": roomid})
    return ("reason", 0, "delete")


def check_roomids(roomid):
    """checks if the roomid you have is a real roomid"""
    roomid_check = database.find_room({"roomid": roomid}, 'id')
    if roomid_check is not None:
        return True
    else:
        return False
