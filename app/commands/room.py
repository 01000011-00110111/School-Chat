"""this is where all room commands goes"""
import app.rooms as rooms
from app.commands import other


def reset_chat_user(**kwargs):
    """Reset the current chatroom."""
    # user = kwargs['user']
    room = kwargs['room']
    # room = Chat.create_or_get_chat(roomid)
    # if other.check_if_dev(user) == 1 or other.check_if_mod(user) == 1:
    #     Chat.reset_chat(False, True, roomid)
    # elif other.check_if_owner(roomid, user) == 1 or other.check_if_room_mod(roomid,
    #                                                             user) == 1:
        # Chat.reset_chat(False, False, roomid)
    room.reset_chat()
    # else:
        # other.respond_command((), roomid, None)


def create_room(**kwargs):
    user = kwargs['user']
    name = kwargs['commands']["v1"]
    roomid = kwargs['roomid']
    result = rooms.create_chat_room(name, user.displayName, user)
    other.respond_command(result, roomid)