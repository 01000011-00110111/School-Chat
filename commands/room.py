"""this is where all room commands goes"""
from chat import Chat
import database
import rooms
from commands import other

def reset_chat_user(**kwargs):
    """Reset the current chatroom."""
    # user = kwargs['user']
    roomid = kwargs['roomid']
    room = Chat.create_or_get_chat(roomid)
    # if other.check_if_dev(user) == 1 or other.check_if_mod(user) == 1:
    #     Chat.reset_chat(False, True, roomid)
    # elif other.check_if_owner(roomid, user) == 1 or other.check_if_room_mod(roomid,
    #                                                             user) == 1:
        # Chat.reset_chat(False, False, roomid)
    room.reset_chat()
    # else:
        # other.respond_command((), roomid, None)
    