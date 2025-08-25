"""private/database.py: Backend functions for communicating with MongoDB.
    Copyright (C) 2023-2025  cserver45, cseven, CastyiGlitchxz
    License info can be viewed in app.py or the LICENSE file.
"""

import configparser


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


Private = client.Rooms.Private

def load_private_rooms():
    """Returns all available permission data in that room."""
    private_rooms = {}
    for room in Private.find():
        pmid = room["pmid"]
        userlist = room["userIds"]
        private_rooms[tuple(userlist)] = pmid
    return private_rooms

def get_pmids():
    """retuns all plivate room ids and userlist"""
    return Private.find({}, {"_id": 0, "userIds": 1, "pmid": 1})
