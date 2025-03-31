"""user/database.py: Backend functions for communicating with MongoDB.
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in app.py or the LICENSE file.
"""

import configparser
import uuid

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

def username_exists(username):
    """Checks if a username already exists in the database."""
    return ID.find_one({"username": username})

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
                "onlineId": "$onlineId",
                "status": "$status",
                "role": {"$arrayElemAt": ["$customization.role", 0]},
                "profile": {"$arrayElemAt": ["$customization.profile", 0]},
                "displayName": {"$arrayElemAt": ["$customization.displayName", 0]},
                "SPermission": {"$arrayElemAt": ["$permissions.SPermission", 0]},
            }
        },
    ]
    try:
        result = list(ID.aggregate(pipeline))
        result_dict = {user["onlineId"]: user for user in result}
        return result_dict
    except IndexError:
        return None


def add_accounts(data):
    """Adds a single account to the database."""
    username = data["username"]
    password = data["password"]
    email = data["email"]
    role = data["role"]
    displayname = data["displayName"]
    user_color = data["userColor"]
    role_color = data["roleColor"]
    message_color = data["messageColor"]
    # print(username, password, email, role, displayname, user_color, role_color, message_color)
    # locked = data["locked"]

    while True:
        userid = str(uuid.uuid4())
        if userid not in [user["userId"] for user in ID.find()]:
            break

    while True:
        onlineid = str(uuid.uuid4())[:8]
        if onlineid not in [user["onlineId"] for user in ID.find()]:
            break

    id_data = {
        "userId": userid,
        "onlineId": onlineid,
        "username": username,
        "password": password,
        "email": email,
        "status": "offline",
    }
    customization_data = {
        "userId": userid,
        "role": role,
        "profile": "/icons/favicon.ico",
        "theme": "dark",
        "displayName": displayname,
        "messageColor": message_color,
        "roleColor": role_color,
        "userColor": user_color,
    }
    permission_data = {
        "userId": userid,
        "warned": "0",
        "SPermission": [""],
        "themeCount": 0,
    }

    ID.insert_one(id_data)
    Customization.insert_one(customization_data)
    Permission.insert_one(permission_data)
    # return userid
