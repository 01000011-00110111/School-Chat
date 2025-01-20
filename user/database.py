"""user/database.py: Backend functions for communicating with MongoDB.
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in app.py or the LICENSE file.
"""

import configparser

# import hashlib
# import secrets
# from datetime import datetime

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
Accounts = client.Accounts
Permission = client.Accounts.Permission
Customization = client.Accounts.Customization
ID = client.Accounts.Accounts

def get_login_data():
    """Returns the login data for a user."""
    return ID.find({}, {"_id": 0, "username": 1, "password": 1, "userId": 1})

def get_diplay_names():
    """Returns all users."""
    return Customization.find({}, {"_id": 0, "displayName": 1, "userId": 1})

def get_user_data(uuid):
    """Retrieves all data required to login."""
    pipeline = [
        {
            "$lookup": {
                "from": "Customization",
                "localField": "userId",
                "foreignField": "userId",
                "as": "customization",
            }
        },
        {
            "$lookup": {
                "from": "Permission",
                "localField": "userId",
                "foreignField": "userId",
                "as": "permissions",
            }
        },
        {
            "$project": {
                "_id": 0,
                "uuid": "$userId",
                "status": "$status",
                "username": "$username",
                "password": "$password",
                "email": "$email",
                "role": {"$arrayElemAt": ["$customization.role", 0]},
                "profile": {"$arrayElemAt": ["$customization.profile", 0]},
                "displayName": {"$arrayElemAt": ["$customization.displayName", 0]},
                "messageColor": {"$arrayElemAt": ["$customization.messageColor", 0]},
                "roleColor": {"$arrayElemAt": ["$customization.roleColor", 0]},
                "userColor": {"$arrayElemAt": ["$customization.userColor", 0]},
                "theme": {"$arrayElemAt": ["$customization.theme", 0]},
                # "blocked": {"$arrayElemAt": ["$customization.blocked", 0]},
                # "permission": {"$arrayElemAt": ["$permissions.SPermission", 0]},
                "mutes": {"$arrayElemAt": ["$permissions.mutes", 0]},
                "locked": {"$arrayElemAt": ["$permissions.location", 0]},
                # "warned": {"$arrayElemAt": ["$permissions.location", 0]},
                "SPermission": {"$arrayElemAt": ["$permissions.SPermission", 0]},
                "themeCount": {"$arrayElemAt": ["$permissions.themeCount", 0]},
            }
        },
    ]
    match = [{"$match": {"userId": uuid}}]
    try:
        result = list(ID.aggregate(match + pipeline))[0]
        return result
    except IndexError:
        return None

def get_online_data():
    """Retrieves all data required to login."""
    pipeline = [
        {
            "$lookup": {
                "from": "Customization",
                "localField": "userId",
                "foreignField": "userId",
                "as": "customization",
            }
        },
        {
            "$lookup": {
                "from": "Permission",
                "localField": "userId",
                "foreignField": "userId",
                "as": "permissions",
            }
        },
        {
            "$project": {
                "_id": 0,
                "uuid": "$userId",
                "status": "$status",
                "role": {"$arrayElemAt": ["$customization.role", 0]},
                "profile": {"$arrayElemAt": ["$customization.profile", 0]},
                "displayName": {"$arrayElemAt": ["$customization.displayName", 0]},
                # "roleColor": {"$arrayElemAt": ["$customization.roleColor", 0]},
                # "userColor": {"$arrayElemAt": ["$customization.userColor", 0]},
                "SPermission": {"$arrayElemAt": ["$permissions.SPermission", 0]},
            }
        },
    ]
    try:
        result = list(ID.aggregate(pipeline))
        result_dict = {user["uuid"]: user for user in result}
        return result_dict
        # return result
    except IndexError:
        return None
