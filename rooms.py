import random
from string import ascii_uppercase
from datetime import datetime
from main import dbm


def generate_unique_code(length, username):
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
        rooms.append({'name': r['roomName'], 'id': r['roomid'], 'canSee': r['canSee']})
    return rooms


def create_chat_room(username, name, user):
    """Make a chat room, register in the db."""
    possible_room = dbm.rooms.find_one({"generatedBy": user})
    if possible_room is not None:
        return ('fail', 1)
    elif name == '':
        return ('fail', 2)
    elif dbm.rooms.find_one({"roomName": name}) is not None:
        print("FAILED BOZO")
        return ('fail', 2)
    code = generate_unique_code(5, username)
    generated_at = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
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
        "locked":
        'false',
        "messages": [
            f"[SYSTEM]: <font color='#ff7f00'><b>{name}</b> created by <b>{username}</b> at {generated_at}.</font>"
        ]
    })

    return ('good', 0)

def delete_chat_room(roomid):
    deleted = dbm.rooms.find_one_and_delete({"roomid": roomid})
    # return ('good', 1)