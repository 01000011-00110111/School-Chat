from flask_socketio import emit
from chat import Chat
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
        other.respond_command((0, "not_confirmed"), roomid)
    else:
        message = other.format_system_msg("All Chatrooms locked by Admin.")
        Chat.add_message_to_all(message, "all", None)
        Chat.set_all_lock_status(True)
        emit("message_chat", (message, "all"), broadcast=True)


def lock(**kwargs):
    """locks the chat so that only devs can send"""
    user = kwargs['user']
    roomid = kwargs['roomid']
    room = kwargs['room']
    other.respond_command((0, 'priv'), roomid) if database.check_private(roomid) \
    else None
    if other.check_if_dev(user) == 1:
        message = other.format_system_msg("Chat Locked by Admin.")
        room.add_message(message, None)
        room.set_lock_status(True)
        emit("message_chat", (message, roomid), broadcast=True)
    elif other.check_if_mod(user) == 1:
        message = other.format_system_msg("Chat Locked by Moderator.")
        room.add_message(message, None)
        room.set_lock_status(True)
        emit("message_chat", (message, roomid), broadcast=True)


def unlock(**kwargs):
    """unlocks the chat so that everyone can send"""
    user = kwargs['user']
    roomid = kwargs['roomid']
    room = kwargs['room']
    other.respond_command((0, 'priv'), roomid) if database.check_private(roomid) \
    else None
    if other.check_if_dev(user) == 1:
        message = other.format_system_msg("Chat Unlocked by Admin.")
        room.add_message(message, None)
        room.set_lock_status(False)
        emit("message_chat", (message, roomid), broadcast=True)
    elif other.check_if_mod(user) == 1:
        message = other.format_system_msg("Chat Unlocked by Moderator.")
        room.add_message(message, None)
        room.set_lock_status(False)
        emit("message_chat", (message, roomid), broadcast=True)
