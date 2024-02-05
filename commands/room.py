"""this is where all room commands goes"""
import chat
import database
import rooms
from commands import other

def reset_chat_user(**kwargs):
    """Reset the current chatroom."""
    user = kwargs['user']
    roomid = kwargs['roomid']
    if other.check_if_dev(user) == 1 or other.check_if_mod(user) == 1:
        chat.reset_chat(False, True, roomid)
    elif other.check_if_owner(roomid, user) == 1 or other.check_if_room_mod(roomid,
                                                                user) == 1:
        chat.reset_chat(False, False, roomid)
    # else:
        # other.respond_command((), roomid, None)


def create_room(**kwargs):
    user = kwargs['user']
    name = kwargs['commands']["v1"]
    roomid = kwargs['roomid']
    result = rooms.create_rooms(name, user, user["displayName"])
    other.respond_command(result, roomid)