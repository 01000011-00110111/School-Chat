"""All commands ran by devs, mods, users, etc.
    Copyright (C) 2023  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
import chat
from main import scheduler
import log
import rooms
import time
from time import sleep
import database

from commands import debug, online
# below is needed for systemd restart, do not remove
try:
    import dbus
except ModuleNotFoundError:
    print(
        'DBus python library not installed or found, support for $sudo shutdown or $sudo restart is disabled.'
    )
    systemd_available = False
else:
    systemd_available = True
import re
from datetime import datetime, timedelta
from flask_socketio import emit


def find_command(**kwargs):
    """Send whatever sudo command is issued to its respective function."""
    response_strings = {
        ('status', 'dev'): debug.status,
        ('pstats', 'dev'): debug.pstats,
        ('lines', 'dev'): debug.line_count,
        ('appear_offline', 'dev'): online.appear_offline,
        ('appear_online', 'dev'): online.appear_online
    }
    try:
        response_strings[(kwargs['commands']['v0'], permission(kwargs['user']))] \
            (**kwargs)
    except KeyError:
        respond_command(("result", 1, None), kwargs['roomid'])#, None)
        
def permission(user):
    """get the users permission"""
    return 'dev' if user['SPermission'] == 'Debugpass' else 'admin' \
        if user['SPermission'] == 'modpass' else None
    # in the 1.4 update ill add room mods back


def respond_command(result, roomid):
    """Tell the client that can't run this command for what reason."""


    response_strings = {
        (1,None): "eather that is not a command or you have no perms"
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
