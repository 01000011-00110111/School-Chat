from flask_socketio import emit
import chat
# from cmds import  other.respond_command, other.check_if_dev, other.format_system_msg, other.check_if_mod
import database
from commands import other


def globalock(**kwargs):
    """Locks all chatrooms, only used in emergencies."""
    # user = kwargs['user']
    roomid = kwargs['roomid']
    confirm = kwargs['commands']['v1']
    other.respond_command((0, 'priv'), roomid) if database.check_private(roomid) \
    else None

    if confirm != "yes":
        other.respond_command(("reason", 3, "not_confirmed"), roomid, None)
    else:
        message = other.format_system_msg("All Chatrooms locked by Admin.")
        chat.add_message(message, "all", "none")
        database.set_all_lock_status("true")
        emit("message_chat", (message, "all"), broadcast=True)


def lock(**kwargs):
    """locks the chat so that only devs can send"""
    user = kwargs['user']
    roomid = kwargs['roomid']
    other.respond_command((0, 'priv'), roomid) if database.check_private(roomid) \
    else None
    if other.check_if_dev(user) == 1:
        message = other.format_system_msg("Chat Locked by Admin.")
        chat.add_message(message, roomid, 'none')
        database.set_lock_status(roomid, 'true')
        emit("message_chat", (message, roomid), broadcast=True)
    elif other.check_if_mod(user) == 1:
        message = other.format_system_msg("Chat Locked by Moderator.")
        chat.add_message(message, roomid, 'none')
        database.set_lock_status(roomid, 'true')
        emit("message_chat", (message, roomid), broadcast=True)


def unlock(**kwargs):
    """unlocks the chat so that everyone can send"""
    user = kwargs['user']
    roomid = kwargs['roomid']
    other.respond_command((0, 'priv'), roomid) if database.check_private(roomid) \
    else None
    if other.check_if_dev(user) == 1:
        message = other.format_system_msg("Chat Unlocked by Admin.")
        chat.add_message(message, roomid, 'none')
        database.set_lock_status(roomid, 'false')
        emit("message_chat", (message, roomid), broadcast=True)
    elif other.check_if_mod(user) == 1:
        message = other.format_system_msg("Chat Unlocked by Moderator.")
        chat.add_message(message, roomid, 'none')
        database.set_lock_status(roomid, 'false')
        emit("message_chat", (message, roomid), broadcast=True)
