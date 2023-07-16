"""All commands ran by devs, mods, users, etc."""
import chat
from main import dbm
from flask_socketio import emit
from time import sleep
import os
import re
import rooms


def log_commands(message):
    """Log when a command is issued."""
    with open('backend/command_log.txt', 'a', encoding="utf8") as file:
        file.write(message + '\n')


def find_command(commands, user, roomid):
    """Send whatever sudo command is issued to its respective function."""
    # maybe redo this simmilar to how respond_command works (not sure how to do the function bit -cserver)
    # to be done after research
    if commands.get('v0') == 'E':
        print('test')
    elif commands.get('v0') == 'help':
        help_command(user, roomid)
    elif commands.get('v0') == "chat":
        chat_room_edit(commands, roomid, user)
    elif commands.get('v0') == 'mute':
        username = commands['v1']
        time = commands['v2']
        reason = ' '.join(list(commands.values())[3:])
        mute_user(username, user, time, reason, roomid)
    elif commands.get('v0') == 'unmute':
        username = commands['v1']
        unmute_user(username, user, roomid)
    elif commands.get('v0') == 'ban':
        username = commands['v1']
        reason = ' '.join(list(commands.values())[2:])
        ban_user(username, user, reason, roomid)
    elif commands.get('v0') == "blanks":
        if check_if_dev(user) == 1:
            chat.line_blanks(roomid)
        else:
            respond_command(("reason", 2, "not_dev"), roomid, None)
    elif commands.get('v0') == "status":
        result = chat.get_stats()
        emit("message_chat", (result, roomid), broadcast=True)
    elif commands.get('v0') == "lock":
        lock(user, roomid)
    elif commands.get('v0') == "unlock":
        unlock(user, roomid)
    elif commands.get('v0') in ("ronline", "ro"):
        reload_users()
    elif commands.get('v0') in ("clear", 'rc'):
        if check_if_dev(user) == 1 or check_if_mod(user) == 1:
            chat.reset_chat(False, True, roomid)
        else:
            respond_command(("reason", 2, "not_mod"), roomid, None)
    elif commands.get('v0') == "shutdown":
        if check_if_dev(user) == 1:
            run_shutdown()
        else:
            respond_command(("reason", 2, "not_dev"), roomid, None)
    elif commands.get('v0') in ("lines", "pstats"):
        send_lines(roomid, dbm)
    elif commands.get('v0') == "system":
        message = ' '.join(list(commands.values())[1:])
        send_system(roomid, user, message)
    elif commands.get('v0') == "song":
        message = ' '.join(list(commands.values())[1:])
        send_song(roomid, user, message)
    elif commands.get('v0') == "jotd":
        message = ' '.join(list(commands.values())[1:])
        send_joke(roomid, user, message)
    elif commands.get('v0') in ("permlist", "banned", "muted"):
        send_perms(roomid, user)
    else:
        result = ("reason", 1, None)
        respond_command(result, roomid, None)


def check_if_dev(user):
    """Return if a user is a dev or not."""
    return 1 if user['SPermission'] == 'Debugpass' else 0


def check_if_mod(user):
    """Return if a user is a mod or not."""
    return 1 if user['SPermission'] == 'modpass' else 0


def ban_user(username: str, issuer, reason, roomid):
    """Ban a user from the chat forever."""
    is_dev = check_if_dev(issuer)
    if is_dev != 1:
        respond_command(("reason", 2, "not_dev"), roomid, None)
        return

    user = dbm.Accounts.find_one({"displayName": username})
    if user['permission'] == 'banned':
        return

    dbm.Accounts.update_one({"displayName": username},
                            {"$set": {
                                "permission": "banned"
                            }})
    if reason == '':
        message = '[SYSTEM]: <font color="#ff7f00">' + username + " has been banned.</font>"
    else:
        message = '[SYSTEM]: <font color="#ff7f00">' + username + " has been banned. Reason: " + reason + "." + "</font>"

    chat.add_message(message, roomid, 'true')
    emit("message_chat", (message, roomid), broadcast=True)


def mute_user(username: str, issuer, time, reason, roomid):
    """Mute a user from the chat."""
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

            chat.add_message(message, roomid, 'true')
            emit("message_chat", message, broadcast=True)
    else:
        respond_command(("reason", 2, "not_mod"), roomid, None)


def unmute_user(username: str, issuer, roomid):
    """Unmute a user from the chat"""
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

            chat.add_message(message, roomid, 'true')
            emit("message_chat", message, broadcast=True)
    else:
        respond_command(("reason", 2, "not_mod"), roomid, None)


