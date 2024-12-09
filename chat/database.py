"""chat/database.py: Backend functions for communicating with MongoDB.
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in app.py or the LICENSE file.
"""

import configparser

# import hashlib
import secrets
from datetime import datetime

import pymongo

config = configparser.ConfigParser()
config.read("core/config/keys.conf")
mongo_pass = config["mongodb"]["passwd"]

if config['backend']['ENV'] == 'development': #this check is temp.
    #pylint: disable=E0401
    import certifi
    client = pymongo.MongoClient(mongo_pass, tls=True, tlsCAFile=certifi.where())
else:
    client = pymongo.MongoClient(mongo_pass)


# accounts/user data
# Accounts = client.Accounts
# Permission = client.Accounts.Permission
# Customization = client.Accounts.Customization
# ID = client.Accounts.Accounts

# chat room data
Rooms = client.Rooms.Rooms
Access = client.Rooms.Permission
Messages = client.Rooms.Messages
Private = client.Rooms.Private


def get_room(roomid):
    """Returns all available permission data in that room."""
    return Rooms.find_one({"roomid": roomid})

def get_rooms():
    """Returns all available permission data in that room."""
    return Rooms.find()

def get_room_data(roomid):
    """Returns all available permission data in that room."""
    pipeline = [
        {"$match": {"roomid": roomid}},
        {
            "$lookup": {
                "from": "Permission",  # Target collection
                "localField": "roomid",  # Field in the 'Rooms' collection
                "foreignField": "roomid",  # Field in the 'Permission' collection
                "as": "access",  # Alias for the joined data
            }
        },
        {
            "$project": {
                "_id": 0,
                "roomName": "$roomName",
                "whitelisted": {"$arrayElemAt": ["$access.whitelisted", 0]},
                "blacklisted": {"$arrayElemAt": ["$access.blacklisted", 0]},
                "canSend": {"$arrayElemAt": ["$access.canSend", 0]},
                "locked": {"$arrayElemAt": ["$access.locked", 0]},
                "muted": {"$arrayElemAt": ["$access.muted", 0]},
                "banned": {"$arrayElemAt": ["$access.banned", 0]},
            }
        },
    ]

    result = list(Rooms.aggregate(pipeline))
    if not result:
        get_room_data("ilQvQwgOhm9kNAOrRqbr")

    return result[0]

def get_messages(roomid):
    """Gets messages."""
    return Messages.find_one({"roomid": roomid})["messages"]
