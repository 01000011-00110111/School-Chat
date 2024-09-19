"""database.py: Backend functions for communicating with MongoDB.
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""

import configparser

# import hashlib
import secrets
from datetime import datetime

import pymongo
#pylint: disable=C0302
def format_system_msg(msg):
    """Format a message [SYSTEM] would send."""
    profile = "<img class='message_pfp' src='/static/favicon.ico'></img>"
    user_string = "<p style='color: #ff7f00;'>[SYSTEM]</p>"
    message_string = f"<p style='color: #ffffff;'>{msg}</p>"
    role_string = "<p style='background:\
#ff7f00; color: #ffffff;' class='badge'>System</p>"
    date_str = datetime.now().strftime("%a %I:%M %p ")
    return {
        'profile': profile,
        'user': user_string,
        'message': message_string,
        'badges': [role_string, None],
        'date': date_str
    }


config = configparser.ConfigParser()
config.read("config/keys.conf")
mongo_pass = config["mongodb"]["passwd"]

if config['backend']['ENV'] == 'development': #this check is temp.
    #pylint: disable=E0401
    import certifi
    client = pymongo.MongoClient(mongo_pass, tls=True, tlsCAFile=certifi.where())
    #needed for mac users (might be temp depends on mongo)
else:
    client = pymongo.MongoClient(mongo_pass)


# accounts/user data
Accounts = client.Accounts
Permission = client.Accounts.Permission
Customization = client.Accounts.Customization
ID = client.Accounts.Accounts

# chat room data
Rooms = client.Rooms.Rooms
Access = client.Rooms.Permission
Messages = client.Rooms.Messages
Private = client.Rooms.Private

# extra
Themes = client.Extra.Themes


def clear_online():
    """Clears the online list"""
    # db.Online.delete_many({})
    ID.update_many({"status": "online"}, {"$set": {"status": "offline"}})


def set_offline(userid):
    """Removes a user from the online list"""
    if ID.find_one({"userId": userid})["status"] != "offline-locked":
        ID.update_one({"userId": userid}, {"$set": {"status": "offline"}})


def force_set_offline(userid):
    """Removes a user from the online list"""
    ID.update_one({"userId": userid}, {"$set": {"status": "offline-locked"}})


# def update_user(username, vid):
#     db.Online.update_one({"socketid": vid}, {"$set": {"username": username}})


def set_online(userid, force):
    """sets the user online"""
    if not force and ID.find_one({"userId": userid})["status"] != "offline-locked":
        ID.update_one({"userId": userid}, {"$set": {"status": "online"}})
    if force:
        ID.update_one({"userId": userid}, {"$set": {"status": "online"}})


# accounting


def distinct_userids():
    """Returns all userids"""
    return ID.distinct("userId")


def find_data(location):
    """Finds all user data in a specific database."""
    data = None
    if location == "vid":
        data = ID.find()
    if location == "perm":
        data = Permission.find()
    if location == "customization":
        data = Customization.find()
    return data


def find_userid(user):
    """Finds a userid of a user."""
    userid = ID.find_one({"username": user})
    if userid is None:
        userid = Customization.find_one({"displayName": user})
    return None if userid is None else userid["userId"]


def get_email(userid):
    """Gets the email of a specific user."""
    return ID.find_one({"userId": userid})["email"]


def find_account(data, location):
    """Finds a user's data in a specific database."""
    values = None
    if location == "vid":
        values = ID.find_one(data)
    if location == "perm":
        values = Permission.find_one(data)
    if location == "customization":
        values = Customization.find_one(data)
    return values


def get_all_offline():
    """gets all offline users"""
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
                "as": "permission",
            }
        },
        {
            "$project": {
                "_id": 0,
                "userid": "$userId",
                "username": "$username",
                "status": "$status",
                "profile": {"$arrayElemAt": ["$customization.profile", 0]},
                "role": {"$arrayElemAt": ["$customization.role", 0]},
                "displayName": {"$arrayElemAt": ["$customization.displayName", 0]},
                "perm": {"$arrayElemAt": ["$permission.SPermission", 0]},
            }
        },
    ]

    return list(ID.aggregate(pipeline))


