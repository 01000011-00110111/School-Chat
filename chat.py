"""chat.py: Backend functions for message handling.
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
import os
from dataclasses import dataclass
from datetime import datetime, timedelta

from flask_socketio import emit

import database
import log


def format_system_msg(msg):
    """Format a message [SYSTEM] would send."""
    # return f'[SYSTEM]: <font color="#ff7f00">{msg}</font>'
    profile = "<img class='message_pfp' src='/static/favicon.ico'></img>"
    user_string = "<p style='color: #ff7f00'>[SYSTEM]</p>"
    message_string = f"<p color='#ff7f00'>{msg}</p>"
    role_string = "<p style='background:\
#ff7f00; color: #ffffff;' class='badge'> [SYSTEM]</p>"
    # perm_string = f"<p style='background:{perm}; color: #ffffff;' class='badge'> {perm}</p>" if user != 'user' else None
    date_str = datetime.now().strftime("%a %I:%M %p ")
    return {
        'profile': profile,
        'user': user_string,
        'message': message_string,
        'badges': [role_string, None],
        'date': date_str
    }

def permission(perm):
    """get the users permission"""
    return 'dev' if 'Debugpass' in perm else 'admin' \
        if 'adminpass' in perm else 'mod' \
        if 'modpass' in perm else None

# import cmds
@dataclass
class ChatConfig:
    """Config stuff for chats."""

    def __init__(self, config):
        self.whitelisted = config["whitelisted"]
        self.banned = config["blacklisted"]
        self.can_send = config["canSend"]
        self.locked = config["locked"]
        self.backups = [0, 0]
        self.last_message =  datetime.now()



class Chat:
    """Chat class."""
    chats = {}  # Dictionary to store existing chats

    def __init__(self, room, roomid):
        """Initialize the chat."""
        self.name = room["roomName"]
        self.vid = roomid
        self.config = ChatConfig(room)
        self.user_data = room["user_data"]
        self.muted = room["muted"]
        self.banned = room["banned"]
        self.messages = database.get_messages(roomid)
        self.sids = []
        self.sids = []


    @classmethod
    def create_or_get_chat(cls, roomid):
        """Create a new chat or return an existing one."""
        cls.log_rooms()
        if roomid in cls.chats:
            return cls.chats[roomid]
        #### create new chat class#######
        if roomid not in cls.chats:
            room = database.get_room_data(roomid)
            new_chat = cls(room, roomid)
            cls.chats[roomid] = new_chat
            return new_chat
        return None

    @classmethod
    def log_rooms(cls):
        """add what this does here."""
        if os.path.exists("backend/chatlog.txt"):
            with open("backend/chatlog.txt", "a", encoding="utf-8") as logfile:
                logfile.write(f"{datetime.now()} - Chat log updated\nChats:\n")
                for key, _chat in cls.chats.items():
                    logfile.write(key+'\n')


    @classmethod
    def set_all_lock_status(cls, status):
        """Sets the lo9ck status on all active chat rooms."""
        for chat in cls.chats:
            chat.config.locked = status

    @classmethod
    def add_message_to_all(cls, message_text: str, _rooms, _permission='false'):
        """ads messsages to all chatrooms"""
        for chat in cls.chats:
            chat.config.last_message = datetime.now()
            _lines = len(chat.messages)
            chat.messages.append(message_text)

            log.backup_log(message_text, chat.vid, False, None)
            return ('room', 1)


    def send_message(self, message_text: str):
        """Emits the message to the chat"""
        emit("message_chat", (message_text), broadcast=True, namespace="/")


    def add_message(self, message_text: str, user, perm=False) -> None:
        """Handler for messages so they get logged."""
        # private = self.vid == "all"
        perm = permission(user.perm[0])
        self.user_data[user.uuid] = [user.role, perm,
                            False if user.uuid not in self.muted else True,
                            False if user.uuid not in self.banned else True]
                            #last 2 is for mute and ban
        self.config.last_message = datetime.now()
        lines = len(self.messages)

        if ((lines >= 350) and not perm):
            self.reset_chat('limit')
        if not any(sudo_cmd in message_text['message'] for sudo_cmd in ["$sudo rc", "$sudo clear"]):
            self.messages.append(message_text)

            for sid in self.sids:
                emit("message_chat", (message_text, self.user_data), to=sid)

            log.backup_log(message_text, self.vid, False, None)
            return ('room', 1)


    def reset_chat(self, type):
        """Reset the chat."""
        self.messages.clear()
        if type == 'limit':
            msg = format_system_msg('Message limit reached chat cleared.')
        else:
            msg = format_system_msg(f'The chat was cleared by {type}.')
        self.messages.append(msg)
        for sid in self.sids:
            emit("reset_chat", (msg), to=sid)


    def set_lock_status(self, status):
        """Changes the chat lock status."""
        self.config.locked = status


    def backup_data(self):
        """Backups the chat room."""
        database.update_chat(self)
        self.config.backups[0] += 1
        if self.config.last_message > datetime.now() + timedelta(minutes=90):
            self.config.backups[1] += 1
            if self.config.backups[1] > 3:
                self.delete()

    def delete(self):
        """Deletes the chat."""
        del Chat.chats[self.vid]
