"""All commands ran by devs, mods, users, etc."""
import chat
from main import dbm
from flask_socketio import emit
from time import sleep
import os


def ban_user(username: str):
    """Ban a user from the chat forever."""
    dbm.Accounts.update_one({"displayName": username},
                            {"$set": {
                                "permission": "banned"
                            }})
    chat.force_message('[SYSTEM]: <font color="#ff7f00">' + username +
                       " has been banned forever.</font>")
    emit("message_chat",
         '[SYSTEM]: <font color="#ff7f00">' + username +
         " has been banned forever.</font>",
         broadcast=True)


def mute_user(username: str):
    """Mute a user from the chat."""
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
    """Unmute a user from the chat"""
    dbm.Accounts.update_one({"displayName": username},
                            {"$set": {
                                "permission": "true"
                            }})
    chat.force_message('[SYSTEM]: <font color="#ff7f00">' + username +
                       " ihas been unmuted.</font>")
    emit("message_chat",
         '[SYSTEM]: <font color="#ff7f00">' + username +
         " has been unmuted.</font>",
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
    elif cmd == "shutdown":
        run_shutdown()


def handle_cilent_refresh(muteuser):
    """Send command to refresh all clients."""
    emit("reload_pages", muteuser, broadcast=True, namespace="/")


# why is this here
def handle_admin_message(message):
    """Bypass message filtering, used when chat is locked."""
    chat.force_message(message)
    emit("message_chat", message, broadcast=True, namespace="/")


def run_shutdown():
    """Stop the server, but also tell everyone that the server is going down."""
    emit(
        "message_chat",
        "[SYSTEM]: <font color='#ff7f00'>Server going down in 2 Seconds (unknown ETA on restart)</font>",
        broadcast=True,
        namespace='/')
    sleep(2)
    os.system('pkill gunicorn')
