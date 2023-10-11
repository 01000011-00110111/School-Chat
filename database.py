import os
import pymongo

client = pymongo.MongoClient(os.environ["mongo_key"])
#accounts/user data
permission = client.Accounts.Permission
customization = client.Accounts.Customization
user = client.Accounts.Accounts

#chat room data
messages = client.Rooms.Messages
rooms = client.Rooms.Rooms
access = client.Rooms.Permission

#other
games = client.Chat.Games
