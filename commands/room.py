"""this is where all room commands goes"""
import chat
import database
# from commands import other

def check_if_dev(user):
    """Return if a user is a dev or not."""
    return 1 if user['SPermission'] == 'Debugpass' else 0


def check_if_mod(user):
    """Return if a user is a mod or not."""
    return 1 if user['SPermission'] == 'modpass' else 0

def check_if_owner(roomid, user):
    """Return if a user is a mod or not."""
    return 1 if database.find_room({'roomid': roomid}, 'id')["generatedBy"] == user['username'] else 0


def check_if_room_mod(roomid, user):
    """Return if a user is a mod or not."""
    return 1 if database.find_room({'roomid': roomid}, 'perm')["mods"] == user['username'] else 0

def reset_chat_user(**kwargs):
    """Reset the current chatroom."""
    user = kwargs['user']
    roomid = kwargs['roomid']
    if check_if_dev(user) == 1 or check_if_mod(user) == 1:
        chat.reset_chat(False, True, roomid)
    elif check_if_owner(roomid, user) == 1 or check_if_room_mod(roomid,
                                                                user) == 1:
        chat.reset_chat(False, False, roomid)
    # else:
        # other.respond_command((), roomid, None)