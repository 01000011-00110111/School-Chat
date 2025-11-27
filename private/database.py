"""private/database.py: Backend functions for communicating with MongoDB.
    Copyright (C) 2023-2025  cserver45, cseven, CastyiGlitchxz
    License info can be viewed in app.py or the LICENSE file.
"""

import configparser
from system import format_system_msg

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

def get_all_chats():
    """Returns all private chats formatted as {(userA, userB): pmid}."""
    chats = {}
    for doc in Private.find({}, {"_id": 0, "userids": 1, "pmid": 1}):
        key = tuple(sorted(doc["userids"]))
        chats[key] = doc["pmid"]
    return chats

def private_create(userlist, pmid):
    """creates a private chat"""
    data = {
        "userids": userlist,
        "messages": [{"message": format_system_msg("Temp message")}],
        "pmid": pmid,
    }
    Private.insert_one(data)
    return data

def get_private_chat(pmid):
    """finds a private chat"""
    return Private.find_one({"pmid": pmid})

def save_backup(chat):
    """Saves the private chat."""
    Private.update_one({"pmid": chat.pmid}, {"$set": {"messages": chat.messages}}, upsert=True)
