from flask_socketio import emit
import chat
from cmds import respond_command, check_if_dev, format_system_msg, check_if_mod
import database


def globalock(**kwargs):
    """Locks all chatrooms, only used in emergencies."""
    user = kwargs['user']
    roomid = kwargs['roomid']
    confirm = kwargs['commands']['v1']
    if check_if_dev(user) != 1:
        respond_command(("reason", 2, "not_dev"), roomid, None)
        return

    if confirm != "yes":
        respond_command(("reason", 3, "not_confirmed"), roomid, None)
    else:
        message = format_system_msg("All Chatrooms locked by Admin.")
        chat.add_message(message, "all", "none")
        emit("message_chat", (message, "all"), broadcast=True)
        database.set_all_lock_status("true")


def lock(**kwargs):
    """locks the chat so that only devs can send"""
    user = kwargs['user']
    roomid = kwargs['roomid']
    if check_if_dev(user) == 1:
        message = format_system_msg("Chat Locked by Admin.")
        chat.add_message(message, roomid, 'none')
        emit("message_chat", (message, roomid), broadcast=True)
        database.set_lock_status(roomid, 'true')
    elif check_if_mod(user) == 1:
        message = format_system_msg("Chat Locked by Moderator.")
        chat.add_message(message, roomid, 'none')
        emit("message_chat", (message, roomid), broadcast=True)
        database.set_lock_status(roomid, 'true')
    else:
        respond_command(("reason", 2, "not_mod"), roomid, None)


def unlock(**kwargs):
    """unlocks the chat so that everyone can send"""
    user = kwargs['user']
    roomid = kwargs['roomid']
    if check_if_dev(user) == 1:
        message = format_system_msg("Chat Unlocked by Admin.")
        chat.add_message(message, roomid, 'none')
        emit("message_chat", (message, roomid), broadcast=True)
        database.set_lock_status(roomid, 'false')
    elif check_if_mod(user) == 1:
        message = format_system_msg("Chat Unlocked by Moderator.")
        chat.add_message(message, roomid, 'none')
        emit("message_chat", (message, roomid), broadcast=True)
        database.set_lock_status(roomid, 'false')
    else:
        respond_command(("reason", 2, "not_mod"), roomid, None)
