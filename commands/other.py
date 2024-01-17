"""other.py: functions that need to be imported in multiple places."""

import time

from flask_socketio import emit

import chat


def check_if_dev(user):
    """Return if a user is a dev or not."""
    return 1 if user['SPermission'] == 'Debugpass' else 0


def check_if_mod(user):
    """Return if a user is a mod or not."""
    return 1 if user['SPermission'] == 'modpass' else 0


def help(**kwargs):
    """sends a message with a file full of commands that the user can use."""
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
    elif check_if_mod(issuer) == 1:
        for i, line in enumerate(lines):
            if 'admin commands' in line.lower():
                start_index = i
            elif 'end' in line.lower():
                end_index = i - 1
    else:
        for i, line in enumerate(lines):
            # if check_if_owner(roomid, issuer) == 1:
            #     if 'user commands' in line.lower():
            #         start_index = i
            #     elif 'end' in line.lower():
            #         end_index = i - 1
            # elif check_if_room_mod(issuer) == 1:
            #     if 'user commands' in line.lower():
            #         start_index = i
            #     elif 'room owner commands' in line.lower():
            #         end_index = i - 1
            # else:
                if 'user commands' in line.lower():        
                    start_index = i
                elif 'end' in line.lower():
                    end_index = i - 1

    command_line = "[SYSTEM]:<font color='#ff7f00'><br>" + ' '.join(
        line.strip() for line in lines[start_index:end_index + 1]) + "</font>"
    emit("message_chat", (command_line, roomid), namespace="/")
    

def format_system_msg(msg):
    """Format a message [SYSTEM] would send."""
    return f'[SYSTEM]: <font color="#ff7f00">{msg}</font>'
    

def respond_command(result, roomid):
    """Tell the client that can't run this command for what reason."""

    response_strings = {
        (0, 'dev'): "Hey, you're not a dev!!!",
        (0, 'admin'): "Hey, acting like an admin I see. Too bad you're not one.",
        (0, None): "Try '$sudo help' to see what commands are available to you.",
        (0, 'priv'): "Sorry that command is not available wile in private chats.",
        (0, 'chat'): "chat room made(this is temp)",
        (1, 'chat'): "Your chat name is too long. (less them 10 letters long)(this is temp)",
        (2, 'chat'): "you can not make another chat room(this is temp)",
        (3, 'chat'): "you must have a chat name and not ''(this is temp)",
        (4, 'chat'): "that name was taken(this is temp)",
    }
    response_str = format_system_msg(response_strings.get(result))
    emit("message_chat", (response_str, roomid), namespace="/")

def end_ping(start, ID):
    """The end of the ping comamnd."""
    end = time.time() * 1000.0
    difference = end - start
    msg = '[SYSTEM]: <font color="#ff7f00">Ping Time: ' + str(
        int(difference)) + 'ms RTT</font>'
    chat.add_message(msg, ID, 'true')
    emit("message_chat", (msg, ID), broadcast=True, namespace="/")