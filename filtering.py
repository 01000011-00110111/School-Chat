"""Filter usernames and make the chat more xss safe"""
import os
import re
from typing import Union
from better_profanity import profanity
from flask_socketio import emit
from chat import force_message


def create_username(user_name, user_color, role, role_color, message,
                    message_color, profile_img) -> Union[str, bool]:
    """See if an admin as sending the message, otherwise use normal procedure"""
    # this will be redone so I don't need to use bs4 except for html escaping (maybe)
    if user_name in ('Admin', 'admin', '[admin]', '[ADMIN]', 'ADMIN', '[URL]',
                     'mod', 'Mod', '[mod]', '[Mod]', '[MOD]', 'MOD', 'SYSTEM',
                     '[SYSTEM]', "SONG", "[Song]", "[SONG]", "[song]", " ",
                     "  ", "   ", "Dev E", "cserver"):
        return None

    if user_name == '':
        user_name = "Anonymous"
    elif user_name == "Dev EReal":
        user_name = "Dev E"
    elif user_name == "cserverReal":
        user_name = "cserver"

    messageC = profanity.censor(message)

    locked = os.path.exists("backend/chat.lock")
    user_color_name = "<font color='" + user_color + "'>" + user_name + "</font>"
    message_color_send = "<font color='" + message_color + "'>" + messageC + "</font>"
    role_color_send = "<font color='" + role_color + "'>" + role + "</font>"

    pings = re.findall(r'(?<=\[).+?(?=\])', message_color_send)

    for ping in pings:
        emit("ping", {
            "who": ping,
            "from": user_name
        },
             namespace="/",
             broadcast=True)

    if role == "":
        msg = user_color_name + " - " + message_color_send
    else:
        msg = user_color_name + " (" + role_color_send + ")" + " - " + message_color_send
    if user_name in ("Dev E", "cserver"):
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
