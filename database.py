import os
import pymongo
import hashlib

client = pymongo.MongoClient(os.environ["mongo_key"])
#accounts/user data
Permission = client.Accounts.Permission
Customization = client.Accounts.Customization
ID = client.Accounts.Accounts

#chat room data
Rooms = client.Rooms.Rooms
Access = client.Rooms.Permission
Messages = client.Rooms.Messages
Private = client.Rooms.Private

#extra
db = client.Extra


def clear_online():
    """Clears the online list"""
    db.Online.delete_many({})


def remove_user(userid):
    """Removes a user from the online list"""
    ID.update_one({"userId": userid}, {'$set': {"status": 'offline'}})


def update_user(username, id):
    db.Online.update_one({"socketid": id}, {"$set": {"username": username}})


def set_online(userid):
    # db.Online.insert_one({
    #     "username": username,
    #     "socketid": socketid,
    #     "location": location
    # })
    ID.update_one({"userId": userid}, {'$set': {"status": 'online'}})


# new online code
def find_online():
    user_list = ID.find()
    for user in user_list:
        if user["status"] == 'offline':
            user_list.remove(user)
    return user_list


# accounting


def find_data(data, location):
    if location == 'id':
        return ID.find(data)
    if location == 'perm':
        return Permission.find(data)
    if location == 'customization':
        return Customization.find(data)


def find_account(data, location):
    if location == 'id':
        return ID.find_one(data)
    if location == 'perm':
        # print(data)
        return Permission.find_one(data)
    if location == 'customization':
        return Customization.find_one(data)
    

def get_all_online():
    pipeline = [
        {
            "$lookup": {
                "from": "Customization",
                "localField": "userId",
                "foreignField": "userId",
                "as": "customization"
            }
        },
            {
        "$match": {
            "status": { "$ne": "offline" } # Exclude documents where status is "offline"
        }
    },
        {
            "$project": {
                "_id": 0,
                "username": "$username",
                "status": "$status",
                "profile": { "$arrayElemAt": ["$customization.profile", 0] },
                "displayName": { "$arrayElemAt": ["$customization.displayName", 0] },
            }
        }
    ]

    return list(ID.aggregate(pipeline))


def find_account_data(userid):
    pipeline = [
        {
            "$match": {
                "userId": userid
            }
        },
        {
            "$lookup": {
                "from": "Permission",
                "localField": "userId",
                "foreignField": "userId",
                "as": "permissions"
            }
        },
        {
            "$lookup": {
                "from": "Customization",
                "localField": "userId",
                "foreignField": "userId",
                "as": "customization"
            }
        },
        {
            "$project": {
                "_id": 0,
                "userId": "$userId",
                "username": "$username",
                "role": { "$arrayElemAt": ["$customization.role", 0] },
                "profile": { "$arrayElemAt": ["$customization.profile", 0] },
                "displayName": { "$arrayElemAt": ["$customization.displayName", 0] },
                "messageColor": { "$arrayElemAt": ["$customization.messageColor", 0] },
                "roleColor": { "$arrayElemAt": ["$customization.roleColor", 0] },
                "userColor": { "$arrayElemAt": ["$customization.userColor", 0] },
                "permission": { "$arrayElemAt": ["$permissions.permission", 0] },
                "locked": { "$arrayElemAt": ["$permissions.locked", 0] },
                "warned": { "$arrayElemAt": ["$permissions.warned", 0] },
                "SPermission": { "$arrayElemAt": ["$permissions.SPermission", 0] }
            }
        }
    ]

    return list(ID.aggregate(pipeline))[0]
    


def find_all_accounts():
    return ID.find()


def update_account_set(location, data):
    if location == 'id':
        return ID.update_one(data)
    if location == 'perm':
        return Permission.update_one(data)
    if location == 'customization':
        return Customization.update_one(data)


def add_accounts(SUsername, SPassword, userid, SEmail, SRole, SDisplayname,
                 locked):
    """Adds a single account to the database"""
    id_data = {
        "userId": userid,
        "username": SUsername,
        "password": SPassword,
        "email": SEmail,
        'status': 'offline'
    }
    customization_data = {
        "userId": userid,
        "role": SRole,
        "userId": userid,
        "profile": "",
        "theme": "dark",
        "displayName": SDisplayname,
        "messageColor": "#ffffff",
        "roleColor": "#ffffff",
        "userColor": "#ffffff",
    }
    permission_data = {
        "userId": userid,
        "permission": 'true',
        'locked': locked,
        "warned": '0',
        "SPermission": ""
    }

    ID.insert_one(id_data)
    Customization.insert_one(customization_data)
    Permission.insert_one(permission_data)


