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
        
def create_chat(**kwargs):
    user = kwargs['user']
    commands = kwargs['commands']
    room_name = commands.get('v1', '')
    response = rooms.create_rooms(room_name, user, user["displayName"])
    other.respond_command(response, kwargs['roomid'])