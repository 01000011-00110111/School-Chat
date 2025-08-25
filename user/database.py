"""user/database.py: Backend functions for communicating with MongoDB.
    Copyright (C) 2023-2025  cserver45, cseven, CastyiGlitchxz
    License info can be viewed in app.py or the LICENSE file.
"""

import configparser
import uuid

import hashlib
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

def display_exists(display_name):
    """Checks if a username already exists in the database."""
    return ID.find_one({"displayName": display_name})

def email_exists(email):
    """Checks if an email already exists in the database."""
    return ID.find_one({"email": email})

def get_user_data(user_id):
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
                "badges": {"$arrayElemAt": ["$customization.badges", 0]},
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
    match = [{"$match": {"userId": user_id}}]
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
                "SPermission": {"$arrayElemAt": ["$permissions.SPermission", 0]},
            }
        },
    ]
    try:
        result = list(ID.aggregate(pipeline))
        result_dict = {user["uuid"]: {key: val for key, val in user.items() if key != "uuid"}\
                        for user in result}

        return result_dict
    except IndexError:
        return None


def add_accounts(data):
    """Adds a single account to the database."""
    username = data["username"]
    email = data["email"]
    role = data["role"]
    displayname = data["displayName"]
    user_color = data["userColor"]
    role_color = data["roleColor"]
    message_color = data["messageColor"]
    # locked = data["locked"]

    while True:
        userid = str(uuid.uuid4())
        if userid not in [user["userId"] for user in ID.find()]:
            break

    while True:
        onlineid = str(uuid.uuid4())[:8]
        if onlineid not in [user["onlineId"] for user in ID.find()]:
            break

    # Hash the password before storing it
    password = hashlib.sha384(data["password"].encode('utf-8')).hexdigest()

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
        "badges": [],
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


def update(data, user_id):
    """Updates user data in the database."""
    customization_data = {}

    if "role" in data:
        customization_data["role"] = data["role"]
    if "display_name" in data:
        customization_data["displayName"] = data["display_name"]
    if "m_color" in data:
        customization_data["messageColor"] = data["m_color"]
    if "r_color" in data:
        customization_data["roleColor"] = data["r_color"]
    if "u_color" in data:
        customization_data["userColor"] = data["u_color"]

    Customization.update_one(
        {"userId": user_id},
        {"$set": customization_data}
    )
