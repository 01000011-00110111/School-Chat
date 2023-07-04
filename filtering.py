"""Filter usernames and make the chat more xss safe"""
import os
import re
from datetime import datetime, timezone, timedelta
from typing import Union
from better_profanity import profanity
from flask_socketio import emit
from chat import force_message
import profanity_words

# get our custom whitelist words (that shouldnot be banned in the first place)
profanity.load_censor_words(whitelist_words=profanity_words.whitelist_words)
profanity.add_censor_words(profanity_words.censored)

def run_filter(username, message, dbm):
    """Its simple now, but when chat rooms come this will be more convoluted."""
    user = dbm.Accounts.find_one({"username": username})
    locked = check_lock()
    user_muted = check_mute(username, user)

    if user_muted != 0:
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
    find_cmds(message, user)

    final_str = compile_message(message, profile_picture, user, role)

    if user['SPermission'] == "Debugpass":
        force_message(final_str)
        emit("message_chat", final_str, broadcast=True, namespace="/")
        return ('dev', 0)

    if locked is True:
        return ("permission", 3)

    # insert the bypass for [SONG] and [JOTD]

    return ('msg', final_str)

def check_mute(username, user):
    if user["permission"] == "muted":
        return 1
    elif user["permission"] == "banned":
        return 2
    return 0

def check_lock():
    """For now, its just as simple as this, but when rooms come it will be more complicated."""
    return os.path.exists("backend/chat.lock")

def filter_message(message):
    return profanity.censor(message)

def find_pings(message, dispname, profile_picture):
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

def find_cmds(message, user):
    """$sudo commands, will push every cmd found to cmds.py along with the user, so we can check if they can do said command."""
    # currently we only find commands, have not implmented the other half
    cmds = re.findall(r'(?<=\$sudo ).+?(?=\</font>)', message)
    for cmd in cmds:
        # send these to sone function in cmds.py, along with the user
        # and have an error handler send back to the room, or maybe just the client? whatever the problem was.
        pass

def compile_message(message, profile_picture, user, role):
    """Taken from old methold of making messages"""
    profile = "<img class='pfp' src='" + profile_picture + "'></img>"
    user_string = "<font color='" + user['userColor'] + "'>" + user['displayName'] + "</font>"
    message_string = "<font color='" + user['messageColor'] + "'>" + message + "</font>"
    role_string = do_dev_easter_egg(role, user)
    date_str = datetime.now(timezone(
        timedelta(hours=-4))).strftime("[%a %I:%M %p] ")

    # because accounts will now be required, we don't need the check if a role exists for the user
    return date_str + profile + " " + user_string + " (" + role_string + ")" + " - " + message_string

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

"""
if user_name in ('Admin', 'admin', '[admin]', '[ADMIN]', 'ADMIN', '[URL]',
                     'mod', 'Mod', '[mod]', '[Mod]', '[MOD]', 'MOD', 'SYSTEM',
                     '[SYSTEM]', "SONG", "[Song]", "[SONG]", "[song]", " ",
                     "  ", "   ", "cseven", "cserver"):
    return None
# move the above code to account creation/editing
# adapt below code so [SONG] and [JOTD] work again
if user_color == "[Joke of the day]: ":
    msg = user_color + "<font color='" + message_color + "'>" + messageC + "</font>"
    return msg
if user_color == "[SONG]: ":
    msg = "<font color='" + message_color + "'>" + user_color + messageC + "</font>"
    return msg
"""