def find_login_data(value, login):
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
                "userId": "$userId",
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
                "permission": {"$arrayElemAt": ["$permissions.SPermission", 0]},
                # "mutes": {"$arrayElemAt": ["$permissions.mutes", 0]},
                "locked": {"$arrayElemAt": ["$permissions.location", 0]},
                "warned": {"$arrayElemAt": ["$permissions.location", 0]},
                "SPermission": {"$arrayElemAt": ["$permissions.SPermission", 0]},
            }
        },
    ]
    match = (
        [{"$match": {"username": value}}]
        if not login
        else [{"$match": {"userId": value}}]
    )
    try:
        result = list(ID.aggregate(match + pipeline))[0]
        return result
    except IndexError:
        return None


def find_target_data(display_name):
    """Retrieves all data required to open targe class."""
    uuid = Customization.find_one({"displayName": display_name})['userId']
    pipeline = [
        {"$match": {"userId": uuid}},
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
                "userId": "$userId",
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
                "permission": {"$arrayElemAt": ["$permissions.SPermission", 0]},
                # "mutes": {"$arrayElemAt": ["$permissions.mutes", 0]},
                "locked": {"$arrayElemAt": ["$permissions.location", 0]},
                "warned": {"$arrayElemAt": ["$permissions.location", 0]},
                "SPermission": {"$arrayElemAt": ["$permissions.SPermission", 0]},
            }
        },
    ]
    try:
        result = list(ID.aggregate(pipeline))[0]
        return result
    except IndexError:
        return None



def find_account_data(userid):
    """Retrieves account data of a user."""
    pipeline = [
        {"$match": {"userId": userid}},
        {
            "$lookup": {
                "from": "Permission",
                "localField": "userId",
                "foreignField": "userId",
                "as": "permissions",
            }
        },
        {
            "$lookup": {
                "from": "Customization",
                "localField": "userId",
                "foreignField": "userId",
                "as": "customization",
            }
        },
        {
            "$project": {
                "_id": 0,
                "userId": "$userId",
                "username": "$username",
                "email": "$email",
                "role": {"$arrayElemAt": ["$customization.role", 0]},
                "profile": {"$arrayElemAt": ["$customization.profile", 0]},
                "theme": {"$arrayElemAt": ["$customization.theme", 0]},
                "displayName": {"$arrayElemAt": ["$customization.displayName", 0]},
                "messageColor": {"$arrayElemAt": ["$customization.messageColor", 0]},
                "roleColor": {"$arrayElemAt": ["$customization.roleColor", 0]},
                "userColor": {"$arrayElemAt": ["$customization.userColor", 0]},
                "permission": {"$arrayElemAt": ["$permissions.permission", 0]},
                # "mutes": {"$arrayElemAt": ["$permissions.mutes", 0]},
                "locked": {"$arrayElemAt": ["$permissions.locked", 0]},
                "warned": {"$arrayElemAt": ["$permissions.warned", 0]},
                "SPermission": {"$arrayElemAt": ["$permissions.SPermission", 0]},
            }
        },
    ]
    return list(ID.aggregate(pipeline))[0]


def find_account_room_data(userid):
    """Retrieves room's data."""
    pipeline = [
        {"$match": {"userId": userid}},
        {
            "$lookup": {
                "from": "Permission",
                "localField": "userId",
                "foreignField": "userId",
                "as": "permissions",
            }
        },
        {
            "$lookup": {
                "from": "Customization",
                "localField": "userId",
                "foreignField": "userId",
                "as": "customization",
            }
        },
        {
            "$project": {
                "displayName": {"$arrayElemAt": ["$customization.displayName", 0]},
                "permission": {"$arrayElemAt": ["$permissions.permission", 0]},
                # "mutes": {"$arrayElemAt": ["$permissions.mutes", 0]},
                "locked": {"$arrayElemAt": ["$permissions.locked", 0]},
                "warned": {"$arrayElemAt": ["$permissions.warned", 0]},
                "SPermission": {"$arrayElemAt": ["$permissions.SPermission", 0]},
            }
        },
    ]
    return list(ID.aggregate(pipeline))[0]


