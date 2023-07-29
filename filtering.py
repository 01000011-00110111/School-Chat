"""Filter usernames and make the chat more xss safe.
    Copyright (C) 2023  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
import re
from datetime import datetime, timezone, timedelta
from better_profanity import profanity
from flask_socketio import emit
import chat
import profanity_words
import cmds
import rooms

# get our custom whitelist words (that shouldnot be banned in the first place)
profanity.load_censor_words(whitelist_words=profanity_words.whitelist_words)
profanity.add_censor_words(profanity_words.censored)


def run_filter(user, room, message, roomid):
    """Its simple now, but when chat rooms come this will be more convoluted."""
    locked = check_lock(room)
    perms = check_perms(user)
    can_send = check_allowed_sending(user, room)
    user_muted = check_mute(user)

    if user_muted != 0 and perms != 'dev':
        return ('permission', user_muted)

    if perms != "dev":
        message = filter_message(message)
        role = profanity.censor(user['role'])
    else:
        role = user['role']

    if user['profile'] == "":
        profile_picture = 'static/favicon.ico'
    else:
        profile_picture = user['profile']

    if "[" in message:
        find_pings(message, user['displayName'], profile_picture)

    final_str = compile_message(message, profile_picture, user, role)

    if perms == "dev":
        chat.add_message(final_str, roomid, 'true')
        emit("message_chat", (final_str, roomid),
             broadcast=True,
             namespace="/")
        if "$sudo" in message:
            find_cmds(message, user, roomid)
        return ('dev', 0)

    if locked == 'true':
        return ("permission", 3)

    if can_send == "everyone":
        return ('msg', final_str)
    elif can_send == 'mod':
        if perms == 'mod':
            return ('msg', final_str)
        else:
            return ('permission', 5)
    else:
        return ('permission', 5)

    return ('msg', final_str)


def check_mute(user):
    """checks if the user is muted or banned."""
    permission = user["permission"].split(' ')
    if permission[0] == "muted":
        return 1
    elif user["permission"] == "banned":
        return 2
    return 0


def check_lock(room):
    """For now, its just as simple as this, but when rooms come it will be more complicated."""
    return (room["locked"])


def check_allowed_sending(user, room):
    """this is a check to se if the database allowes you to send"""  # we can make this more advanced if we want
    return (room["canSend"])


def check_perms(user):
    """checks if the user has specal perms else return as a user"""
    if user['SPermission'] == 'Debugpass':
        perms = 'dev'
    elif user['SPermission'] == 'modpass':
        perms = 'mod'
    else:
        perms = 'user'
    return perms


def to_hyperlink(text):
    """Taken from the js file, we don't need to have the client process it really."""
    mails = re.findall(r"mailto:([^\?]*)", text)
    links2 = re.findall(r"(^|[^\/])(www\.[\S]+(\b|$))", text)
    #print(f"{mails}\n\n\n{links2}")


def filter_message(message):
    """No one likes profanity, especially flagging systems."""
    return profanity.censor(message)


def find_pings(message, dispName, profile_picture):
    """Gotta catch 'em all! (checks for pings in the users message)"""
    pings = re.findall(r'(?<=\[).+?(?=\])', message)
    for ping in pings:
        emit("ping", {
            "who": ping,
            "from": dispName,
            "pfp": profile_picture,
            "message": message
        },
             namespace="/",
             broadcast=True)


