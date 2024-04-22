# from datetime import datetime, timedelta

from flask_socketio import emit

import database
from commands import other
from user import User


def refresh_online(**kwargs):
    # database.clear_online()
    emit("force_username", ("", None), brodcast=True)
    msg = "This is a testing command and will be removed in upcoming updates."
    emit("message_chat", (
        other.format_system_msg(msg),
            kwargs['roomid']),
             namespace="/")


def appear_offline(**kwargs):
    """sets the user to appear offline"""
    database.force_set_offline(kwargs["user"].vid)
    User.get_user_by_id(kwargs["user"].vid).status = 'offline-locked'
    emit("force_username", ("", None), broadcast=True)
    

def appear_online(**kwargs):
    """sets the user to appear online"""
    database.set_online(kwargs["user"].vid, True)
    User.get_user_by_id(kwargs["user"].vid).status = 'online'
    emit("force_username", ("", None), broadcast=True)