def find_all_accounts():
    """finds all accounts"""
    return ID.find()


def update_account_set(location, data, data2):
    """Updates a account data in a specific location."""
    values = None
    if location == "vid":
        values = ID.update_one(data, data2, upsert=True)
    if location == "perm":
        values = Permission.update_one(data, data2, upsert=True)
    if location == "customization":
        values = Customization.update_one(data, data2, upsert=True)
    return values


def add_accounts(data):
    """Adds a single account to the database."""
    username = data["username"]
    password = data["password"]
    userid = data["userid"]
    email = data["email"]
    role = data["role"]
    displayname = data["displayname"]
    locked = data["locked"]

    id_data = {
        "userId": userid,
        "username": username,
        "password": password,
        "email": email,
        "status": "offline",
    }
    customization_data = {
        "userId": userid,
        "role": role,
        "profile": "",#latter asign a uniqe profile image path but keep the favicon
        "theme": "dark",
        "displayName": displayname,
        "messageColor": "#ffffff",
        "roleColor": "#ffffff",
        "userColor": "#ffffff",
        "badges": [],
    }
    permission_data = {
        "userId": userid,
        "permission": "true",
        # "mutes": [],
        "locked": locked,
        "warned": "0",
        "SPermission": [""],
    }

    ID.insert_one(id_data)
    Customization.insert_one(customization_data)
    Permission.insert_one(permission_data)


def update_account(user_data):
    """Updates a user's account."""
    userid = user_data["userid"]
    customization_data = {
        "messageColor": user_data["message_color"],
        "roleColor": user_data["role_color"],
        "userColor": user_data["user_color"],
        "displayName": user_data["displayname"],
        "role": user_data["role"],
        "profile": user_data["profile"],
        "theme": user_data["theme"],
        # "badges": user_data["badges"],
    }

    Customization.update_one(
        {"userId": userid}, {"$set": customization_data}, upsert=True
    )
    ID.update_one({"userId": userid}, {"$set": {"email": user_data["email"]}}, upsert=True)


def backup_user(user):
    """Saves a users data."""
    customization_data = {
        "messageColor": user.m_color,
        "roleColor": user.r_color,
        "userColor": user.u_color,
        "displayName": user.display_name,
        "role": user.role,
        "profile": user.profile,
        "theme": user.theme,
        "badges": user.badges,
    }
    permission_data = {
        "SPermission": user.perm,
        # "warned": user.warned,
    }

    Customization.update_one(
        {"userId": user.uuid}, {"$set": customization_data}, upsert=True
    )
    Permission.update_one({"userId": user.uuid}, {"$set": permission_data}, upsert=True)


def delete_account(user):
    """deletes a users account."""
    Permission.delete_one({"userId": user["userId"]})
    Customization.delete_one({"userId": user["userId"]})
    ID.delete_one({"userId": user["userId"]})


#### room db edits ####
def find_room(data, location):
    """Finds room data in a specific location."""
    values = None
    if location == "vid":
        values = Rooms.find_one(data)
    if location == "acc":
        values = Access.find_one(data)
    if location == "msg":
        values = Messages.find_one(data)
    return values


def find_rooms(location):
    """Finds all rooms in a specific location."""
    values = None
    if location == "vid":
        values = Rooms.find()
    if location == "acc":
        values = Access.find()
    if location == "msg":
        values = Messages.find()
    return values


def distinct_roomids():
    """Gets all room id's."""
    return Rooms.distinct("roomid")


def distinct_names():
    """Gets all room names."""
    return Rooms.distinct("roomName")


def distinct_name(roomid):
    """Gets a specific room's name."""
    return Rooms.find_one({"roomid": roomid})["roomName"]


