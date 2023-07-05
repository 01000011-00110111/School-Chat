"""All commands ran by devs, mods, users, etc."""
import chat
from main import dbm
from flask_socketio import emit
from time import sleep
import time
import os


def log_commands(message):
    with open('backend/command_log.txt', 'a') as file:
        file.write(message + '\n')


# this is literally what sleep() does
# and this still blocks the thread, like sleep()
def delay(seconds):
    start_time = time.time()
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time >= seconds:
            break


def find_command(commands, user):
    """Send whatever sudo command is issued to its respective function."""
    if commands.get('v0') == 'E':
        print('test')
    elif commands.get('v0') == 'refresh':
        handle_admin_cmds("refresh_users", user)
    elif commands.get('v0') == 'clear':
        handle_admin_cmds("reset_chat", user)
    elif commands.get('v0') == 'lines':
        handle_admin_cmds("line_ct", user)
        #need to be added here as its just called without a check
    elif commands.get('v0') == 'mute':
        username = commands['v1']
        print(username, " and ", user)
        mute_user(username, user)
    elif commands.get('v0') == 'unmute':
        username = commands['v1']
        unmute_user(username, user)
    elif commands.get('v0') == 'ban':
        username = commands['v1']
        ban_user(username, user)
    elif commands.get('v0') == 'lock':
        handle_admin_cmds("lock", user)
    elif commands.get('v0') == 'unlock':
        handle_admin_cmds("unlock", user)


def handle_admin_cmds(cmd: str, user):
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


def check_if_dev(user):
    if user['SPermission'] == 'Debugpass':
        return 1
    return 0


def check_if_mod(user):
    if user['SPermission'] == 'modpass':
        return 1
    return 0


def ban_user(username: str, issuer):
    """Ban a user from the chat forever."""
    is_dev = check_if_dev(issuer)
    if is_dev != 1:
        return

    user = dbm.Accounts.find_one({"displayName": username})
    if user['permission'] == 'banned':
        return
    else:
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


def mute_user(username: str, issuer):
    """Mute a user from the chat."""
    # these need to be run a different way than ban, i wish I could do it like ban but thats not how it works.
    if check_if_dev(issuer) == 1 or check_if_mod(issuer) == 1:
        user = dbm.Accounts.find_one({"displayName": username})
        if user['permission'] in ('banned', 'muted'):
            return
        else:
            dbm.Accounts.update_one({"displayName": username},
                                    {"$set": {
                                        "permission": "muted"
                                    }})
            chat.force_message(
                '[SYSTEM]: <font color="#ff7f00">' + username +
                " is mutted for an undefned period of time.</font>")
            emit("message_chat",
                 '[SYSTEM]: <font color="#ff7f00">' + username +
                 " is mutted for an undefned period of time.</font>",
                 broadcast=True)


def unmute_user(username: str, issuer):
    """Unmute a user from the chat"""
    # see mute_user for explanation
    if check_if_dev(issuer) == 1 or check_if_mod(issuer) == 1:
        user = dbm.Accounts.find_one({"displayName": username})
        if user['permission'] in ('banned', 'true'):
            return
        else:
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
