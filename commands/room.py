"""this is where all room commands goes
    Copyright (C) 2023  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
import rooms
from commands import other


def reset_chat_user(**kwargs):
    """Reset the current chatroom."""
    room = kwargs['room']
    room.reset_chat()



def create_room(**kwargs):
    """creates a new chat room"""
    user = kwargs['user']
    name = kwargs['commands']["v1"]
    roomid = kwargs['roomid']
    result = rooms.create_chat_room(name, user.display_name, user)
    other.respond_command(result, roomid)