def get_rooms():
    """Return all available rooms."""
    pipeline = [
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
                "name": "$roomName",
                "vid": "$roomid",
                "generatedBy": "$generatedBy",
                "mods": "$mods",
                "whitelisted": {"$arrayElemAt": ["$access.whitelisted", 0]},
                "blacklisted": {"$arrayElemAt": ["$access.blacklisted", 0]},
            }
        },
    ]

    return list(Rooms.aggregate(pipeline))


def get_room(roomid):
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
                "name": "$roomName",
                "vid": "$roomid",
                "generatedBy": "$generatedBy",
                "mods": "$mods",
                "whitelisted": {"$arrayElemAt": ["$access.whitelisted", 0]},
                "blacklisted": {"$arrayElemAt": ["$access.blacklisted", 0]},
                "canSend": {"$arrayElemAt": ["$access.canSend", 0]},
                "locked": {"$arrayElemAt": ["$access.locked", 0]},
                # "user_data": {"$arrayElemAt": ["$access.user_data", 0]},/
                "muted": {"$arrayElemAt": ["$access.muted", 0]},
                "banned": {"$arrayElemAt": ["$access.banned", 0]},
            }
        },
    ]

    return list(Rooms.aggregate(pipeline))[0]


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
                "user_data": {"$arrayElemAt": ["$access.user_data", 0]},
                "muted": {"$arrayElemAt": ["$access.muted", 0]},
                "banned": {"$arrayElemAt": ["$access.banned", 0]},
            }
        },
    ]

    result = list(Rooms.aggregate(pipeline))
    if not result:
        get_room_data("ilQvQwgOhm9kNAOrRqbr")

    return result[0]


def get_room_msg_data(roomid):
    """Returns all available message data in that room."""
    pipeline = [
        {"$match": {"roomid": roomid}},
        {
            "$lookup": {
                "from": "Messages",  # Target collection
                "localField": "roomid",  # Field in the 'Rooms' collection
                "foreignField": "roomid",  # Field in the 'Permission' collection
                "as": "access",  # Alias for the joined data
            }
        },
        {
            "$project": {
                "_id": 0,
                "roomid": "$roomid",
                "name": "$roomName",
                "msg": {"$arrayElemAt": ["$access.messages", 0]},
            }
        },
    ]
    return list(Rooms.aggregate(pipeline))[0]


def get_messages(roomid):
    """Gets messages."""
    return Messages.find_one({"roomid": roomid})["messages"]


def update_chat(chat):
    """Updates a chatrooms data."""
    room_data = {
        "roomName": chat.name,
    }
    access_data = {
        "whitelisted": chat.config.whitelisted,
        "blacklisted": chat.config.banned,
        "canSend": chat.config.can_send,
        "locked": chat.config.locked,
        "muted": chat.muted,
        "banned": chat.banned,
    }

    # Rooms.insert_one(room_data)
    Rooms.update_one({"roomid": chat.vid}, {"$set": room_data}, upsert=True)
    Access.update_one({"roomid": chat.vid}, {"$set": access_data}, upsert=True)
    Messages.update_one(
        {"roomid": chat.vid}, {"$set": {"messages": chat.messages}}, upsert=True
    )


def update_whitelist(vid, message):  # combine whitelist and blacklist
    """Adds the whitelisted users to the database"""
    Access.update_one({"roomid": vid}, {"$set": {"whitelisted": message}}, upsert=True)


def update_blacklist(vid, message):
    """Adds the blacklisted users to the database"""
    Access.update_one({"roomid": vid}, {"$set": {"blacklisted": message}}, upsert=True)


def delete_room(vid):
    """Deletes a room."""
    Rooms.delete_one({"roomid": vid})
    Access.delete_one({"roomid": vid})
    Messages.delete_one({"roomid": vid})


def set_lock_status(roomid, locked: str):
    """Set a room's locked status."""
    Access.update_one({"roomid": roomid}, {"$set": {"locked": locked}}, upsert=True)


def set_all_lock_status(locked: str):
    """Set all rooms' locked status."""
    Access.update_many({}, {"locked": locked}, upsert=True)


