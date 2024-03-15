import sched
import time
from datetime import timedelta
from typing import List

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
        self.id = roomid
        self.whitelisted = room["whitelisted"]
        self.banned = room["blacklisted"]
        self.canSend = room["canSend"]
        self.locked = room["locked"]
        self.messages = database.get_messages(roomid)
        
        # background tasks
        # app.teardown_appcontext(self.backup_data)
        self.scheduler = sched.scheduler(time.time, time.sleep)
        # Schedule the backup function to run every 15 minutes
        self.scheduler.enter(900, 1, self.backup_data, ())
        

    @classmethod
    def create_or_get_chat(cls, roomid):
        """Create a new chat or return an existing one."""
        if roomid not in cls.chats:
            # Create a new chat instance if it doesn't exist
            room = database.get_room_data(roomid)
            new_chat = cls(room, roomid)
            cls.chats[roomid] = new_chat
            return new_chat
        else:
            # Return the existing chat instance
            return cls.chats[roomid]
        
    def add_message(self, message_text: str, permission='false') -> None:
        """Handler for messages so they get logged."""
        # private = self.id == "all"
        lines = len(self.messages)# if not private else 1

        if ((lines >= 500) and permission != 'true'):
            self.reset_chat(message_text, False)
        else:
            self.messages.append(message_text)

        return ('room', 1)

    def reset_chat(self):
        """Reset the chat."""
        self.messages.clear()
        msg = format_system_msg('Chat reset by an admin.')
        self.messages.append(msg)
        emit("reset_chat", ("admin", self.id), broadcast=True, namespace="/")
        
        
    def backup_data(self):
        database.update_chat(self)
        