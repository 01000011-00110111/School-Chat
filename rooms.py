"""Handles creations, deletions, and edits of chat rooms.
    Copyright (C) 2023  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
import random
from string import ascii_uppercase
from datetime import datetime
from flask_socketio import emit
from main import dbm
#import main


def chat_room_log(message):
    """logs all deletes, creations, and edits done to chat rooms"""
    with open('backend/chat-rooms_log.txt', 'a', encoding="utf8") as file:
        file.write(f'{message}\n')


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
            'generatedBy': r['generatedBy'],
            'mods': r['mods'],
            'whitelisted': r['whitelisted'],
            'blacklisted': r['blacklisted']
        })
    return rooms


def get_chat_room(roomid):
    """grabs a chat room"""
    return dbm.rooms.find_one({'roomid': roomid})


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
    """Create a room in the db."""
    dbm.rooms.insert_one({
        "roomid":
        code,
        "generatedBy":
        username,
        "mods":
        '',
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
    made_by = rooms["generatedBy"]
    username = user["displayName"]
    date_str = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    if made_by == user["username"]:
        if len(rooms["roomid"]) == 20:
            return ("reason", 3, "delete")
        response = delete_room(room_name)
        logmessage = f"{username} deleted {room_name} at {date_str}"
    elif user["SPermission"] == "Debugpass":
        if len(rooms["roomid"]) == 20:
            return ("reason", 2, "delete")
        response = delete_room(room_name)
        logmessage = f"{username} deleted {room_name} owned by {made_by} at {date_str}"
    else:
        logmessage = f"{username} tried to delete {room_name} at {date_str}"
        response = ("reason", 1, "delete")

    if response[1] == 0:
        emit("force_room_update", broadcast=True)

    chat_room_log(logmessage)
    return response


def delete_room(room_name):
    """Deletes the chat room off the database"""
    dbm.rooms.find_one_and_delete({"roomName": room_name})
    return ("reason", 0, "delete")


def chat_room_edit(request, function, room_name, user, users):
    """checks if the user can edit the chat room and calls the different chat room edits the user can run"""
    room = dbm.rooms.find_one({"roomName": room_name})
    username = user["displayName"]
    if request == "whitelist":
        if room["generatedBy"] == user["username"]:
            return whitelist(room_name, function, user, users, room, username,
                             False)
        if user["SPermission"] == "Debugpass":
            return whitelist(room_name, function, user, users, room, username,
                             True)
        else:
            if users not in ['clear', '', 'everyone']:
                chat_room_log(
                    f"{username} tried to whitelist {users} in chat room {room_name}"
                )
            else:
                chat_room_log(
                    f"{username} tried to clear the whitelist in chat room {room_name}"
                )
            return ('response', 1, 'edit')
    elif request == "blacklist":
        if room["generatedBy"] == user["username"]:
            return blacklist(room_name, function, user, users, room, username,
                             False)
        if user["SPermission"] == "Debugpass":
            return blacklist(room_name, function, user, users, room, username,
                             True)
        else:
            if users not in ['clear', '']:
                chat_room_log(
                    f"{username} tried to blacklist {users} in chat room {room_name}"
                )
            else:
                chat_room_log(
                    f"{username} tried to clear the blacklist in chat room {room_name}"
                )
            return ('response', 1, 'edit')
    elif request == 'permote spell fix later':
        print('grant users mod perms in the chat room')
    elif request == "add more stuff later":
        print('what to add')


def whitelist(room_name, set_type, user, users, room, username, dev):
    """Whitelist user a dev or the owner picks"""
    pre_user_list = dbm.rooms.find_one({'roomName': room_name})
    users_to_add = users.split(',')
    blacklisted_users = pre_user_list["blacklisted"].replace("users:", "").split(',')
    whitelisted_users = pre_user_list["whitelisted"].replace("users:", "").split(',')
    add_users = []
    new_users = []

    for user in users_to_add:
        if user not in ['clear','everyone'] and set_type == 'add':
            if user in blacklisted_users:
                if dev is True:
                    log = f"The dev {username} tried to whitelist the users: {users} but one or more where already in the whitelist. In chat room {room_name}"
                else:
                    log = f"The user {username} tried to whitelist the users: {users} but one or more where already in the whitelist. In chat room {room_name}"
                chat_room_log(log)
                return (4, 'W')
            if user not in whitelisted_users:
                new_users.append(user)
                response = (3, 'W')
            else:
                if dev is True:
                    log = f"The dev {username} tried to whitelist the users: {users} but one or more where already in the blacklist. In chat room {room_name}"
                else:
                    log = f"The user {username} tried to whitelist the users: {users} but one or more where already in the blacklist. In chat room {room_name}"
                chat_room_log(log)
                return (5, 'W')
        elif user not in ['clear','everyone'] and set_type == 'set':
            new_users.append(user)
            add_users = f"users:{','.join(new_users)}"
            response = (0, 'W')
        elif (user in ['clear','everyone'] and user not in ['modonly','devonly']
              and set_type == 'set'):
            new_users.append('everyone')
            add_users = ','.join(new_users)
            response = (1, 'W')
        elif user not in ['modonly','devonly'] and set_type == 'set':
            new_users.append(user)
            add_users = ','.join(new_users)
            response = (2, 'W')  
    if set_type == 'add':
        add_users = f"users:{','.join(whitelisted_users)},{''.join(new_users)}"

    #turn the addusers list into a string
    add_users.split(',') #split the list into a string
    add_users = ','.join(add_users) #join the list into a string
    update_blacklist(room_name, add_users)
    update_whitelist(room_name, add_users)
    emit("force_room_update", broadcast=True)
    if dev is True:
        if set_type == 'add':
            log = f"The dev {username} added {users} to the whitelist in chat room {room_name}"
        else:
            log = f"The dev {username} set the whitelist to everyone in chat room {room_name}"
    else:
        if set_type == 'add':
            log = f"The user {username} added {users} to the whitelist in chat room {room_name}"
        else:
            log =  f"The user {username} set the whitelist to everyone in chat room {room_name}"
    chat_room_log(log)
    return response


def blacklist(room_name, set_type, user, users, room, username, dev):
    """Blacklist user a dev or the owner picks"""
    pre_user_list = dbm.rooms.find_one({'roomName': room_name})
    users_to_add = users.split(',')
    blacklisted_users = pre_user_list["blacklisted"].replace("users:", "").split(',')
    whitelisted_users = pre_user_list["whitelisted"].replace("users:", "").split(',')
    add_users = []
    new_users = []
    
    for user in users_to_add:
        
        if user not in ['clear','everyone'] and set_type == 'add':
            if user in whitelisted_users:
                if dev is True:
                    log = f"The dev {username} tried to blacklist the users: {users} but one or more where already in the whitelist. In chat room {room_name}"
                else:
                    log = f"The user {username} tried to blacklist the users: {users} but one or more where already in the whitelist. In chat room {room_name}"
                chat_room_log(log)
                return (3, 'B')
            if user not in blacklisted_users:
                new_users.append(user)
                response = (2, 'B')
            else:
                if dev is True:
                    log = f"The dev {username} tried to blacklist the users: {users} but one or more where already in the blacklist. In chat room {room_name}"
                else:
                    log = f"The user {username} tried to blacklist the users: {users} but one or more where already in the blacklist. In chat room {room_name}"
                chat_room_log(log)
                return (4, 'B')
        elif user not in ['clear','everyone'] and set_type == 'set':
            if user == pre_user_list['generatedBy'] and user not in blacklisted_users:
                if dev is True:
                    log = f"The dev {username} tried to blacklist the Owner. In chat room {room_name}"
                else:
                    log = f"The user {username} tried to blacklist the Owner. In chat room {room_name}"
                chat_room_log(log)
                return (5, 'B')
            new_users.append(user)
            add_users = ','.join(new_users)
            response = (0, 'B')
        elif user in ['clear','empty'] and set_type == 'set':
            new_users.append('empty')
            add_users = ','.join(new_users)
            response = (1, 'B')

    if set_type == 'add':
        add_users = f"users:{','.join(blacklisted_users)},{''.join(new_users)}"

    #turn the addusers list into a string
    add_users.split(',') #split the list into a string
    add_users = ','.join(add_users) #join the list into a string
    update_blacklist(room_name, add_users)
    update_blacklist(room_name, add_users)
    emit("force_room_update", broadcast=True)
    if dev is True:
        if set_type == 'add':
            log = f"The dev {username} added {users} to the blacklist in chat room {room_name}"
        else:
            log = f"The dev {username} set the blacklist to everyone in chat room {room_name}"
    else:
        if set_type == 'add':
            log = f"The user {username} added {users} to the blacklist in chat room {room_name}"
        else:
            log =  f"The user {username} set the blacklist to everyone in chat room {room_name}"
    chat_room_log(log)
    return response


def update_whitelist(room_name, message):  #combine whitelist and blacklist
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
    """checks if the roomid you have is a real roomid"""
    roomid_check = dbm.rooms.find_one({"roomid": roomid})
    if roomid_check is not None:
        return True
    else:
        return False