def update_account(userid, messageC, roleC, userC, displayname, role, profile,
                   theme, email):
    customization_data = {
        "messageColor": messageC,
        "roleColor": roleC,
        "userColor": userC,
        "displayName": displayname,
        "role": role,
        "profile": profile,
        "theme": theme,
    }

    Customization.update_one({'userId': userid}, {'$set': customization_data})
    ID.update_one({'userId': userid}, {'$set': {"email": email}})


def delete_account(user):
    Permission.delete_one({'userId': user["userId"]})
    Customization.delete_one({'userId': user["userId"]})
    ID.delete_one({'userId': user["userId"]})


#### room db edits ####
def clear_chat_room(roomid, message):
    Messages.update_one({"roomid": roomid}, {'$set': {"messages": [message]}})


def send_message_single(message_text: str, roomid):
    Messages.update_one({"roomid": roomid},
                        {'$push': {
                            "messages": message_text
                        }})


def send_message_all(message_text: str):
    Messages.rooms.update_many({}, {'$push': {'messages': message_text}})


def find_room(data, location):
    if location == 'id':
        return Rooms.find_one(data)
    if location == 'acc':
        return Access.find_one(data)
    if location == 'msg':
        return Messages.find_one(data)


def find_rooms(location):
    if location == 'id':
        return Rooms.find()
    if location == 'acc':
        return Access.find()
    if location == 'msg':
        return Messages.find()


def distinct_roomids():
    return Rooms.distinct('roomid')

def distinct_names():
    return Rooms.distinct('roomName')

def distinct_name(roomid):
    return Rooms.find_one({'roomid': roomid})["roomName"]


def get_rooms():
    """Return all available rooms."""
    pipeline = [
        {
            "$lookup": {
                "from": "Permission",  # Target collection
                "localField": "roomid",  # Field in the 'Rooms' collection
                "foreignField": "roomid",  # Field in the 'Permission' collection
                "as": "access"  # Alias for the joined data
            }
        },
        {
            "$project": {
                "_id": 0,
                "name": "$roomName",
                "id": "$roomid",
                "generatedBy": "$generatedBy",
                "mods": "$mods",
                "whitelisted": { "$arrayElemAt": ["$access.whitelisted", 0] },
                "blacklisted": { "$arrayElemAt": ["$access.blacklisted", 0] }
            }
        }
    ]

    return list(Rooms.aggregate(pipeline))


def get_room_data(roomid):
    """Returns all available permission data in that room."""
    pipeline = [
        {
            "$match": {
                "roomid": roomid
            }
        },
        {
            "$lookup": {
                "from": "Permission",  # Target collection
                "localField": "roomid",  # Field in the 'Rooms' collection
                "foreignField": "roomid",  # Field in the 'Permission' collection
                "as": "access"  # Alias for the joined data
            }
        },
        {
             "$project": {
                "_id": 0,
                "roomName": "$roomName",
                "canSend": { "$arrayElemAt": ["$access.canSend", 0] },
                "locked": { "$arrayElemAt": ["$access.locked", 0] }
            }
        }
    ]

    return list(Rooms.aggregate(pipeline))[0]


def get_room_msg_data(roomid):
    """Returns all available message data in that room."""
    pipeline = [
        {
            "$match": {
                "roomid": roomid
            }
        },
        {
            "$lookup": {
                "from": "Messages",  # Target collection
                "localField": "roomid",  # Field in the 'Rooms' collection
                "foreignField": "roomid",  # Field in the 'Permission' collection
                "as": "access"  # Alias for the joined data
            }
        },
        {
            "$project": {
                "_id": 0,
                "roomid": "$roomid",
                "name": "$roomName",
                "msg": { "$arrayElemAt": ["$access.messages", 0] }
            }
        }
    ]

    return list(Rooms.aggregate(pipeline))[0]


def update_whitelist(id, message):  #combine whitelist and blacklist
    """Adds the whitelisted users to the database"""
    Access.update_one({"id": id}, {"$set": {"whitelisted": message}})


def update_blacklist(id, message):
    """Adds the blacklisted users to the database"""
    Access.update_one({"id": id}, {"$set": {"blacklisted": message}})


def delete_room(data):
    Rooms.find_one_and_delete(data)
    Access.find_one_and_delete(data)
    Messages.find_one_and_delete(data)


"""      
def add_rooms(SUsername, SPassword, userid, SEmail, SRole, SDisplayname, locked):
    adds a single account to the database
    room_data = {
        "roomid": code,
        "generatedBy": username,
        "mods": '',
        "generatedAt": generated_at,
        "roomName": name,
        "locked": 'false',
    }
    access_data = {
        "canSend": 'everyone',
        "whitelisted": "everyone",
        "blacklisted": "empty",
    }
    message = { "messages": [
            f"[SYSTEM]: <font color='#ff7f00'><b>{name}</b> created by <b>{username}</b> at {generated_at}.</font>"
        ]}
    
    Rooms.insert_one(room_data)
    Access.insert_one(access_data)
    Messages.insert_one(message)
    """
