"""other.py: Functions that need to be imported in multiple places by other commands
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""

import re
import time
from datetime import datetime

from flask_socketio import emit

from chat import Chat


def check_if_dev(user):
    """Return if a user is a dev or not."""
    return 1 if 'Debugpass' in user.perm else 0

def check_if_admin(user):
    """Return if a user is a mod or not."""
    return 1 if 'adminpass' in user.perm else 0

def check_if_mod(user):
    """Return if a user is a mod or not."""
    return 1 if 'modpass' in user.perm else 0


def song(**kwargs):
    """Send a song to the chat."""
    room = kwargs['room']
    user = kwargs['user']
    msg = format_song_msg(' '.join(list(kwargs["commands"].values())[1:]))
    room.add_message(msg, user)


def send_admin(**kwargs):
    """Send a song to the chat."""
    room = kwargs['room']
    user = kwargs['user']
    msg = format_admin_msg(' '.join(list(kwargs["commands"].values())[1:]))
    room.add_message(msg, user, False   )


def help_command(**kwargs):
    """sends a message with a file full of commands that the user can use."""
    # pylint: disable=R0912
    roomid = kwargs['roomid']
    issuer = kwargs['user']
    with open('backend/command_list.txt', 'r', encoding="utf8") as file:
        lines = file.readlines()
    start_index = None
    end_index = None

    if check_if_dev(issuer) == 1:
        for i, line in enumerate(lines):
            if 'dev commands' in line.lower():
                start_index = i
            elif 'end' in line.lower():
                end_index = i - 1
    elif check_if_admin(issuer) == 1:
        for i, line in enumerate(lines):
            if 'admin commands' in line.lower():
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

    command_line = format_system_msg(' '.join(
        line.strip() for line in lines[start_index:end_index + 1]))
    emit("message_chat", (command_line, roomid), namespace="/")


def format_system_msg(msg):
    """Format a message [SYSTEM] would send."""
    profile = "<img class='message_pfp' src='/static/favicon.ico'></img>"
    user_string = "<p style='color: #ff7f00;'>[SYSTEM]</p>"
    message_string = f"<p style='color: #ffffff;'>{msg}</p>"
    role_string = "<p style='background:\
#ff7f00; color: #ffffff;' class='badge'>System</p>"
    date_str = datetime.now().strftime("%a %I:%M %p ")
    return {
        'profile': profile,
        'user': user_string,
        'message': message_string,
        'badges': [role_string, None],
        'date': date_str
    }


def format_song_msg(msg):
    # """Format a message [SONG] would send."""
    # return f'<font color="#0E9556">[SONG]: {msg}</font>'
    """Format a message [SONG] would send."""
    profile = "<img class='message_pfp' src='/static/favicon.ico'></img>"
    user_string = "<p style='color:'>[SONG]</p>"
    message_string = f"<p style='color: #0E9556;'>{msg}</p>"
    role_string = "<p style='background:\
#0E9556; color: #ffffff;' class='badge'>Song</p>"
    date_str = datetime.now().strftime("%a %I:%M %p ")
    return {
        'profile': profile,
        'user': user_string,
        'message': message_string,
        'badges': [role_string, None],
        'date': date_str
    }

def format_admin_msg(msg):
    # """Format a message [SONG] would send."""
    # return f'<font color="#e0790b">[ADMIN]: {msg}</font>'
    """Format a message Admin would send."""
    profile = "<img class='message_pfp' src='/static/favicon.ico'></img>"
    user_string = "<p style='color:'>[ADMIN]</p>"
    message_string = f"<p style='color: #f9211b;'>{msg}</p>"
    role_string = "<p style='background:\
#f9211b; color: #ffffff;' class='badge'>Admin</p>"
    date_str = datetime.now().strftime("%a %I:%M %p ")
    return {
        'profile': profile,
        'user': user_string,
        'message': message_string,
        'badges': [role_string, None],
        'date': date_str
    }


def respond_command(result, roomid):
    """Tell the client that can't run this command for what reason."""

    response_strings = {
        (0, 'dev'): "Hey, you're not a dev!!!",
        (0, 'admin'): "Hey, acting like an admin I see. Too bad you're not one.",
        (0, 'mod'): "Hey, Don't be shy call for help when you need it. Your not a mod.",
        (0, None): "Try '$sudo help' to see what commands are available to you.",
        (0, 'priv'): "Sorry that command is not available wile in private chats.",
        (0, 'chat'): "chat room made(this is temp)",
        (1, 'chat'):
            "Your chat name is too long. (less them 10 letters long)(this is temp)",
        (2, 'chat'): "you can not make another chat room(this is temp)",
        (3, 'chat'): "you must have a chat name and not ''(this is temp)",
        (4, 'chat'): "that name was taken(this is temp)",
    }
    response_str = format_system_msg(response_strings.get(result))
    emit("message_chat", (response_str, roomid), namespace="/")


def e_count_backup(**kwargs):
    """E_count_bacup"""
    roomid = kwargs['roomid']
    room = kwargs['room']
    with open('backend/Chat-backup.txt', 'r', encoding="utf-8") as file:
        text = file.read()
    count = len(re.findall(r'\be\b', text))
    msg = format_system_msg("Current count: " + str(count))
    room.add_message(msg, roomid)


def end_ping(start, roomid):
    """The end of the ping comamnd."""
    room = Chat.create_or_get_chat(roomid)
    end = time.time() * 1000.0
    difference = end - start
    msg = '[SYSTEM]: <font color="#ff7f00">Ping Time: ' + str(
        int(difference)) + 'ms RTT</font>'
    room.add_message(msg, roomid)
