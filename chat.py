import sched
import time
from datetime import timedelta, datetime
from typing import List
import os

import psutil

from flask_socketio import emit

import database
import log


def format_system_msg(msg):
    """Format a message [SYSTEM] would send."""
    return f'[SYSTEM]: <font color="#ff7f00">{msg}</font>'

# import cmds

class Chat:
    chats = {}  # Dictionary to store existing chats

    def __init__(self, room, roomid):
        """Initialize the chat."""
        self.name = room["roomName"]
        self.vid = roomid
        self.whitelisted = room["whitelisted"]
        self.banned = room["blacklisted"]
        self.canSend = room["canSend"]
        self.locked = room["locked"]
        self.messages = database.get_messages(roomid)
        self.backups = [0, 0] # 1st is total and 2nd is total sense last message
        self.last_message =  datetime.now()
        self.sids = []
        

    @classmethod
    def create_or_get_chat(cls, roomid):
        """Create a new chat or return an existing one."""
        cls.log_rooms()
        if roomid in cls.chats:
            return cls.chats[roomid]
        if roomid not in cls.chats:
            # print('remade it')
            # Create a new chat instance if it doesn't exist
            room = database.get_room_data(roomid)
            new_chat = cls(room, roomid)
            cls.chats[roomid] = new_chat
            return new_chat

    @classmethod
    def log_rooms(cls):
        if os.path.exists("backend/chatlog.txt"):
            with open("backend/chatlog.txt", "a") as logfile:
                logfile.write(f"{datetime.now()} - Chat log updated\nChats:\n")
                for key, chat in cls.chats.items():
                    logfile.write(key+'\n')
        
        
    @classmethod
    def set_all_lock_status(cls, status):
        for chat in cls.chats:
            chat.locked = status
                
    @classmethod
    def add_message_to_all(cls, message_text: str, rooms, permission='false'):
        """ads messsages to all chatrooms"""
        for chat in cls.chats:
            # private = self.vid == "all"
            chat.last_message = datetime.now()
            lines = len(chat.messages)# if not private else 1

            # if ((lines >= 500) and permission != 'true'):
            #     chat.reset_chat(message_text, False)
            #     chat.messages.append(message_text)
            # else:
            chat.messages.append(message_text)
            # emit("message_chat", (message_text), brodcast=True)

            log.backup_log(message_text, chat.vid, False)
            return ('room', 1)
        
        
    def add_message(self, message_text: str, permission='false') -> None:
        """Handler for messages so they get logged."""
        # private = self.vid == "all"
        self.last_message = datetime.now()
        lines = len(self.messages)# if not private else 1

        if ((lines >= 250) and permission != 'true'):
            self.reset_chat(message_text, False)

        for sid in self.sids:
            emit("message_chat", (message_text), room=sid)
        self.messages.append(message_text)

        log.backup_log(message_text, self.vid, False)
        return ('room', 1)

    def reset_chat(self):
        """Reset the chat."""
        self.messages.clear()
        msg = format_system_msg('Chat reset by an admin.')
        self.messages.append(msg)
        emit("reset_chat", ("admin", self.vid), broadcast=True, namespace="/")
        
    
    def set_lock_status(self, status):
        self.locked = status
        
        
    def backup_data(self):
        database.update_chat(self)
        self.backups[0] += 1
        if self.last_message > datetime.now() + timedelta(minutes=90):
            self.backups[1] += 1
            self.delete() if self.backups[1] > 3 else None
            
    def delete(self):
        del Chat.chats[self.vid]
