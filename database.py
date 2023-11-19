import os
import pymongo

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
    
def remove_user():
    """Clears the online list"""
    db.Online.delete_one({})
    
def update_user(username, id):
    db.Online.update_one({"socketid": id},
                        {"$set": {
                            "username": username
                        }})
    
def add_user(username, socketid, location):
    db.Online.insert_one({
            "username": username,
            "socketid": socketid,
            "location": location
    })

# new online code
def find_online():
    user_list = Customization.find()
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
    if location == 'costom':
        return Customization.find(data)
    

def find_account(data, location):
    if location == 'id':
        return ID.find_one(data)
    if location == 'perm':
        return Permission.find_one(data)
    if location == 'costom':
        return Customization.find_one(data)
    
        
def find_all_account(data):
    pipeline = [
        {
            "$lookup": {
                "from": "Permission",  # Target collection
                "localField": "userId",  # Field in the current collection
                "foreignField": "userId",  # Field in the 'Permission' collection
                "as": "permissions"  # Alias for the joined data
            }
        },
        {
            "$lookup": {
                "from": "Customization",  # Target collection
                "localField": "userId",  # Field in the current collection
                "foreignField": "userId",  # Field in the 'Customization' collection
                "as": "customizations"  # Alias for the joined data
            }
        }
    ]

    pipeline.insert(0, {"$match": data})

    result = ID.aggregate(pipeline)
    return list(result)
    
def find_all_accounts():
    return ID.find()

def update_account_set(location, data):
    if location == 'id':
        return ID.update_one(data)
    if location == 'perm':
        return Permission.update_one(data)
    if location == 'costom':
        return Customization.update_one(data)

def add_account(SUsername, SPassword, userid, SEmail, SRole, SDisplayname, locked):
    """Adds a single account to the database"""
    id_data = {
        "username": SUsername,
        "password": hashlib.sha384(bytes(SPassword, 'utf-8')).hexdigest(),
        "userId": userid,
        "email": SEmail
    }
    customization_data = {
        "role": SRole,
        "profile": "",
        "theme": "dark",
        "displayName": SDisplayname,
        "messageColor": "#ffffff",
        "roleColor": "#ffffff",
        "userColor": "#ffffff",
    }
    permission_data = {
        "permission": 'true',
        'locked': locked,
        "warned": '0',
        "SPermission": ""
    }
    
    ID.insert_one(id_data)
    Customization.insert_one(customization_data)
    Permission.insert_one(permission_data)
    
def update_account(userid, messageC, roleC, userC, displayname, role, profile, theme, email):
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
    Messages.update_one({"roomid": roomid},
     {'$set': {
         "messages": [message]
     }})

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
    
def find_rooms(data, location):
    if location == 'id':
        return Rooms.find(data)
    if location == 'acc':
        return Access.find(data)

def distinct_roomids():
    return Rooms.distinct('roomid')

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
                "whitelisted": "$access.whitelisted",  # Access collection field
                "blacklisted": "$access.blacklisted"  # Access collection field
            }
        }
    ]

    rooms = list(Rooms.aggregate(pipeline))
    return rooms

def update_whitelist(id, message):  #combine whitelist and blacklist
    """Adds the whitelisted users to the database"""
    Access.update_one({"id": id},
                         {"$set": {
                             "whitelisted": message
                         }})


def update_blacklist(id, message):
    """Adds the blacklisted users to the database"""
    Access.update_one({"id": id},
                         {"$set": {
                             "blacklisted": message
                         }})
    
def delete_room(data):
    Rooms.find_one_and_delete(data)
    Access.find_one_and_delete(data)
    Messages.find_one_and_delete(data)
    
def add_account(SUsername, SPassword, userid, SEmail, SRole, SDisplayname, locked):
    """Adds a single account to the database"""
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