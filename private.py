"""private.py - Prive Messaging"""
import random
from datetime import datetime, timedelta
from string import ascii_uppercase

from flask_socketio import emit

import database
import log
from commands.other import format_system_msg


def get_messages_list(sender, receiver):
    """gets the chats with 2 users."""
    userlist = format_userlist(sender, receiver)

    chat = Private.create_or_get_private(userlist, sender)
    
    return chat


def get_messages(vid, sender):
    """gets the chats with 2 users."""
    chat = Private.create_or_get_private(vid, sender)
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
        list = private["userIds"]
        self.userlist = list
        self.active = {list[0]: False, list[1]: False}
        self.vid = vid
        self.messages = database.get_private_messages(userlist)
        self.unread = private['unread']
        self.backups = [0, 0] # 1st is total and 2nd is total sense last message
        self.last_message = datetime.now()
        self.sids = []

    @classmethod
    def create_or_get_private(cls, vid, sender):
        if isinstance(vid, list):
            vid_tuple = tuple(vid)
            existing_private = cls.chats_userlist.get(vid_tuple)
        else:
            existing_private = cls.chats.get(vid)
        
        if existing_private:
            existing_private.set_active(sender)
            return existing_private
        
        if isinstance(vid, list):
            private = database.get_private_chat(vid)
        else:
            private = database.find_private(vid)
        
        if private is None:
            code = generate_unique_code(12)
            private = database.create_private_chat(vid, code)
        
        userlist = private['userIds']
        priv_id = private['pmid']
        new_private = cls(private, priv_id, userlist)
        cls.chats[priv_id] = new_private
        cls.chats_userlist[tuple(userlist)] = new_private
        new_private.set_active(sender)
        
        return new_private

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
            if receiver != uuid and not self.active[receiver]:
                self.unread[receiver] += 1
                
        # print(self.backups)
                
        if len(self.messages) >= 250:
            self.reset_chat()
        else:
            for sid in self.sids:
                emit("message_chat", (message_text), room=sid)
            self.messages.append(message_text)

        log.backup_log(message_text, self.vid, True)
        return ('room', 1)

    def set_active(self, sender):
        """Sets the active user."""
        self.active[sender] = True
        self.unread[sender] = 0
    
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