"""this is where all room commands goes"""
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
    result = rooms.create_chat_room(name, user.displayName, user)
    other.respond_command(result, roomid)
