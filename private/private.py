"""private.py: Backend functions for the private messaging system.
    Copyright (C) 2023-2025  cserver45, cseven, CastyiGlitchxz
    License info can be viewed in app.py or the LICENSE file.
"""
import asyncio
import random
from string import ascii_uppercase
from datetime import datetime
from system import format_system_msg
from socketio_confg import sio
# pylint: disable=W0406
from private.database import get_all_chats, private_create, get_private_chat, save_backup

# pmids = database.get_pmids()

class Private:
    """The Private chat class."""
    chats = {}  # Dictionary to store existing chats
    all_chats = get_all_chats()

    def __init__(self, private):
        """Initialize the chat."""
        userlist = private["userids"]
        self.userlist = userlist
        self.active = {userlist[0]: False, userlist[1]: False}
        self.pmid = private["pmid"]
        self.messages = private["messages"]
        self.sids = {}
        self.backup_values = [
            [0, 0], # 1st is total and 2nd is total sense last message
            datetime.now()
        ]

    @staticmethod
    def create_chat(userlist):
        """creates a private chat"""
        pmid = Private.generate_unique_code(5)
        private = private_create(userlist, pmid)
        print(private)
        Private.all_chats[userlist] = pmid
        return Private(private)

    @classmethod
    def check_created(cls, userlist):
        """checks if a private chat has been made"""
        if userlist in cls.all_chats:
            return cls.all_chats[userlist]
        return False

    @staticmethod
    def add_chat(pmid):
        """Add a new private chat or return an existing one."""
        if pmid not in Private.chats:
            room = get_private_chat(pmid)
            chat = Private(room)
            Private.chats[pmid] = chat
            asyncio.create_task(chat.run_backup_task())
            return chat
        else:
            return Private.get_chat(pmid)

    @classmethod
    def get_chat(cls, pmid):
        """Get a chat from the list of existing chats."""
        return cls.chats.get(pmid)

    @classmethod
    def generate_unique_code(cls, length):
        """Make a room code that doesen't exist yet."""
        while True:
            code = ""
            for _ in range(length):
                code += random.choice(ascii_uppercase)

            if code not in cls.all_chats:
                break

        return code

    async def send_message(self, message, reset):
        """Send a message to the chat."""
        print('test')
        lines = len(self.messages)# if not private else 1
        if lines >= 350 or reset:# and permission != 'true'):
            await self.reset_chat()
            return
        else:
            self.messages.append(message)

        for _, sid in self.sids.items():
            await sio.emit("message", {"message": message}, to=sid)
        return

    async def reset_chat(self):
        """Reset the chat."""
        self.messages.clear()
        msg = format_system_msg('Message limit reached chat cleared.')
        self.messages.append(msg)
        for _, sid in self.sids.items():
            await sio.emit("reset_chat", msg, to=sid)

    @staticmethod
    async def run_backup_task(self):
        """Run the backup task every 15 minutes."""
        while True:
            await self.backup(False)
            await asyncio.sleep(15 * 60)

    async def backup(self, force):
        """Backup the chat."""
        diff = datetime.now() - self.backup_values[1]
        if diff.total_seconds() >= 60 or force:
            print("Backup")
            self.backup_values[0][0] += len(self.messages)
            self.backup_values[0][1] += len(self.messages)
            self.backup_values[1] = datetime.now()
            save_backup(self)