def add_rooms(code, username, displayname, generated_at, name, message):
    """Creates a new chatroom."""
    if message == "System_regular":
        message = f"<b>{name}</b> created by \
                <b>{displayname}</b> at {generated_at}."

    room_data = {
        "roomid": code,
        "generatedBy": username,
        "mods": "",
        "generatedAt": generated_at,
        "roomName": name,
    }

    access_data = {
        "roomid": code,
        "whitelisted": "everyone",
        "blacklisted": "empty",
        "canSend": "everyone",
        "locked": False,
        "user_data": {},
        "muted": {},
        "banned": {},
    }
    message = {
        "roomid": code,
        "messages": [
            format_system_msg(message)
        ],
    }

    Rooms.insert_one(room_data)
    Access.insert_one(access_data)
    Messages.insert_one(message)


def check_private(pmid):
    """looks for a private chat room"""
    return bool(Private.find_one({"pmid": pmid}))


def find_private(pmid):
    """find the chat with 2 users"""
    pm_id = Private.find_one({"pmid": pmid})
    return pm_id


def get_unread(ulist, uuid):
    """find the chat with 2 users"""
    chat = Private.find_one({"userIds": ulist})
    if chat is None:
        return 0
    return chat["unread"][uuid]


def get_unread_all():
    """Gets all private chats."""
    return Private.find()


def get_private_chat(userlist):
    """Gets a private chat."""
    return Private.find_one({"userIds": userlist})


def get_private_messages(ulist):
    """Gets private chat messages."""
    return Private.find_one({"userIds": ulist})["messages"]


def find_private_messages(userlist, sender):
    """find the chat with 2 users"""
    pm_id = Private.find_one({"userIds": userlist})
    if pm_id is not None:
        pm_id["unread"][sender] = 0
        Private.update_one(
            {"userIds": userlist}, {"$set": {"unread": pm_id["unread"]}}, upsert=True
        )
    return pm_id


def update_private(priv):
    """Updates a private chat's data."""
    access_data = {
        "messages": priv.messages,
        "unread": priv.unread,
    }

    # Rooms.insert_one(room_data)
    Private.update_one({"pmid": priv.vid}, {"$set": access_data}, upsert=True)


def create_private_chat(userlist, code):
    """creates a private chat with 2 users"""
    # i = userlist.split(',')
    data = {
        "userIds": userlist,
        "messages": ["This is a private chat with you and one other user"],
        "pmid": code,
        "unread": {userlist[0]: 0, userlist[1]: 0},
    }
    Private.insert_one(data)
    return data


def distinct_pmid():
    """Find all Private Message IDs"""
    return Private.distinct("pmid")


def check_roomids(roomid):
    """checks if the system chat rooms are there"""
    result = Rooms.find_one({"roomid": roomid})
    print(bool(result))
    return bool(result)


def check_roomnames(name):
    """checks if the system chat rooms are there"""
    result = Rooms.find_one({"roomName": name})
    print(bool(result))
    return bool(result)


def check_themes(name):
    """checks if the system chat rooms are there"""
    result = Themes.find_one({"themeID": name})
    print(bool(result))
    return bool(result)


def setup_chatrooms():
    """sets up the starter chat rooms"""
    if not check_roomids("ilQvQwgOhm9kNAOrRqbr"):
        generate_main()
    if not check_roomids("zxMhhAPfWOxuZylxwkES"):
        generate_locked()
    if not check_roomnames("Dev Chat"):
        generate_other("Dev Chat", "devonly")
    if not check_roomnames("Mod Chat"):
        generate_other("Mod Chat", "modonly")
    if not check_roomnames("Commands"):
        generate_other("Commands", "devonly")
    if not check_themes("dark"):
        dark()
    if not check_themes("light"):
        light()


