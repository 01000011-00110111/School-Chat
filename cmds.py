import chat
from main import dbm
from flask_socketio import emit
import os

#   aaaaaaaa


def ban_user(username: str):
    """Ban a user from the chat forever (until cookie wipe.)"""
    emit("ban", username, broadcast=True)
    dbm.Accounts.update_one({"displayName": username},
                            {"$set": {
                                "permission": "banned"
                            }})
    chat.force_message('[SYSTEM]: <font color="#ff7f00">' + username +
                       " is mutted for an undefned period of time.</font>")
    emit("message_chat",
         '[SYSTEM]: <font color="#ff7f00">' + username +
         " is Banned for forever.</font>",
         broadcast=True)


def mute_user(username: str):
    """mute a user from the chat untilled mutted or until cookie wipe."""
    emit("mute", username, broadcast=True)
    dbm.Accounts.update_one({"displayName": username},
                            {"$set": {
                                "permission": "muted"
                            }})
    chat.force_message('[SYSTEM]: <font color="#ff7f00">' + username +
                       " is mutted for an undefned period of time.</font>")
    emit("message_chat",
         '[SYSTEM]: <font color="#ff7f00">' + username +
         " is mutted for an undefned period of time.</font>",
         broadcast=True)


def unmute_user(username: str):
    """unmute a user from the chat"""
    emit("unmute", username, broadcast=True)
    dbm.Accounts.update_one({"displayName": username},
                            {"$set": {
                                "permission": "true"
                            }})
    chat.force_message('[SYSTEM]: <font color="#ff7f00">' + username +
                       " is unmuted.</font>")
    emit("message_chat",
         '[SYSTEM]: <font color="#ff7f00">' + username +
         " is unmutted.</font>",
         broadcast=True)


def handle_admin_cmds(cmd: str):
    """Admin commands will be sent here."""
    if cmd == "blanks":
        chat.line_blanks()
    elif cmd == "full_status":
        result = chat.get_stats()
        emit("message_chat", result, broadcast=True)
    elif cmd == "lock":
        chat.add_message(
            "[SYSTEM]: <font color='#ff7f00'>Chat Locked by Admin.</font>")
        emit("message_chat",
             "[SYSTEM]: <font color='#ff7f00'>Chat Locked by Admin.</font>",
             broadcast=True)
        with open("backend/chat.lock", "w", encoding="utf8"):
            pass
    elif cmd == "unlock":
        if os.path.exists("backend/chat.lock"):
            os.remove("backend/chat.lock")
            chat.add_message(
                "[SYSTEM]: <font color='#ff7f00'>Chat Unlocked by Admin.</font>"
            )
            emit(
                "message_chat",
                "[SYSTEM]: <font color='#ff7f00'>Chat Unlocked by Admin.</font>",
                broadcast=True)
    elif cmd == "username_clear":
        dbm.Online.delete_many({})
    elif cmd == "refresh_users":
        dbm.Online.delete_many({})
        emit("force_username", "", broadcast=True)
    elif cmd == "reset_chat":
        chat.reset_chat(False, True)
        emit("reset_chat", broadcast=True, namespace="/")


def handle_cilent_refresh(muteuser):
    """Send command to refresh all clients."""
    emit("reload_pages", muteuser, broadcast=True, namespace="/")


# why is this here
def handle_admin_message(message):
    """Bypass message filtering, used when chat is locked."""
    chat.force_message(message)
    emit("message_chat", message, broadcast=True, namespace="/")