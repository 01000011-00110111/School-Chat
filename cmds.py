"""All commands ran by devs, mods, users, etc."""
import chat
from main import dbm
from flask_socketio import emit
from time import sleep
import os
import re


def log_commands(message):
    with open('backend/command_log.txt', 'a') as file:
        file.write(message + '\n')


def find_command(commands, user):
    """Send whatever sudo command is issued to its respective function."""
    if commands.get('v0') == 'E':
        print('test')
    elif commands.get('v0') == 'help':
        help_command(user)
    elif commands.get('v0') == 'mute':
        username = commands['v1']
        time = commands['v2']
        reason = ' '.join(list(commands.values())[3:])
        mute_user(username, user, time, reason)
    elif commands.get('v0') == 'unmute':
        username = commands['v1']
        unmute_user(username, user)
    elif commands.get('v0') == 'ban':
        username = commands['v1']
        reason = ' '.join(
            list(commands.values())[2:]
        )  # should i make a ban time  # no, hard to enfore the time for when the ban is lifted, and also bans are permanent
        ban_user(username, user, reason)
    else:
        handle_admin_cmds(commands.get('v0'), user)


def handle_admin_cmds(cmd: str, user):
    """Admin commands will be sent here."""
    if cmd == "blanks":
        if check_if_dev(user) == 1:
            chat.line_blanks()
    elif cmd == "status":
        result = chat.get_stats()
        emit("message_chat", result, broadcast=True)
    elif cmd == "lock":
        if check_if_dev(user) == 1:
            chat.add_message(
                "[SYSTEM]: <font color='#ff7f00'>Chat Locked by Admin.</font>")
            emit(
                "message_chat",
                "[SYSTEM]: <font color='#ff7f00'>Chat Locked by Admin.</font>",
                broadcast=True)
            with open("backend/chat.lock", "w", encoding="utf8"):
                pass
        elif check_if_mod(user) == 1:
            chat.add_message(
                "[SYSTEM]: <font color='#ff7f00'>Chat Locked by Moderator.</font>"
            )
            emit(
                "message_chat",
                "[SYSTEM]: <font color='#ff7f00'>Chat Locked by Moderator.</font>",
                broadcast=True)
            with open("backend/chat.lock", "w", encoding="utf8"):
                pass
    elif cmd == "unlock":
        if check_if_dev(user) == 1:
            if os.path.exists("backend/chat.lock"):
                os.remove("backend/chat.lock")
                chat.add_message(
                    "[SYSTEM]: <font color='#ff7f00'>Chat Unlocked by Admin.</font>"
                )
                emit(
                    "message_chat",
                    "[SYSTEM]: <font color='#ff7f00'>Chat Unlocked by Admin.</font>",
                    broadcast=True)
        elif check_if_mod(user) == 1:
            if os.path.exists("backend/chat.lock"):
                os.remove("backend/chat.lock")
                chat.add_message(
                    "[SYSTEM]: <font color='#ff7f00'>Chat Unlocked by Moderator.</font>"
                )
                emit(
                    "message_chat",
                    "[SYSTEM]: <font color='#ff7f00'>Chat Unlocked by Moderator.</font>",
                    broadcast=True)
    #elif cmd == "username_clear":  just needs to changed to a new thing
    #    dbm.Online.delete_many({})  DANGER DANGER DANGER
    elif cmd == "ronline" or cmd == "ro":
        dbm.Online.delete_many({})
        emit("force_username", "", broadcast=True)
    elif cmd == "clear" or cmd == 'rc':
        if check_if_dev(user) == 1 or check_if_mod(user) == 1:
            chat.reset_chat(False, True)
            emit("reset_chat", broadcast=True, namespace="/")
    elif cmd == "shutdown":
        if check_if_dev(user) == 1:
            run_shutdown()
    elif cmd == "lines" or cmd == "pstats":
        lines = chat.get_line_count()
        emit("message_chat",
             f"[SYSTEM]: <font color='#ff7f00'>Line count is {lines}</font>",
             broadcast=True,
             namespace="/")
    else:
        result = ("reason", 1)
        failed_command(result)


def check_if_dev(user):
    return 1 if user['SPermission'] == 'Debugpass' else 0


def check_if_mod(user):
    return 1 if user['SPermission'] == 'modpass' else 0


def ban_user(username: str, issuer, reason):
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
        if reason == '':
            message = '[SYSTEM]: <font color="#ff7f00">' + username + " has been banned.</font>"
        else:
            message = '[SYSTEM]: <font color="#ff7f00">' + username + " has been banned. Reason: " + reason + "." + "</font>"

        chat.force_message(message)
        emit("message_chat", message, broadcast=True)


def mute_user(username: str, issuer, time, reason):
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
            time_match = re.match(r'^(\d+)([dh])$', time)
            if time_match:
                time_number = time_match.group(1)
                time_letter = time_match.group(2)

                if time_letter == 'd':
                    time_final = time_number + " days"
                elif time_letter == 'h':
                    time_final = time_number + " hours"
                elif time_letter == 'f':
                    time_final == ''

            if reason == '' and time_final == '':
                message = '[SYSTEM]: <font color="#ff7f00">' + username + " is muted for an undefined period of time.</font>"
            elif time_final == '':
                message = '[SYSTEM]: <font color="#ff7f00">' + username + " is muted for an undefined period of time. Reason: " + reason + ".</font>"
            elif reason == '':
                message = '[SYSTEM]: <font color="#ff7f00">' + username + " is mutted for " + time_final + ".</font>"
            else:
                message = '[SYSTEM]: <font color="#ff7f00">' + username + " is mutted for " + time_final + " . Reason: " + reason + "." + "</font>"

            chat.force_message(message)
            emit("message_chat", message, broadcast=True)


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
            message = '[SYSTEM]: <font color="#ff7f00">' + username + " has been unmuted.</font>"

            chat.force_message(message)
            emit("message_chat", message, broadcast=True)


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


def failed_command(result):
    """Tell the client that your message could not be sent for whatever the reason was."""
    if result[0] == 'reason':
        if result[1] == 1:
            fail_str = "[SYSTEM]: <font color='#ff7f00'>command not found use " + '"$sudo help"' + " to see all commands.</font>"
        emit("message_chat", fail_str, namespace="/")


def help_command(issuer):
    with open('backend/command_list.txt', 'r') as file:
        lines = file.readlines()

    start_index = None
    end_index = None

    if check_if_dev(issuer) == 1:
        for i, line in enumerate(lines):
            if 'dev' in line.lower():
                start_index = i + 1
            elif 'mod' in line.lower():
                end_index = i - 1
    elif check_if_mod(issuer) == 1:
        for i, line in enumerate(lines):
            if 'mod' in line.lower():
                start_index = i + 1
            elif 'user' in line.lower():
                end_index = i - 1
    else:
        for i, line in enumerate(lines):
            if 'user' in line.lower():
                start_index = i + 1
            elif 'end' in line.lower():
                end_index = i - 1

    if start_index is None or end_index is None:
        print("Command section not found.")
    else:
        command_line = "[SYSTEM]:<font color='#ff7f00'><br>" + ' '.join(
            line.strip()
            for line in lines[start_index:end_index + 1]) + "</font>"
        print(command_line)
        emit("message_chat", command_line, namespace="/")
