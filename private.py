"""private.py - Prive Messaging"""
import sched
import time
from datetime import timedelta
from typing import List
from flask_socketio import SocketIO, emit
import random
from string import ascii_uppercase
import database

def get_messages(sender, receiver):
    """gets the chats with 2 users."""
    userlist = format_userlist(sender, receiver)
    chat = Private.create_or_get_private(userlist, sender)
    # database.update_private_messages(userlist, chat['pmid'])
    # print(chat)

    if chat is None:
        code = generate_unique_code(12)
        database.create_private_chat(userlist, code)
        chat = Private.create_or_get_private(userlist, sender)

    return chat


def format_userlist(sender, receiver):
    return sorted([sender, receiver], key=lambda x: (not x[0].isdigit(), x[0].lower()))

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
        self.userlist = private["userlist"]
        self.id = id
        self.messages = database.get_private_messages(userlist)
        self.unread = private['unread']

        # background tasks
        # app.teardown_appcontext(self.backup_data)
        self.scheduler = sched.scheduler(time.time, time.sleep)
        # Schedule the backup function to run every 15 minutes
        self.scheduler.enter(900, 1, self.backup_data, ())


    @classmethod
    def create_or_get_private(cls, userlist):
        """Create a new chat or return an existing one."""
        
        if id not in cls.chats:
            # Create a new chat instance if it doesn't exist
            private = database.get_private_chat(userlist)
            new_private = cls(private, id, userlist)
            cls.chats[id] = new_private
            return new_private
        else:
            # Return the existing chat instance
            return cls.chats[id]

    def add_message(self, message_text: str, permission='false', uuid) -> None:
        """Handler for messages so they get logged."""
        # private = self.id == "all"
        lines = len(self.messages)# if not private else 1

        if ((lines >= 250) and permission != 'true'):
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
        