"""chat/chat.py: Backend functions for message handling.
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in app.py or the LICENSE file.
"""
import asyncio
from datetime import datetime
import chat.database as database
from socketio_confg import sio
from system import format_system_msg

class Chat:
    """Chat class."""
    all_chats = [(room["roomName"], room["roomid"]) for room in database.get_rooms()]
    chats = {}  # Dictionary to store existing chats

    def __init__(self, room, roomid):
        """Initialize the chat."""
        self.name = room["roomName"]
        self.vid = roomid
        self.config = {
            "whitelisted" : room["whitelisted"],
            "banned": room["blacklisted"],
            "can_send": room["canSend"],
            "locked": room["locked"],
            "backups": [0, 0],
            "last_message":  datetime.now()
        }
        # self.user_data = room["user_data"]
        self.muted = room["muted"]
        self.banned = room["banned"]
        self.messages = database.get_messages(roomid)
        self.sids = {}
        self.images = [] #TO-DO: add images
        self.backup_values = [
            [0, 0], # 1st is total and 2nd is total sense last message
            datetime.now()
        ]

    @staticmethod
    def add_chat(roomid):
        """Add a chat to the list of existing chats."""
        room = database.get_room_data(roomid)
        chat = Chat(room, roomid)
        Chat.chats[roomid] = chat
        asyncio.create_task(chat.run_backup_task())
        return chat

    @staticmethod
    def get_chat(roomid):
        """Get a chat from the list of existing chats."""
        return Chat.chats[roomid]

    async def send_message(self, message):
        """Send a message to the chat."""
        self.messages.append(message)
        self.config["last_message"] = datetime.now()
        lines = len(self.messages)# if not private else 1

        if lines >= 350:# and permission != 'true'):
            self.reset_chat()
        else:
            self.messages.append(message)

        for _, sid in self.sids.items():
            await sio.emit("message", {"message": message}, to=sid)
        # await sio.emit("message", {"message": message})

    async def reset_chat(self):
        """Reset the chat."""
        self.messages.clear()
        msg = format_system_msg('Message limit reached chat cleared.')
        self.messages.append(msg)
        for _, sid in self.sids.items():
            await sio.emit("reset_chat", msg, to=sid)

    async def run_backup_task(self):
        """Run the backup task every 15 minutes."""
        while True:
            await self.backup()
            await asyncio.sleep(15 * 60)

    async def backup(self):
        """Backup the chat."""
        diff = datetime.now() - self.backup_values[1]
        if diff.total_seconds() >= 60:
            print("Backup")
            self.backup_values[0][0] += len(self.messages)
            self.backup_values[0][1] += len(self.messages)
            self.backup_values[1] = datetime.now()
            database.save_backup(self)
