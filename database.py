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

#extra
dbm = client.Chat.Chat

def clear_online():
    """Clears the online list"""
    dbm.Online.delete_many({})

#online code
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
        return ID.update_one({user_search: user_input}, {'$set': {search_type: input})

def add_accounts(add_list):
    """Adds accounts to the database"""
    pass#needs lots of work

# room database data
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