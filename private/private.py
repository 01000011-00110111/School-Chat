"""private.py: Backend functions for the private messaging system.
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
# import asyncio
from datetime import datetime
from system import format_system_msg
from socketio_confg import sio
# pylint: disable=W0406
from private import database
# import private.database as database

pmids = database.get_pmids()

class Private:
    """The Private chat class."""
    chats = {}  # Dictionary to store existing chats
    chats_userlist = database.load_private_rooms()

    def __init__(self, private, pmid):
        """Initialize the chat."""
        lst = private["userIds"]
        self.userlist = lst
        self.active = {lst[0]: False, lst[1]: False}
        self.pmid = pmid
        self.messages = database.get_private_messages(pmid)
        # self.unread = private['unread']
        self.backup_values = [
            [0, 0], # 1st is total and 2nd is total sense last message
            datetime.now()
        ]
        self.sids = {}

    @staticmethod
    def add_chat(pmid):
        """Add a chat to the list of existing chats."""
        room = database.get_priv_data(pmid)
        chat = Private(room, pmid)
        Private.chats[pmid] = chat
        return chat

    @staticmethod
    def get_chat(roomid):
        """Get a chat from the list of existing chats."""
        return Private.chats[roomid]

    async def send_message(self, message):
        """Send a message to the chat."""
        self.messages.append(message)
        # self.config["last_message"] = datetime.now()
        lines = len(self.messages)# if not private else 1

        if lines >= 350:# and permission != 'true'):
            self.reset_chat()
        else:
            self.messages.append(message)

        for _, sid in self.sids.items():
            await sio.emit("message", {"message": message}, to=sid)

    async def reset_chat(self):
        """Reset the chat."""
        self.messages.clear()
        msg = format_system_msg('Message limit reached chat cleared.')
        self.messages.append(msg)
        for _, sid in self.sids.items():
            await sio.emit("reset_chat", msg, to=sid)
