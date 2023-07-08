"""Filter usernames and make the chat more xss safe"""
import os
import re
from datetime import datetime, timezone, timedelta
from better_profanity import profanity
from flask_socketio import emit
from chat import force_message
import profanity_words
import cmds

# get our custom whitelist words (that shouldnot be banned in the first place)
profanity.load_censor_words(whitelist_words=profanity_words.whitelist_words)
profanity.add_censor_words(profanity_words.censored)


def run_filter(username, message, dbm, roomid):
    """Its simple now, but when chat rooms come this will be more convoluted."""
    user = dbm.Accounts.find_one({"username": username})
    locked = check_lock(roomid, dbm)
    user_muted = check_mute(username, user)

    if user_muted != 0 and user['SPermission'] != 'Debugpass':
        return ('permission', user_muted)

    if user['SPermission'] != "Debugpass":
        message = filter_message(message)
        role = profanity.censor(user['role'])
    else:
        role = user['role']

    if user['profile'] == "":
        profile_picture = 'static/favicon.ico'
    else:
        profile_picture = user['profile']

    find_pings(message, user['displayName'], profile_picture)
    find_cmds(message, user, locked, roomid)

    final_str = compile_message(message, profile_picture, user, role)

    if user['SPermission'] == "Debugpass":
        force_message(final_str, roomid, dbm)
        emit("message_chat", (final_str, roomid),
             broadcast=True,
             namespace="/")
        return ('dev', 0)
    else:
        final_str = compile_message(message, profile_picture, user, role)
        if locked == 'true':
            return ("permission", 3)
        return ('msg', final_str)

    # insert the bypass for [SONG] and [JOTD]

    return ('msg', final_str)


def check_mute(username, user):
    if user["permission"] == "muted":
        return 1
    elif user["permission"] == "banned":
        return 2
    return 0


def check_lock(roomid, dbm):
    """For now, its just as simple as this, but when rooms come it will be more complicated."""
    locked = dbm.rooms.find_one({"roomid": roomid})
    return locked["locked"]


def filter_message(message):
    """No one likes profanity, especially flagging systems."""
    return profanity.censor(message)


def find_pings(message, dispname, profile_picture):
    """Gotta catch 'em all!"""
    pings = re.findall(r'(?<=\[).+?(?=\])', message)
    for ping in pings:
        emit("ping", {
            "who": ping,
            "from": dispname,
            "pfp": profile_picture,
            "message": message
        },
             namespace="/",
             broadcast=True)


def find_cmds(message, user, locked, roomid):
    """$sudo commands, will push every cmd found to cmds.py along with the user, so we can check if they can do said command."""
    # currently we only find commands, have not implmented the other half
    #cmds = re.findall(r'(?<=\$sudo ).+?(?=\</font>)', message)
    command_split = message.split("$sudo")
    command_split.pop(0)

    # this check is needed, because the finding of commands is after chat lock check in run_filter
    # leading to users being able to send comamnds, even when chat is locked
    # we should be the only ones that can do that (devs)
    if locked is True and user['SPermission'] != 'Debugpass':
        return ("permission", 3)

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
            cmds.find_command(commands, user, roomid)


def compile_message(message, profile_picture, user, role):
    """Taken from old methold of making messages"""
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
    if result[0] == 'permission':
        if result[1] == 1:
            fail_str = "[SYSTEM]: <font color='#ff7f00'>You can't send messages because you are muted.</font>"
        elif result[1] == 2:
            fail_str = "[SYSTEM]: <font color='#ff7f00'>You can't send messages because you have been banned.</font>"
        elif result[1] == 3:
            fail_str = "[SYSTEM]: <font color='#ff7f00'>You can't send messages because this chat room has been locked.</font>"
        elif result[1] == 4:
            fail_str = "[SYSTEM]: <font color='#ff7f00'>You can't send messages because you have been banned from this chat room.</font>"
    elif result[0] == "dev":
        return
    # more will be added when error messages become more common (chat rooms TM)
    # something simmilar to this will be in cmds.py for commands failing.
    emit("message_chat", (fail_str, roomid), namespace="/")


"""
if user_name in ('Admin', 'admin', '[admin]', '[ADMIN]', 'ADMIN', '[URL]',
                     'mod', 'Mod', '[mod]', '[Mod]', '[MOD]', 'MOD', 'SYSTEM',
                     '[SYSTEM]', "SONG", "[Song]", "[SONG]", "[song]", " ",
                     "  ", "   ", "cseven", "cserver"):
    return None
# move the above code to account editing
# adapt below code so [SONG] and [JOTD] work again
if user_color == "[Joke of the day]: ":
    msg = user_color + "<font color='" + message_color + "'>" + messageC + "</font>"
    return msg
if user_color == "[SONG]: ":
    msg = "<font color='" + message_color + "'>" + user_color + messageC + "</font>"
    return msg
"""
