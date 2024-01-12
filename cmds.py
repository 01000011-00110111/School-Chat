"""All commands ran by devs, mods, users, etc.
    Copyright (C) 2023  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
import re
import time
from datetime import datetime, timedelta
from inspect import cleandoc
from time import sleep

from flask_socketio import emit

import chat
from main import scheduler
import log
import rooms
import time
from time import sleep
import database

from commands import debug, moderation, online, room, other
# below is needed for systemd restart, do not remove
try:
    import dbus
except ModuleNotFoundError:
    print('''
        \rDBus python library not installed or found. 
        \rSupport for $sudo shutdown or $sudo restart is disabled.
        ''')
    systemd_available = False
else:
    systemd_available = True

# consts
troll_str = """
                [SYSTEM]: <font color='#ff7f00'>YOUVE BEEN TROLOLOLOLLED</font>
                <img src='static/troll-face.jpeg'>
            """


def format_system_msg(msg):
    """Format a message [SYSTEM] would send."""
    return f'[SYSTEM]: <font color="#ff7f00">{msg}</font>'


def find_command(**kwargs):
    """Send whatever sudo command is issued to its respective function."""
    dev_commands = {
        'status': debug.status,
        'pstats': debug.pstats,
        'lines': debug.line_count,
        'rc': room.reset_chat_user,
    }
    admin_commands = {
        'cmd_logs': debug.send_cmd_logs,
        'lock': moderation.lock,
        'unlock': moderation.unlock,
        'globalock': moderation.globalock,
        'reset': room.reset_chat_user,
        # 'globalunlock': moderation.globalunlock,
    }
    # mod_commands = {}
    basic_commands = {
        'help': other.help,
        'refresh': online.refresh_online,
        'offline': online.appear_offline,
        'online': online.appear_online,
        'ping': debug.ping,
    }
    command = kwargs['commands']['v0']
    perm = permission(kwargs['user'])
    if command in dev_commands and perm in ['dev']:
        # print('dev')
        dev_commands[command](**kwargs)
    if command in admin_commands and perm in ['dev', 'admin']:
        # print('admin')
        admin_commands[command](**kwargs)
    if command in basic_commands:
        # print('basic')
        basic_commands[command](**kwargs)
    # try:
    #     response_strings[(kwargs['commands']['v0'], permission(kwargs['user']))] \
    #         (**kwargs)
    # except KeyError:
    #     respond_command(("result", 1, None), kwargs['roomid'])#, None)
    # key = (kwargs['commands']['v0'], permission(kwargs['user']))
    # if key in response_strings and callable(response_strings[key]):
    #     response_strings[key](**kwargs)
    # else:
    #     print("Invalid action or permission level")


def permission(user):
    """get the users permission"""
    return 'dev' if user['SPermission'] == 'Debugpass' else 'admin' \
        if user['SPermission'] == 'modpass' else None
    # in the 1.4 update ill add room mods back


def respond_command(result, roomid):
    """Tell the client that can't run this command for what reason."""

    response_strings = {
        (1, None): "eather that is not a command or you have no perms"
    }
    response_str = response_strings.get((result[1], result[2]))
    emit("message_chat", (response_str, roomid), namespace="/")


def warn_user(user):
    """adds a new warning to the user"""
    warn_count = user["warned"].split(' ')
    current_time = datetime.now()
    expiration_time = current_time + timedelta(days=30)
    date = expiration_time.strftime("%Y-%m-%d %H:%M:%S")
    warn_updated = int(warn_count[0]) + 1
    dbm.Accounts.update_one(
        {"username": user["username"]},
        {'$set': {
            'warned': f"{str(warn_updated)} {date}"
        }})
