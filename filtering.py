"""Filter usernames and make the chat more xss safe"""
import os
import re
from datetime import datetime, timezone, timedelta
from typing import Union
from better_profanity import profanity
from flask_socketio import emit
from chat import force_message

# get our custom whitelist words (that shouldnot be banned in the first place)
profanity.load_censor_words(whitelist_words=[
    'crap',
    'god',
    'LMAO',
    'lmao',
    'omg',
    'stupid',
    'dumb',
    'piss',
    'wtf',
    'stroke',
    'suck',
    'hebe',
    'gay',
    'screw',
])
profanity.add_censor_words([
    'sh!t',
    'dumba',
    'dam',
    'boobie',
])  # add your custom words here (will be in a separate file someday)


def create_username(user_name, user_color, role, role_color, message,
                    message_color, profile_picture) -> Union[str, bool]:
    """See if an admin as sending the message, otherwise use normal procedure"""
    # this will be redone so I don't need to use bs4 except for html escaping (maybe)
    if user_name in ('Admin', 'admin', '[admin]', '[ADMIN]', 'ADMIN', '[URL]',
                     'mod', 'Mod', '[mod]', '[Mod]', '[MOD]', 'MOD', 'SYSTEM',
                     '[SYSTEM]', "SONG", "[Song]", "[SONG]", "[song]", " ",
                     "  ", "   ", "cseven", "cserver"):
        return None

    # user = dbm.Accounts.find_one({'displayName': user_name})
    # if user['permission'] == "muted" or user['permission'] == "banned":
    # return

    if user_name == '':
        user_name = "Anonymous"
        #return
    elif user_name == "csevenReal":
        user_name = "cseven"
        # return
    elif user_name == "cserverReal":
        user_name = "cserver"

    messageC = profanity.censor(message)
    rolec = profanity.censor(role)

    locked = os.path.exists("backend/chat.lock")
    if profile_picture == "":
        profile_picture = 'static/favicon.ico'
    profile_img = "<img class='pfp' src='" + profile_picture + "'></img>"
    user_color_name = "<font color='" + user_color + "'>" + user_name + "</font>"
    message_color_send = "<font color='" + message_color + "'>" + messageC + "</font>"
    if role_color == "#00ff00":
        role_color_send = "<font class='Dev_colors-loop'>" + rolec + "</font>"
    elif role_color == "#3262a8":
        role_color_send = "<font class='ow_colors-loop'>" + rolec + "</font>"
    else:
        role_color_send = "<font color='" + role_color + "'>" + rolec + "</font>"
    pings = re.findall(r'(?<=\[).+?(?=\])', message_color_send)
    cmds = re.findall(r'(?<=\$sudo ).+?(?=\</font>)', message_color_send)

    for ping in pings:
        emit("ping", {
            "who": ping,
            "from": user_name,
            "pfp": profile_img,
            "message": messageC
        },
             namespace="/",
             broadcast=True)

    for cmd in cmds:
        emit(
            "cmd",
            {
                "cmd": cmd,
                # "from": user_name,
                # "who": user_name
            },
            namespace="/",
            broadcast=False)

    date_str = datetime.now(timezone(
        timedelta(hours=-4))).strftime("[%a %I:%M %p] ")

    if role == "":
        msg = date_str + profile_img + " " + user_color_name + " - " + message_color_send
    else:
        msg = date_str + profile_img + " " + user_color_name + " (" + role_color_send + ")" + " - " + message_color_send
    if user_name in ("cseven", "cserver"):
        force_message(msg)
        emit("message_chat", msg, broadcast=True, namespace="/")
        return True

    if locked == True:
        return True
    # don't look at this too closely, its to make it impossible to impersonate (also gets arround line 12 problems)
    if user_color == "[Joke of the day]: ":
        msg = user_color + "<font color='" + message_color + "'>" + messageC + "</font>"
        return msg
    if user_color == "[SONG]: ":
        msg = "<font color='" + message_color + "'>" + user_color + messageC + "</font>"
        return msg

    return msg


# g