def generate_main():
    """Generates the Main chat room"""
    room_data = {
        "roomid": "ilQvQwgOhm9kNAOrRqbr",
        "generatedBy": "[SYSTEM]",
        "mods": "",
        "generatedAt": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "roomName": "Main",
    }

    access_data = {
        "roomid": "ilQvQwgOhm9kNAOrRqbr",
        "whitelisted": "everyone",
        "blacklisted": "empty",
        "canSend": "everyone",
        "locked": "false",
    }
    message = {
        "roomid": "ilQvQwgOhm9kNAOrRqbr",
        "messages": [
            format_system_msg(f"""<b>Main</b> created by <b>[SYSTEM]</b>
            at {datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}.""")
        ],
    }

    Rooms.insert_one(room_data)
    Access.insert_one(access_data)
    Messages.insert_one(message)


def generate_locked():
    """Generates the Locked chat room"""
    room_data = {
        "roomid": "zxMhhAPfWOxuZylxwkES",
        "generatedBy": "[SYSTEM]",
        "mods": "",
        "generatedAt": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "roomName": "Locked Chat",
    }

    access_data = {
        "roomid": "zxMhhAPfWOxuZylxwkES",
        "whitelisted": "lockedonly",
        "blacklisted": "empty",
        "canSend": "everyone",
        "locked": "false",
    }
    message = {
        "roomid": "zxMhhAPfWOxuZylxwkES",
        "messages": [
            format_system_msg(f"""<b>Locked Chat</b> created by
            <b>[SYSTEM]</b> at {datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}.""")
        ],
    }

    Rooms.insert_one(room_data)
    Access.insert_one(access_data)
    Messages.insert_one(message)


def generate_other(name, permission):
    """Generates a chat room"""
    roomid = secrets.token_hex(10)
    room_data = {
        "roomid": roomid,
        "generatedBy": "[SYSTEM]",
        "mods": "",
        "generatedAt": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "roomName": name,
    }

    access_data = {
        "roomid": roomid,
        "whitelisted": permission,
        "blacklisted": "empty",
        "canSend": "everyone",
        "locked": "false",
    }
    message = {
        "roomid": roomid,
        "messages": [
            format_system_msg(f"""<b>{name}</b> created by <b>[SYSTEM]</b>
            at {datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}.""")
        ],
    }

    Rooms.insert_one(room_data)
    Access.insert_one(access_data)
    Messages.insert_one(message)


def dark():
    """Creates the Dark theme."""
    theme = {
        "body": "rgb(2, 2, 2)",
        "chat-text": "rgb(255, 255, 255)",
        "chat-background": "rgb(255, 255, 255)",
        'chat-color': 'rgb(0, 0, 0)',
        "sides-text": "rgb(0, 0, 0)",
        "sides-background": "rgb(23, 23, 23)",
        "sidebar-background": "rgb(33 , 33, 33)",
        "sidebar-boxShadow": "rgb(33, 33, 33)",
        "sidebar-border": "rgb(255, 255, 255)",
        "sidebar-text": "rgb(255, 255, 255)",
        "topleft-background": "rgb(25, 32, 128)",
        "topleft-text": "rgb(255, 255, 255)",
        "send-background": "rgb(255, 255, 255)",
        "send-text": "rgb(0, 0, 0)",
        "sidenav-background": "rgb(23, 23, 23)",
        "sidenav-text": "rgb(255, 255, 255)",
        "sidenav-a-background": "rgb(23, 23, 23)",
        "sidenav-a-color": "rgb(255, 255, 255)",
        "roomText-text": "rgb(255, 255, 255)",
        "topbar-background": "rgb(23, 23, 23)",
        "topbar-boxShadow": "rgb(12, 12, 12)",
        'online-color': 'rgb(255, 255, 255)',
        'offline-color': 'rgb(255, 255, 255)',
    }
    project = {
        "name": "Dark",
        "themeID": "dark",
        "author": [None, "[SYSTEM]"],
        "status": "public",
        "theme": theme,
    }
    Themes.insert_one(project)


