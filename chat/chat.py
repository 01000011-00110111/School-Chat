"""chat/chat.py: Backend functions for message handling.
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in app.py or the LICENSE file.
"""
from datetime import datetime
import chat.database as database
from socketio_confg import sio

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

    @staticmethod
    def add_chat(roomid):
        """Add a chat to the list of existing chats."""
        room = database.get_room_data(roomid)
        chat = Chat(room, roomid)
        Chat.chats[roomid] = chat
        return chat

    @staticmethod
    def get_chat(roomid):
        """Get a chat from the list of existing chats."""
        return Chat.chats[roomid]

    async def send_message(self, message):
        """Send a message to the chat."""
        self.messages.append(message)
        self.config["last_message"] = datetime.now()
        for sid in self.sids:
            await sio.emit("message", {"message": message}, to=sid)
        # await sio.emit("message", {"message": message})
