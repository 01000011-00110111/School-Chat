import os
import pymongo

client = pymongo.MongoClient(os.environ["mongo_key"])
permission = client.Accounts.Permission
# permission = client.Accounts.permission
# permission = client.Accounts.permission
messages = client.Rooms.Messages