def light():
    """Creates the Light theme."""
    theme = {
        "body": "rgb(200, 200, 200)",
        "chat-text": "rgb(0, 0, 0)",
        "chat-background": "rgb(255, 255, 255)",
        'chat-color': 'rgb(0, 0, 0)',
        "sides-text": "rgb(100, 100, 100)",
        "sides-background": "rgb(230, 230, 230)",
        "sidebar-background": "rgb(220, 220, 220)",
        "sidebar-boxShadow": "rgb(255, 255, 255)",
        "sidebar-border": "rgb(150, 150, 150)",
        "sidebar-text": "rgb(0, 102, 153)",
        "topleft-background": "rgb(100, 160, 200)",
        "topleft-text": "rgb(40, 60, 80)",
        "send-background": "rgb(200, 210, 220)",
        "send-text": "rgb(0, 51, 102)",
        "sidenav-background": "rgb(220, 220, 220)",
        "sidenav-text": "rgb(220, 220, 220)",
        "sidenav-a-background": "rgb(243, 243, 243)",
        "sidenav-a-color": "rgb(0, 0, 0)",
        "roomText-text": "rgb(0, 0, 0)",
        "topbar-background": "rgb(220, 220, 220)",
        "topbar-boxShadow": "rgb(255, 255, 255)",
        'online-color': 'rgb(0, 0, 0)',
        'offline-color': 'rgb(0, 0, 0)',
    }
    project = {
        "name": "Light",
        "themeID": "light",
        "author": [None, "[SYSTEM]"],
        "status": "public",
        "theme": theme,
    }
    Themes.insert_one(project)


##### theme stuff


def get_all_projects():
    """Returns all projects."""
    return Themes.find()


def get_projects(uuid, displayname):
    """returns a specific project."""
    return Themes.find({"author": [uuid, displayname]})


def create_project(uuid, displayname, code):
    """Creates a Project."""
    theme = {
        "body": "rgb(2, 2, 2)",
        "chat-text": "rgb(255, 255, 255)",
        "chat-background": "rgb(255, 255, 255)",
        'chat-color': 'rgb(0, 0, 0)',
        "sides-text": "rgb(0, 0, 0)",
        "sides-background": "rgb(23, 23, 23)",
        "sidebar-background": "rgb(33 , 33, 33)",
        "sidebar-boxShadow": "rgb(33, 33, 33)",
        "sidebar-border": "rgb(255, 255, 255)",
        "sidebar-text": "rgb(255, 255, 255)",
        "topleft-background": "rgb(25, 32, 128)",
        "topleft-text": "rgb(255, 255, 255)",
        "send-background": "rgb(255, 255, 255)",
        "send-text": "rgb(0, 0, 0)",
        "sidenav-background": "rgb(23, 23, 23)",
        "sidenav-text": "rgb(255, 255, 255)",
        "sidenav-a-background": "rgb(23, 23, 23)",
        "sidenav-a-color": "rgb(255, 255, 255)",
        "roomText-text": "rgb(255, 255, 255)",
        "topbar-background": "rgb(23, 23, 23)",
        "topbar-boxShadow": "rgb(12, 12, 12)",
        'online-color': 'rgb(255, 255, 255)',
        'offline-color': 'rgb(255, 255, 255)',
    }

    project = {
        "name": "Untitled Project",
        "themeID": code,
        "author": [uuid, displayname],
        "status": "private",
        "theme": {},
        "project": theme,
    }
    Themes.insert_one(project)
    return project


def get_project(theme_id):
    """Returns a project."""
    return Themes.find_one({"themeID": theme_id})


def save_project(theme_id, theme, name, publish):
    """Saves a project."""
    update_fields = {
        "name": name,
        "project": theme,
    }

    if publish:
        update_fields["theme"] = theme

    Themes.update_one(
        {"themeID": theme_id},
        {"$set": update_fields},
        # upsert=True
    )


def update_theme_status(theme_id, status):
    """Changes the theme status in the database."""
    Themes.update_one({'themeID': theme_id}, {"$set": {'status': status}})


def delete_project(theme_id):
    """Deletes a project."""
    Themes.delete_one({"themeID": theme_id})