def send_perms(roomid, issuer):
    """Return the list of people banned, and currently muted."""
    if check_if_dev(issuer) == 1 or check_if_mod(issuer) == 1:
        room = dbm.rooms.find_one({"roomid": roomid})
        banned = dbm.Accounts.find({"permission": "banned"})
        muted = dbm.Accounts.find({"permission": "muted"})
        msg_str = "Currently Banned/Muted Users:<br>Banned:<br>"
        for user in banned:
            msg_str = msg_str + f"{user['displayName']}<br>"
        msg_str = msg_str + '<br>Muted:<br>'
        for user in muted:
            msg_str = msg_str + f"{user['displayName']}<br>"

        # trying something new here, wonder if it will work
        # if it does, we need to redo a lot of these statements like this (make it clean)
        final_msg = f"[SYSTEM]: <font color='#ff7f00'>{msg_str}</font>"
        chat.add_message(final_msg, roomid, room)
        emit("message_chat", (final_msg, roomid), broadcast=True)
    else:
        respond_command(("reason", 2, "not_mod"), roomid, None)


# why is this here
def handle_admin_message(message, roomid):
    """Bypass message filtering, used when chat is locked."""
    chat.add_message(message, roomid, 'true')
    emit("message_chat", message, broadcast=True, namespace="/")


def send_joke(roomid, user, message):  #add a check for a user later
    """Sends as joke of the day."""
    room = dbm.rooms.find_one({"roomid": roomid})
    final_msg = f"[Joke of the day]: <font color='#D51956'>{message}</font>"
    chat.add_message(final_msg, roomid, room)
    emit("message_chat", (final_msg, roomid), broadcast=True)


def send_song(roomid, user, message):  #add a check for a user later
    """Sends as song."""
    room = dbm.rooms.find_one({"roomid": roomid})
    final_msg = f"<font color='#08bd71'>[SONG]: {message}</font>"
    chat.add_message(final_msg, roomid, room)
    emit("message_chat", (final_msg, roomid), broadcast=True)


def send_system(roomid, user, message):  #add a check for a user later
    """Sends as the server for specal dev messages"""
    room = dbm.rooms.find_one({"roomid": roomid})
    final_msg = f"[SYSTEM]: <font color='#ff7f00'>{message}</font>"
    chat.add_message(final_msg, roomid, room)
    emit("message_chat", (final_msg, roomid), broadcast=True)


def run_shutdown():
    """Stop the server, but also tell everyone that the server is going down."""
    emit(
        "message_chat",
        "[SYSTEM]: <font color='#ff7f00'>Server going down in 2 Seconds (unknown ETA on restart)</font>",
        broadcast=True,
        namespace='/')
    sleep(2)
    os.system('pkill gunicorn')


def reload_users():
    """Reload the online list manually."""
    dbm.Online.delete_many({})
    emit("force_username", "", broadcast=True)


def send_lines(roomid, dbm):
    """Respond with the current line count for the room (TBD)"""
    # to rework this so it uses add_message
    lines = chat.get_line_count("main")
    msg = f"[SYSTEM]: <font color='#ff7f00'>Line count is {lines}</font>\n"
    chat.add_message(msg, roomid, dbm)
    emit("message_chat", (msg, roomid), broadcast=True, namespace="/")


def respond_command(result, roomid, name):
    """Tell the client that can't run this command for what reason."""
    room = dbm.rooms.find_one({"roomName": name})
    generatedBy = room["generatedBy"] if room is not None else ""
    generatedAt = room["generatedAt"] if room is not None else ""
    locked = room["locked"] if room is not None else ""
    usersW = room["whitelisted"] if room is not None else ""
    usersB = room["blacklisted"] if room is not None else ""

    response_strings = {
        (1, None):
        "[SYSTEM]: <font color='#ff7f00'>Command not found. Use \"$sudo help\" to see all commands.</font>",
        (0, 'delete'):
        "[SYSTEM]: <font color='#ff7f00'>Chat room deleted.</font>",
        (1, 'delete'):
        f"[SYSTEM]: <font color='#ff7f00'>You are not allowed to delete the chat room named {name}.</font>",
        (2, 'delete'):
        "[SYSTEM]: <font color='#ff7f00'>Just because you are a dev doesn't mean you can delete the main chat.</font>",
        (3, 'delete'):
        "[SYSTEM]: <font color='#ff7f00'>Nice try, but we were prepared.</font>",
        (0, 'create'):
        f"[SYSTEM]: <font color='#ff7f00'>Created chat room named {name}.</font>",
        (1, 'create'):
        f"[SYSTEM]: <font color='#ff7f00'>Your chat name ({name}) is too long. It must be 10 letters or less.</font>",
        (2, 'create'):
        "[SYSTEM]: <font color='#ff7f00'>You are not allowed to create more chat rooms.</font>",
        (3, 'create'):
        "[SYSTEM]: <font color='#ff7f00'>Your chat room must have a name at least 1 letter long.</font>",
        (4, 'create'):
        f"[SYSTEM]: <font color='#ff7f00'>The name {name} has been taken. Pick another name besides {name}.</font>",
        (0, 'edit'):
        f"[SYSTEM]: <font color='#ff7f00'>You have edited the chat room named {name} to whitelist the users {usersW}.</font>",
        (1, 'edit'):
        f"[SYSTEM]: <font color='#ff7f00'>You are not allowed to edit the chat room named {name}.</font>",
        (2, 'edit'):
        f"[SYSTEM]: <font color='#ff7f00'>You have edited the chat room named {name} to blacklist the users {usersB}.</font>",
        (3, 'edit'):
        "[SYSTEM]: <font color='#ff7f00'>.</font>",
        (4, 'edit'):
        "[SYSTEM]: <font color='#ff7f00'>.</font>",
        (0, 'info'):
        f"[SYSTEM]: <font color='#ff7f00'>The chat room {name} was made by {generatedBy} at {generatedAt} and the chat room status is currently set to locked = {locked}.</font>",
        (0, 'rooms'):
        f"[SYSTEM]: <font color='#ff7f00'>The chat room {name} does not exist. Please enter a chat room that does exist.</font>",
        (2, 'not_dev'):
        "[SYSTEM]: <font color='#ff7f00'>Who do you think you are, a Developer?</font>",
        (2, 'not_mod'):
        "[SYSTEM]: <font color='#ff7f00'>Who do you think you are, a Moderator?</font>",
    }
    response_str = response_strings.get((result[1], result[2]))
    if result[1] in [0, 2, 3] and result[2] in ['create', 'delete', 'edit']:
        chat.add_message(response_str, roomid, 'true')
        emit("message_chat", (response_str, roomid), namespace="/")
    else:
        emit("message_chat", (response_str, roomid), namespace="/")


