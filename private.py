"""private.py - Prive Messaging"""
import sched
import time
from datetime import timedelta, datetime
from typing import List
from flask_socketio import SocketIO, emit
import random
from string import ascii_uppercase
import database
from commands.other import format_system_msg
import log


def get_messages_list(sender, receiver):
    """gets the chats with 2 users."""
    userlist = format_userlist(sender, receiver)

    chat = Private.create_or_get_private(userlist)
    
    return chat


def get_messages(vid):
    """gets the chats with 2 users."""
    chat = Private.create_or_get_private(vid)
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
    chats_userlist = {} #or do i make it 

    def __init__(self, private, vid, userlist):
        """Initialize the chat."""
        self.userlist = private["userIds"]
        self.vid = vid
        self.messages = database.get_private_messages(userlist)
        self.unread = private['unread']
        self.backups = [0, 0] # 1st is total and 2nd is total sense last message
        self.last_message = datetime.now()


    @classmethod
    def create_or_get_private(cls, vid):
        """Create a new chat or return an existing one."""
        if vid not in [cls.chats, cls.chats_userlist]:
            private = database.get_private_chat(vid) if isinstance(vid, list) \
                else database.find_private(vid)
            if private is None:
                code = generate_unique_code(12)
                private = database.create_private_chat(vid, code)
            userlist = private['userIds']
            priv_id = private['pmid']
            new_private = cls(private, priv_id, userlist)
            cls.chats[priv_id] = new_private
            cls.chats_userlist[tuple(userlist)] = new_private
            return new_private
        else:
            return cls.chats.get(vid)

    @classmethod
    def get_unread(cls, userlist):
        userlist = (userlist[0], userlist[1])
        if userlist in cls.chats_userlist:
            return cls.chats_userlist[userlist].unread
        else:
            return 0
        

    def add_message(self, message_text: str, uuid) -> None:
        """Handler for messages so they get logged."""
        self.last_message = datetime.now()

        for receiver in self.unread:
            if receiver != uuid:
                self.unread[receiver] += 1
                
        # print(self.backups)
                
        if len(self.messages) >= 250:
            self.reset_chat()
        else:
            self.messages.append(message_text)

        log.backup_log(message_text, self.vid, True)
        return ('room', 1)

    def reset_chat(self):
        """Reset the chat."""
        self.messages.clear()
        msg = format_system_msg('This Private room has been reset.')
        self.messages.append(msg)
        emit("reset_chat", ("admin", self.vid), broadcast=True, namespace="/")


    def backup_data(self):
        database.update_private(self)
        self.backups[0] += 1
        if self.last_message > datetime.now() + timedelta(minutes=30):
            self.backups[1] += 1
            self.delete() if self.backups[1] > 3 else None
            
    def delete(self):
        del Private.chats[self.vid]

# for private in database.get_unread_all():
#     Private.unread.append(private['unread'])