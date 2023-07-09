import random
from string import ascii_uppercase
from datetime import datetime
from main import dbm
from flask_socketio import emit


def chat_room_log(message):
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


def get_chat_rooms(room):
    """Return all available rooms."""
    rooms = []
    for r in room:
        rooms.append({
            'name': r['roomName'],
            'id': r['roomid'],
            'canSee': r['canSee']
        })
    return rooms


def create_rooms(name, user, username):
    """Someone wants to make a chat room."""
    room = dbm.rooms.find()
    if len(name) > 10:
        result = ('reason', 1, "create")
        return result
    else:
        result = create_chat_room(username, name, user)
        # emit('chatCreateResult', result)# what is this
        return result
    if result[1] == 0:
        all_rooms = get_chat_rooms(room)
        emit('roomsList', all_rooms, namespace='/', broadcast=True)
        return result
    else:
        return result


def create_chat_room(username, name, userinfo):
    """Make a chat room, register in the db."""
    user = userinfo["username"]
    possible_room = dbm.rooms.find_one({"generatedBy": user})
    generated_at = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    if possible_room is not None:
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
            "canSee":
            "everyone",
            "blacklisted":
            "",
            "locked":
            'false',
            "messages": [
                f"[SYSTEM]: <font color='#ff7f00'><b>{name}</b> created by <b>{username}</b> at {generated_at}.</font>"
            ]
        })
        logmessage = f"{username} made a room named {name} at {generated_at}"
        response = ('reason', 0, "create")
    chat_room_log(logmessage)
    return response


def delete_chat_room(room_name, user):
    rooms = dbm.rooms.find_one({"roomName": room_name})
    date_str = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    username = user["displayName"]
    if rooms["generatedBy"] == user["username"]:
        deleted = dbm.rooms.find_one_and_delete({"roomName": room_name})
        logmessage = f"{username} deleted {room_name} at {date_str}"
        response = ("reason", 0, "delete")
    else:
        logmessage = f"{username} tried to delete {room_name} at {date_str}"
        response = ("reason", 1, "delete")

    if response[1] == 0:
        room = dbm.rooms.find()
        all_rooms = get_chat_rooms(room)
        emit('roomsList', all_rooms, namespace='/', broadcast=True)

    chat_room_log(logmessage)
    return (response)


def chat_room_edit(request, room_name, user, users): # my git commits for some reason dont go to 
    room = dbm.rooms.find_one({"roomName": room_name}) # can you push to git real quick so pylint can rerun sure why not
    if request == "access":
        if room["generatedBy"] == user["username"]:
            dbm.rooms.update_one({"roomName": room_name},
                                 {"$set": {
                                     "canSee": users
                                 }})
    elif request == "block":
        dbm.rooms.update_one({"roomName": room_name},
                     {"$set": {
                         "blacklisted": users
                     }})
    elif request == "info":
        print("i can't do it lol")