def find_cmds(message, user, roomid):
    """$sudo commands, will push every cmd found to cmds.py along with the user, so we can check if they can do said command."""
    command_split = message.split("$sudo")
    command_split.pop(0)
    command_string = command_split[0]
    perms = check_perms(user)
    origin_room = None
    match = re.findall(r"\(|\)", command_string)

    if perms == 'dev' and roomid == 'jN7Ht3giH9EDBvpvnqRB' and match != []:
        match_msg = re.findall(r"\((.*?)\)", command_string)
        find_roomid = re.sub(r"\([^()]+\)", "", command_string).strip()
        room_check = rooms.check_roomids(find_roomid)
        if room_check is False:
            failed_message(('permission', 7), roomid)
            return
        if len(match) == 2:
            origin_room = roomid
            roomid = find_roomid
            command_split = [match_msg[0]]

    if origin_room is None: origin_room = roomid
    # this check is needed, because the finding of commands is after chat lock check in run_filter
    # leading to users being able to send comamnds, even when chat is locked
    # we should be the only ones that can do that (devs)
    for cmd in command_split:
        date_str = datetime.now(timezone(
            timedelta(hours=-4))).strftime("[%a %H:%M] ")
        Lmessage = date_str + user['username'] + ":" + cmd
        cmds.log_commands(Lmessage)

        command = cmd.split()
        commands = {}

        for index, command in enumerate(command):
            var_name = "v%d" % index
            commands[var_name] = command
        if 'v0' in commands:
            cmds.find_command(commands=commands,
                              user=user,
                              roomid=roomid,
                              origin_room=origin_room)


def compile_message(message, profile_picture, user, role):
    """Taken from old methold of making messages"""
    to_hyperlink(message)
    profile = "<img class='pfp' src='" + profile_picture + "'></img>"
    user_string = "<font color='" + user['userColor'] + "'>" + user[
        'displayName'] + "</font>"
    message_string = "<font color='" + user[
        'messageColor'] + "'>" + message + "</font>"
    role_string = do_dev_easter_egg(role, user)
    date_str = datetime.now(timezone(
        timedelta(hours=-4))).strftime("[%a %I:%M %p] ")

    # because accounts will now be required, we don't need the check if a role exists for the user
    message = date_str + profile + " " + user_string + " (" + role_string + ")" + " - " + message_string
    return message


def do_dev_easter_egg(role, user):
    """Because we want RAINBOW changing role names."""
    role_color = user['roleColor']
    if role_color == "#00ff00":
        role_string = "<font class='Dev_colors-loop'>" + role + "</font>"
    elif role_color == "#3262a8":
        role_string = "<font class='ow_colors-loop'>" + role + "</font>"
    else:
        role_string = "<font color='" + role_color + "'>" + role + "</font>"
    return role_string


def failed_message(result, roomid):
    """Tell the client that your message could not be sent for whatever the reason was."""
    fail_strings = {
        (1):
        "[SYSTEM]: <font color='#ff7f00'>You can't send messages because you are muted.</font>",
        (2):
        "[SYSTEM]: <font color='#ff7f00'>You can't send messages because you have been banned.</font>",
        (3):
        "[SYSTEM]: <font color='#ff7f00'>You can't send messages because this chat room has been locked.</font>",
        (4):
        "[SYSTEM]: <font color='#ff7f00'>You can't send messages because you have been banned from this chat room.</font>",
        (5):
        "[SYSTEM]: <font color='#ff7f00'>You can't send messages because you do not have enough permission to use this chat room.</font>",
        (6):
        "[SYSTEM]: <font color='#ff7f00'>You can't send messages in this chat room because this chat room no longer exists,  select a chat room that does exist.</font>",
        (7): "this chat room id does not exists"
    }
    if result[0] == "dev":
        if result[1] == 6: fail_str = fail_strings.get((result[1]), "")
        else: return
    # if result[0] == "return": emit("message_chat", ('', roomid), namespace="/") what is this

    fail_str = fail_strings.get((result[1]), "")  # result[2]), "")
    emit("message_chat", (fail_str, roomid), namespace="/")


def is_user_expired(permission_str):
    """checks if the user's time maches the time (idk you explain it better to me please)"""
    parts = permission_str.split(' ')
    if len(parts) == 3 and parts[0] == 'muted':
        expiration_time_str = ' '.join(parts[1:])
        expiration_time = datetime.strptime(expiration_time_str,
                                                     "%Y-%m-%d %H:%M:%S")
        current_time = datetime.now()
        return current_time >= expiration_time