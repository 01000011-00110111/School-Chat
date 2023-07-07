import random
from string import ascii_uppercase
from datetime import datetime


def generate_unique_code(length, username, dbm):
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


def get_chat_rooms(dbm):
    """Return all available rooms."""
    rooms = []
    room = dbm.rooms.find()
    for r in room:
        del r['_id']  # forgot mongodb auto generates this, yep its not needed
        del r['messages']
        del r['generatedAt']
        rooms.append(r)
    return rooms


def create_chat_room(username, dbm, name):
    """Make a chat room, register in the db."""
    possible_room = dbm.rooms.find_one({"generatedBy": username})
    print(possible_room)
    if possible_room is not None:
        return ('fail', 1)
    code = generate_unique_code(5, username, dbm)
    print(code)
    generated_at = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    dbm.rooms.insert_one({
        "roomid": code,
        "generatedBy": username,
        "generatedAt": generated_at,
        "roomName": name,
        "messages": []
    })

    return ('good', 0)

    # put a message saying who created the db, and what time
