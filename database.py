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

def find_account(search_type, input):
    return ID.find_one({search_type: input})

def find_all_accounts():
    return ID.find()

def update_account_set(location, user_search, user_input, search_type, input):
    if location == 'id':
        return ID.update_one({user_search: user_input}, {'$set': {search_type: input}})
    if location == 'perm':
        return Permission.update_one({user_search: user_input}, {'$set': {search_type: input}})
    if location == 'costom':
        return Customization.update_one({user_search: user_input}, {'$set': {search_type: input}})

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

def find_room(roomid):
    return Rooms.find_one({"roomid": roomid})