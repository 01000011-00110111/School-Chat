"""Handles creations, deletions, and edits of chat rooms"""
import random
from string import ascii_uppercase
from datetime import datetime
from main import dbm
import main


def chat_room_log(message):
    """logs all deletes, creations, and edits done to chat rooms"""
    with open('backend/chat-rooms_log.txt', 'a') as file:
        file.write(message + '\n')


def generate_unique_code(length):
    """Make a room code that doesen't exist yet."""
    rooms = dbm.rooms.distinct('roomid')
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
    room = dbm.rooms.find()
    rooms = []
    for r in room:
        rooms.append({
            'name': r['roomName'],
            'id': r['roomid'],
            'whitelisted': r['whitelisted'],
            'blacklisted': r['blacklisted']
        })
    return rooms


def create_rooms(name, user, username):
    """Someone wants to make a chat room."""
    if len(name) > 10:
        result = ('reason', 1, "create")
        return result
    else:
        result = create_chat_room(username, name, user)
    if result[1] == 0:
        main.get_rooms(user["username"])
        return result
    else:
        return result


def create_chat_room(username, name, userinfo):
    """Make a chat room, register in the db."""
    user = userinfo["username"]
    possible_room = dbm.rooms.find_one({"generatedBy": user})
    generated_at = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    if possible_room is not None and userinfo["SPermission"] != "Debugpass":
        logmessage = f"{username} failed to make a room named {name} at {generated_at} because {username} has made a room before."
        response = ('reason', 2, "create")
    elif name == '':
        logmessage = f"{username} failed to make a room at {generated_at} because the name was empty."
        response = ('reason', 3, "create")
    elif dbm.rooms.find_one({"roomName": name}) is not None:
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
    dbm.rooms.insert_one({
        "roomid":
        code,
        "generatedBy":
        user,
        "generatedAt":
        generated_at,
        "roomName":
        name,
        "canSend":
        'everyone',
        "whitelisted":
        "everyone",
        "blacklisted":
        "empty",
        "locked":
        'false',
        "messages": [
            f"[SYSTEM]: <font color='#ff7f00'><b>{name}</b> created by <b>{username}</b> at {generated_at}.</font>"
        ]
    })


def delete_chat_room(room_name, user):
    """Deletes the chat room the chat room owner or dev selected"""
    rooms = dbm.rooms.find_one({"roomName": room_name})
    madeBy = rooms["generatedBy"]
    username = user["displayName"]
    date_str = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    if madeBy == user["username"]:
        if rooms["roomid"] is ['jN7Ht3giH9EDBvpvnqRB',"ilQvQwgOhm9kNAOrRqbr"]: return ("reason", 3, "delete")
        response = delete_room(username, room_name, date_str)
        logmessage = f"{username} deleted {room_name} at {date_str}"
    elif user["SPermission"] == "Debugpass":
        if rooms["roomid"] is ['jN7Ht3giH9EDBvpvnqRB',"ilQvQwgOhm9kNAOrRqbr"]: return ("reason", 2, "delete")
        response = delete_room(username, room_name, date_str)
        logmessage = f"{username} deleted {room_name} owned by {madeBy} at {date_str}"
    else: 
        logmessage = f"{username} tried to delete {room_name} at {date_str}"
        response = ("reason", 1, "delete")

    if response[1] == 0:
        main.get_rooms(user["username"])

    chat_room_log(logmessage)
    return (response)


def delete_room(username, room_name, date_str):
    """Deletes the chat room off the database"""
    dbm.rooms.find_one_and_delete({"roomName": room_name})
    return ("reason", 0, "delete")


def chat_room_edit(request, room_name, user, users):
    """checks if the user can edit the chat room and calls the different chat room edits the user can run"""
    room = dbm.rooms.find_one({"roomName": room_name})
    username = user["displayName"]
    if request == "whitelist":
        if room["generatedBy"] == user["username"]: return whitelist(room_name, user, users, room, username, False)
        elif user["SPermission"] == "Debugpass": return whitelist(room_name, user, users, room, username, True)
        else: 
            if users not in ['clear','','everyone']: chat_room_log(f"{username} tried to whitelist {users} in chat room {room_name}")
            else: chat_room_log(f"{username} tried to clear the whitelist in chat room {room_name}")
            return ('response', 1, 'edit')
    elif request == "blacklist":
        if room["generatedBy"] == user["username"]: return blacklist(room_name, user, users, room, username, False)
        elif user["SPermission"] == "Debugpass": return blacklist(room_name, user, users, room, username, True)
        else: 
            if users not in ['clear','']: chat_room_log(f"{username} tried to blacklist {users} in chat room {room_name}")
            else: chat_room_log(f"{username} tried to clear the blacklist in chat room {room_name}")
            return ('response', 1, 'edit')
    elif request == "add more stuff later":
        print('what to add')


def whitelist(room_name, user, users, room, username, dev):
    """Whitelist user a dev or the owner picks"""
    if users not in ['clear','','everyone']:
        message = 'users: ' + users
        update_whitelist(room_name, message)
        main.get_rooms(user["username"])
        if dev is True: chat_room_log(f"The dev {username} whitelisted {users} in chat room {room_name}")
        else: chat_room_log(f"The user{username} whitelisted {users} in chat room {room_name}")
        return ('response', 0, 'edit')
    elif users in ['clear','','everyone']: 
        message = 'everyone'
        update_whitelist(room_name, message)
        main.get_rooms(user["username"])
        if dev is True: chat_room_log(f"The dev {username} set the whitelist to everyone in chat room {room_name}")
        else: chat_room_log(f"The user {username} set the whitelist to everyone in chat room {room_name}")
        return ('response', 0, 'edit')


def blacklist(room_name, user, users, room, username, dev):
    """Blacklist user a dev or the owner picks"""
    if users not in ['clear','']:
        message = 'users: ' + users
        update_blacklist(room_name, message)
        main.get_rooms(user["username"])
        if dev is True: chat_room_log(f"The dev {username} blacklisted {users} in chat room {room_name}")
        else: chat_room_log(f"The user{username} blacklisted {users} in chat room {room_name}")
        return ('response', 2, 'edit')
    elif users in ['clear','']: 
        message = 'empty'
        update_blacklist(room_name, message)
        main.get_rooms(user["username"])
        if dev is True: chat_room_log(f"The dev {username} set the blacklist to everyone in chat room {room_name}")
        else: chat_room_log(f"The user {username} set the blacklist to everyone in chat room {room_name}")
        return ('response', 2, 'edit')


def update_whitelist(room_name, message):#combine whitelist and blacklist
    """Adds the whitelisted users to the database"""
    dbm.rooms.update_one({"roomName": room_name},
                     {"$set": {
                         "whitelisted": message
                     }})

def update_blacklist(room_name, message):
    """Adds the blacklisted users to the database"""
    dbm.rooms.update_one({"roomName": room_name},
                 {"$set": {
                     "blacklisted": message
                 }})


def check_roomids(roomid):
    """checks if the room id you have is a real room id"""
    roomid_check = dbm.rooms.find_one({"roomid": roomid})
    if roomid_check is not None:
        return (True)
    else:
        return (False)