def help_command(issuer, roomid):
    """sends a message with a file full of commands that the user can use."""
    with open('backend/command_list.txt', 'r') as file:
        lines = file.readlines()
    start_index = None
    end_index = None

    if check_if_dev(issuer) == 1:
        for i, line in enumerate(lines):
            if 'dev' in line.lower():
                start_index = i
            elif 'end' in line.lower():
                end_index = i - 1
    elif check_if_mod(issuer) == 1:
        for i, line in enumerate(lines):
            if 'mod' in line.lower():
                start_index = i
            elif 'end' in line.lower():
                end_index = i - 1
    else:
        for i, line in enumerate(lines):
            if 'no permission requirement' in line.lower():
                start_index = i
            elif 'end' in line.lower():
                end_index = i - 1

    command_line = "[SYSTEM]:<font color='#ff7f00'><br>" + ' '.join(
        line.strip() for line in lines[start_index:end_index + 1]) + "</font>"
    emit("message_chat", (command_line, roomid), namespace="/")


def lock(user, roomid):
    """locks the chat so that only devs can send"""
    if check_if_dev(user) == 1:
        message = "[SYSTEM]: <font color='#ff7f00'>Chat Locked by Admin.</font>"
        chat.add_message(message, roomid, dbm)
        emit("message_chat", message, broadcast=True)
        dbm.rooms.update_one({"roomid": roomid}, {'$set': {"locked": 'true'}})
    elif check_if_mod(user) == 1:
        message = "[SYSTEM]: <font color='#ff7f00'>Chat Locked by Moderator.</font>"
        chat.add_message(message, roomid, dbm)
        emit("message_chat", message, broadcast=True)
        dbm.rooms.update_one({"roomid": roomid}, {'$set': {"locked": 'true'}})
    else:
        respond_command(("reason", 2, "not_mod"), roomid, None)


def unlock(user, roomid):
    """unlocks the chat so that everyone can send"""
    if check_if_dev(user) == 1:
        message = "[SYSTEM]: <font color='#ff7f00'>Chat Unlocked by Admin.</font>"
        chat.add_message(message, roomid, dbm)
        emit("message_chat", message, broadcast=True)
        dbm.rooms.update_one({"roomid": roomid}, {'$set': {"locked": 'false'}})
    elif check_if_mod(user) == 1:
        message = "[SYSTEM]: <font color='#ff7f00'>Chat Unlocked by Moderator.</font>"
        chat.add_message(message, roomid, dbm)
        emit("message_chat", message, broadcast=True)
        dbm.rooms.update_one({"roomid": roomid}, {'$set': {"locked": 'false'}})
    else:
        respond_command(("reason", 2, "not_mod"), roomid, None)


def chat_room_edit(commands, roomid, user):
    """checks what chat command the user wants to run then sends it to the room file."""
    room_name = commands.get('v1', '')
    command = commands.get('v2', '')
    room = dbm.rooms.find_one({"roomName": room_name})
    print(room)

    if command not in ['create', 'test'] and room is None:
        command = ''
        respond_command(('reason', 0, 'rooms'), roomid, room_name)

    if command == 'delete':
        response = rooms.delete_chat_room(room_name, user)
        respond_command(response, roomid, room_name)
    elif command == "create":
        response = rooms.create_rooms(room_name, user, user["displayName"])
        respond_command(response, roomid, room_name)
    elif command in ["whitelist", "blacklist"]:
        users = ','.join(list(commands.values())[3:])
        response = rooms.chat_room_edit(command, room_name, user, users)
        respond_command(response, roomid, room_name)
    elif command == "info":
        response = ('reason', 0, 'info')
        respond_command(response, roomid, room_name)
