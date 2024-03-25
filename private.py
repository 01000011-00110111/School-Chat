"""private.py - Prive Messaging"""
import sched
import time
from datetime import timedelta
from typing import List
from flask_socketio import SocketIO, emit
import random
from string import ascii_uppercase
import database
from commands.other import format_system_msg


def get_messages_list(sender, receiver):
    """gets the chats with 2 users."""
    userlist = format_userlist(sender, receiver)
    db = database.find_private_messages(userlist, sender)
    # database.update_private_messages(userlist, chat['pmid'])
    # print(chat)

    if db is None:
        code = generate_unique_code(12)
        database.create_private_chat(userlist, code)
        db = database.find_private_messages(userlist, sender)

    chat = Private.create_or_get_private(userlist, db)
    
    return chat


def get_messages(id):
    """gets the chats with 2 users."""
    db = database.find_private(id)

    chat = Private.create_or_get_private(db['userIds'], db)

    return chat


def format_userlist(uuid1, uuid2):
    return sorted([uuid1, uuid2], key=lambda x: (not x.isdigit(), x.lower()))

def generate_unique_code(length):
    """Make a room code that doesen't exist yet."""
    rooms = database.distinct_pmid()
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)

        if code not in rooms:
            break

    return code
    

class Private:
    chats = {}  # Dictionary to store existing chats

    def __init__(self, private, id, userlist):
        """Initialize the chat."""
        self.userlist = private["userIds"]
        self.id = id
        self.messages = database.get_private_messages(userlist)
        self.unread = private['unread']

        # background tasks
        # app.teardown_appcontext(self.backup_data)
        self.scheduler = sched.scheduler(time.time, time.sleep)
        # Schedule the backup function to run every 15 minutes
        self.scheduler.enter(900, 1, self.backup_data, ())


    @classmethod
    def create_or_get_private(cls, userlist, private):
        """Create a new chat or return an existing one."""
        id = private['pmid']
        if id not in cls.chats:
            new_private = cls(private, id, userlist)
            cls.chats[id] = new_private
            return new_private
        else:
            return cls.chats[id]

    def add_message(self, message_text: str, uuid) -> None:
        """Handler for messages so they get logged."""
        # private = self.id == "all"
        lines = len(self.messages)# if not private else 1
        dict = self.unread
        print(dict)
        dict.remove(uuid)
        reciver = dict[0]
        self.unread['unread'][reciver] += 1

        if lines >= 250:
            self.reset_chat(message_text, False)
        else:
            self.messages.append(message_text)

        return ('room', 1)

    def reset_chat(self):
        """Reset the chat."""
        self.messages.clear()
        msg = format_system_msg('This Private room has been reset.')
        self.messages.append(msg)
        emit("reset_chat", ("admin", self.id), broadcast=True, namespace="/")


    def backup_data(self):
        database.update_private(self)