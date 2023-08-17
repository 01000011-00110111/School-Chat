"""All commands ran by devs, mods, users, etc.
    Copyright (C) 2023  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
import chat
from main import dbm, scheduler
from flask_socketio import emit
import time
from time import sleep
import os
import re
from datetime import datetime, timedelta
import rooms


def log_commands(message):
    """Log when a command is issued."""
    with open('backend/command_log.txt', 'a', encoding="utf8") as file:
        file.write(message + '\n')


def log_mutes(message):
    """Log when a unmuted user is issued."""
    with open('backend/permission.txt', 'a', encoding="utf8") as file:
        file.write(message + '\n')


def find_command(**kwargs):
    """Send whatever sudo command is issued to its respective function."""
    response_strings = {
        'E': E,
        'help': help_command,
        'chat': chat_room_edit,
        'mute': mute_user,
        'unmute': unmute_user,
        'ban': ban_user,
        'blanks': chat.line_blanks,
        'status': send_stats,
        'lock': lock,
        'unlock': unlock,
        'golballock': globalock,
        'ronline': reload_users,
        'ro': reload_users,
        'clear': reset_chat_user,
        'rc': reset_chat_user,
        'shutdown': run_shutdown,
        'restart': run_restart,
        'lines': send_lines,
        'pstats': send_lines,
        'system': send_system,
        'song': send_song,
        'jotd': send_joke,
        'permlist': send_perms,
        'roomlist': list_rooms,
        'banned': send_perms,
        'muted': send_perms,
        'ping': ping,
        'restart': run_restart
    }
    try:
        response_strings[kwargs['commands']['v0']](**kwargs)
    except KeyError:
        respond_command(("result", 1, None), kwargs['roomid'], None)


def E(**kwargs):
    """Test function"""
    roomid = kwargs['roomid']
    emit("troll", (
        "[SYSTEM]: <font color='#ff7f00'>YOUVE BEEN TROLOLOLOLLED</font> <img src='static/troll-face.jpeg'>",
        roomid),
         broadcast=True)


def send_stats(**kwargs):
    roomid = kwargs['roomid']
    emit("message_chat", (chat.get_stats(roomid), roomid), broadcast=True)


def check_if_dev(user):
    """Return if a user is a dev or not."""
    return 1 if user['SPermission'] == 'Debugpass' else 0


def check_if_mod(user):
    """Return if a user is a mod or not."""
    return 1 if user['SPermission'] == 'modpass' else 0


def reset_chat_user(**kwargs):
    user = kwargs['user']
    roomid = kwargs['roomid']
    if check_if_dev(user) == 1 or check_if_mod(user) == 1:
        chat.reset_chat(False, True, roomid)
    else:
        respond_command(("reason", 2, "not_mod"), roomid, None)


def ban_user(**kwargs):
    """Ban a user from the chat forever."""
    username = kwargs['commands']['v1']
    reason = ' '.join(list(kwargs['commands'].values())[2:])
    roomid = kwargs['roomid']
    user = kwargs['user']
    if check_if_dev(user) != 1:
        respond_command(("reason", 2, "not_dev"), roomid, None)
        return

    user_dbm = dbm.Accounts.find_one({"displayName": username})
    if user_dbm['permission'] == 'banned':
        return

    dbm.Accounts.update_one({"displayName": username},
                            {"$set": {
                                "permission": "banned"
                            }})
    if reason == '':
        message = f'[SYSTEM]: <font color="#ff7f00">{username} has been banned.</font>'
        log_mutes(f"{username} is banned by a mod or admin.")
    else:
        message = f'[SYSTEM]: <font color="#ff7f00"> {username} has been banned. Reason: {reason}.</font>'
        log_mutes(f"{username} is banned because {reason} by a mod or admin.")

    chat.add_message(message, roomid, 'true')
    emit("message_chat", (message, roomid), broadcast=True)


def mute_user(**kwargs):
    """Mute a user from the chat."""
    roomid = kwargs['roomid']
    username = kwargs['commands']['v1']
    try:
        time = kwargs['commands']['v2']
    except KeyError:
        respond_command(("reason", 1, "no_time"), roomid, None)
        return
    reason = ' '.join(list(kwargs['commands'].values())[3:])
    issuer = kwargs['user']
    if check_if_dev(issuer) == 1 or check_if_mod(issuer) == 1:
        user_dbm = dbm.Accounts.find_one({"displayName": username})
        if user_dbm['permission'] in ('banned', 'muted'):
            return
        else:
            time_match = re.match(r'^(\d+)([dhm])$', time)
            if time_match:
                permission_str = "muted"
                time_final = None
                time_number = int(time_match.group(1))
                time_letter = time_match.group(2)
                current_time = datetime.now()

                if time_letter == 'd':
                    time_final = f"{time_number} days"
                    expiration_time = current_time + timedelta(
                        days=time_number)
                elif time_letter == 'h':
                    time_final = f"{time_number} hours"
                    expiration_time = current_time + timedelta(
                        hours=time_number)
                elif time_letter == 'm':
                    time_final = f"{time_number} minutes"
                    expiration_time = current_time + timedelta(
                        minutes=time_number)
                elif time_letter == 'f':
                    time_final = None

                if time_letter != 'f':
                    expiration_time_str = expiration_time.strftime(
                        "%Y-%m-%d %H:%M:%S")
                    permission_str = f"muted {expiration_time_str}"

                dbm.Accounts.update_one(
                    {"displayName": username},
                    {"$set": {
                        "permission": permission_str
                    }})

            if reason == '' and time_final is None:
                message = f'[SYSTEM]: <font color="#ff7f00">{username} is muted for an undefined period of time.</font>'
                log_mutes(f"{username} is muted by a mod or admin.")
            elif time_final is None:
                message = f'[SYSTEM]: <font color="#ff7f00">{username} is muted for an undefined period of time. Reason: {reason}.</font>'
                log_mutes(
                    f"{username} is muted because {reason} by a mod or admin.")
            elif reason == '':
                message = f'[SYSTEM]: <font color="#ff7f00">{username} is mutted for {time_final}.</font>'
                log_mutes(
                    f"{username} is muted for {time_final} by a mod or admin.")
            else:
                message = f'[SYSTEM]: <font color="#ff7f00">{username} is mutted for {time_final}. Reason: {reason}.</font>'
                log_mutes(
                    f"{username} is muted because {reason} for {time_final} by a mod or admin."
                )

                chat.add_message(message, roomid, 'true')
                emit("message_chat", (message, roomid), broadcast=True)
    else:
        respond_command(("reason", 2, "not_mod"), roomid, None)


def unmute_user(**kwargs):
    """Unmute a user from the chat"""
    username = kwargs['commands']['v1']
    issuer = kwargs['user']
    roomid = kwargs['roomid']
    if check_if_dev(issuer) == 1 or check_if_mod(issuer) == 1:
        user = dbm.Accounts.find_one({"displayName": username})
        if user['permission'] in ('banned', 'true'):
            return
        else:
            dbm.Accounts.update_one({"displayName": username},
                                    {"$set": {
                                        "permission": "true"
                                    }})
            message = f'[SYSTEM]: <font color="#ff7f00">{username} has been unmuted.</font>'

            log_mutes(f"{username} is unmuted by a mod or admin.")
            chat.add_message(message, roomid, 'true')
            emit("message_chat", (message, roomid), broadcast=True)
    else:
        respond_command(("reason", 2, "not_mod"), roomid, None)


def send_perms(**kwargs):
    """Return the list of people banned, and currently muted."""
    issuer = kwargs['user']
    roomid = kwargs['roomid']
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


def list_rooms(**kwargs):
    """list all the chat rooms names and roomids to devs only"""
    issuer = kwargs['user']
    roomid = kwargs["roomid"]
    origin_room = kwargs['origin_room']

    if check_if_dev(issuer) == 1 and origin_room == 'jN7Ht3giH9EDBvpvnqRB':
        ids = [room["roomid"] for room in dbm.rooms.find({}, {"roomid": 1})]
        names = [
            room["roomName"] for room in dbm.rooms.find({}, {"roomName": 1})
        ]
        msg_str = '<br>'.join([
            f"Room's name: ({name}) Room's id: ({id})"
            for id, name in zip(ids, names)
        ])
        chat.add_message(
            f"[SYSTEM]: <font color='#ff7f00'><br>{msg_str}</font>",
            'jN7Ht3giH9EDBvpvnqRB', 'true')
        emit("message_chat",
             (f"[SYSTEM]: <font color='#ff7f00'><br>{msg_str}</font>",
              'jN7Ht3giH9EDBvpvnqRB'),
             namespace="/")
    else:
        if check_if_dev(issuer) != 1:
            respond_command(("reason", 2, "not_dev"), 'jN7Ht3giH9EDBvpvnqRB',
                            None)
        else:
            respond_command(("reason", 1, "wrong_room"), roomid, None)


def send_joke(**kwargs):  #add a check for a user later
    """Sends as joke of the day."""
    user = kwargs['user']
    roomid = kwargs['roomid']
    commands = kwargs['commands']
    message = ' '.join(list(commands.values())[1:])
    room = dbm.rooms.find_one({"roomid": roomid})
    final_msg = f"[Joke of the day]: <font color='#D51956'>{message}</font>"
    chat.add_message(final_msg, roomid, room)
    emit("message_chat", (final_msg, roomid), broadcast=True)


def send_song(**kwargs):  #add a check for a user later
    """Sends as song."""
    user = kwargs['user']
    roomid = kwargs['roomid']
    commands = kwargs['commands']
    message = ' '.join(list(commands.values())[1:])
    room = dbm.rooms.find_one({"roomid": roomid})
    final_msg = f"<font color='#08bd71'>[SONG]: {message}</font>"
    chat.add_message(final_msg, roomid, room)
    emit("message_chat", (final_msg, roomid), broadcast=True)


def send_system(**kwargs):  #add a check for a user later
    """Sends as the server for specal dev messages"""
    user = kwargs['user']
    roomid = kwargs['roomid']
    commands = kwargs['commands']
    message = ' '.join(list(commands.values())[1:])
    room = dbm.rooms.find_one({"roomid": roomid})
    final_msg = f"[SYSTEM]: <font color='#ff7f00'>{message}</font>"
    chat.add_message(final_msg, roomid, room)
    emit("message_chat", (final_msg, roomid), broadcast=True)


def run_shutdown(**kwargs):
    user = kwargs['user']
    roomid = kwargs['roomid']
    """Stop the server, but also tell everyone that the server is going down."""
    if check_if_dev(user) == 1:
        emit("message_chat", (
            "[SYSTEM]: <font color='#ff7f00'>Server shutting down... (unknown ETA on restart)</font>",
            roomid),
             broadcast=True,
             namespace='/')
        sleep(2)
        scheduler.shutdown()
        # replace with systemd methoud
        sysbus = dbus.SystemBus()
        systemd1 = sysbus.get_object('org.freedesktop.systemd1',
                                     '/org/freedesktop/systemd1')
        manager = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')
        job = manager.StopUnit('chatserverd.service', 'fail')
    else:
        respond_command(("reason", 2, "not_dev"), roomid, None)


def run_restart(**kwargs):
    user = kwargs['user']
    roomid = kwargs['roomid']
    """Restart the server, but also tell everyone that the server is going down."""
    if check_if_dev(user) == 1:
        # later, implement this so it sends it to EVERY room that the server is going down, not just the one that the cmd is sent in...
        # could make it modular (for anouncments? maybe idk)
        emit("message_chat", (
            "[SYSTEM]: <font color='#ff7f00'>Server restarting... (~30sec ETA on restart)</font>",
            roomid),
             broadcast=True,
             namespace='/')
        sleep(2)
        scheduler.shutdown()
        sysbus = dbus.SystemBus()
        systemd1 = sysbus.get_object('org.freedesktop.systemd1',
                                     '/org/freedesktop/systemd1')
        manager = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')
        job = manager.RestartUnit('chatserverd.service', 'fail')
    else:
        respond_command(("reason", 2, "not_dev"), roomid, None)


def reload_users(**kwargs):
    """Reload the online list manually."""
    dbm.Online.delete_many({})
    emit("force_username", "", broadcast=True)


def ping(**kwargs):
    """EEEEEEEEEEEEEEEE"""
    roomid = kwargs['roomid']
    start = time.time() * 1000.0
    emit("pingTime", (start, roomid), namespace="/")


def end_ping(start, roomid):
    """The end of the ping comamnd."""
    end = time.time() * 1000.0
    difference = end - start
    msg = '[SYSTEM]: <font color="#ff7f00">Ping Time: ' + str(
        int(difference)) + 'ms RTT</font>'
    chat.add_message(msg, roomid, dbm)
    emit("message_chat", (msg, roomid), broadcast=True, namespace="/")


def send_lines(**kwargs):
    """Respond with the current line count for the room (TBD)"""
    # to rework this so it uses add_message
    roomid = kwargs['roomid']
    lines = chat.get_line_count("main", roomid)
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
        "[SYSTEM]: <font color='#ff7f00'>You can not blacklist a user that is whitlisted.</font>",
        (4, 'edit'):
        "[SYSTEM]: <font color='#ff7f00'>You can not whitlisted a user that is blacklisted.</font>",
        (0, 'info'):
        f"[SYSTEM]: <font color='#ff7f00'>The chat room {name} was made by {generatedBy} at {generatedAt} and the chat room status is currently set to locked = {locked}.</font>",
        (0, 'rooms'):
        f"[SYSTEM]: <font color='#ff7f00'>The chat room {name} does not exist. Please enter a chat room that does exist.</font>",
        (2, 'not_dev'):
        "[SYSTEM]: <font color='#ff7f00'>Who do you think you are, a Developer?</font>",
        (2, 'not_mod'):
        "[SYSTEM]: <font color='#ff7f00'>Who do you think you are, a Moderator?</font>",
        (1, 'no_time'):
        "[SYSTEM]: <font color='#ff7f00'>You forgot the time!</font>",
        (1, 'wrong_room'):
        "[SYSTEM]: <font color='#ff7f00'>You can only run this command in the dev chat room</font>",
        (1, "not_confirmed"):
        "[SYSTEM]: <font color='#ff7f00'>Are you sure you want to run this?</font>",
    }
    response_str = response_strings.get((result[1], result[2]))
    if result[1] in [0, 2, 3] and result[2] in ['create', 'delete', 'edit']:
        chat.add_message(response_str, roomid, 'true')
        emit("message_chat", (response_str, roomid), namespace="/")
    else:
        emit("message_chat", (response_str, roomid), namespace="/")


def help_command(**kwargs):
    """sends a message with a file full of commands that the user can use."""
    roomid = kwargs['roomid']
    issuer = kwargs['user']
    with open('backend/command_list.txt', 'r') as file:
        lines = file.readlines()
    start_index = None
    end_index = None

    if check_if_dev(issuer) == 1:
        for i, line in enumerate(lines):
            if 'dev commands' in line.lower():
                start_index = i
            elif 'end' in line.lower():
                end_index = i - 1
    elif check_if_mod(issuer) == 1:
        for i, line in enumerate(lines):
            if 'mod commands' in line.lower():
                start_index = i
            elif 'end' in line.lower():
                end_index = i - 1
    else:
        for i, line in enumerate(lines):
            if 'user commands' in line.lower():
                start_index = i
            elif 'end' in line.lower():
                end_index = i - 1

    command_line = "[SYSTEM]:<font color='#ff7f00'><br>" + ' '.join(
        line.strip() for line in lines[start_index:end_index + 1]) + "</font>"
    emit("message_chat", (command_line, roomid), namespace="/")


def globalock(**kwargs):
    """Locks all chatrooms, only used in emergencies."""
    user = kwargs['user']
    roomid = kwargs['roomid']
    confirm = kwargs['commands']['v1']
    if check_if_dev(user) != 1:
        respond_command(("reason", 2, "not_dev"), roomid, None)
        return

    if confirm != "yes":
        respond_command(("reason", 1, "not_confirmed"), roomid, None)
    else:
        message = "[SYSTEM]: <font color='#ff7f00'>All Chatrooms locked by Admin.</font>"
        chat.add_message(message, "all", dbm)
        emit("message_chat", (message, "all"), broadcast=True)
        dbm.rooms.update_many({}, {'$set': {"locked": 'true'}})


def lock(**kwargs):
    """locks the chat so that only devs can send"""
    user = kwargs['user']
    roomid = kwargs['roomid']
    if check_if_dev(user) == 1:
        message = "[SYSTEM]: <font color='#ff7f00'>Chat Locked by Admin.</font>"
        chat.add_message(message, roomid, dbm)
        emit("message_chat", (message, roomid), broadcast=True)
        dbm.rooms.update_one({"roomid": roomid}, {'$set': {"locked": 'true'}})
    elif check_if_mod(user) == 1:
        message = "[SYSTEM]: <font color='#ff7f00'>Chat Locked by Moderator.</font>"
        chat.add_message(message, roomid, dbm)
        emit("message_chat", (message, roomid), broadcast=True)
        dbm.rooms.update_one({"roomid": roomid}, {'$set': {"locked": 'true'}})
    else:
        respond_command(("reason", 2, "not_mod"), roomid, None)


def unlock(**kwargs):
    """unlocks the chat so that everyone can send"""
    user = kwargs['user']
    roomid = kwargs['roomid']
    if check_if_dev(user) == 1:
        message = "[SYSTEM]: <font color='#ff7f00'>Chat Unlocked by Admin.</font>"
        chat.add_message(message, roomid, dbm)
        emit("message_chat", (message, roomid), broadcast=True)
        dbm.rooms.update_one({"roomid": roomid}, {'$set': {"locked": 'false'}})
    elif check_if_mod(user) == 1:
        message = "[SYSTEM]: <font color='#ff7f00'>Chat Unlocked by Moderator.</font>"
        chat.add_message(message, roomid, dbm)
        emit("message_chat", (message, roomid), broadcast=True)
        dbm.rooms.update_one({"roomid": roomid}, {'$set': {"locked": 'false'}})
    else:
        respond_command(("reason", 2, "not_mod"), roomid, None)


def chat_room_edit(**kwargs):
    """checks what chat command the user wants to run then sends it to the room file."""
    user = kwargs['user']
    roomid = kwargs['roomid']
    commands = kwargs['commands']
    room_name = commands.get('v1', '')
    command = commands.get('v2', '')
    function = commands.get('v3', '')
    room = dbm.rooms.find_one({"roomName": room_name})
    # print(command, room_name, function)

    if command not in ['create', 'test'] and room is None:
        command = ''
        respond_command(('reason', 0, 'rooms'), roomid, room_name)

    if command == 'delete' and function == '':
        response = rooms.delete_chat_room(room_name, user)
        respond_command(response, roomid, room_name)
    elif command == "create" and function == '':
        response = rooms.create_rooms(room_name, user, user["displayName"])
        respond_command(response, roomid, room_name)
    elif command in ["whitelist", "blacklist"]:
        users = ','.join(list(commands.values())[4:])
        response = rooms.chat_room_edit(command, function, room_name, user,
                                        users)
        respond_command(response, roomid, room_name)
    elif command == "info" and function == '':
        response = ('reason', 0, 'info')
        respond_command(response, roomid, room_name)
    else:
        print('add a failed response')


def warn_user(user):
    """adds a new warning to the user"""
    warn_count = user["warned"]
    current_time = datetime.now()
    expiration_time = current_time + timedelta(days=30)
    date = expiration_time.strftime("%Y-%m-%d %H:%M:%S")
    warn_updated = int(warn_count) + 1
    dbm.Accounts.update_one(
        {"username": user["username"]},
        {'$set': {
            'warned': f"{str(warn_updated)} {date}"
        }})