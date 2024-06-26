# from datetime import datetime, timedelta

from flask_socketio import emit

import database
from commands import other
from user import User


def appear_offline(**kwargs):
    """sets the user to appear offline"""
    database.force_set_offline(kwargs["user"].uuid)
    User.get_user_by_id(kwargs["user"].uuid).status = 'offline-locked'
    # emit("force_username", ("", None), broadcast=True)
    

def appear_online(**kwargs):
    """sets the user to appear online"""
    database.set_online(kwargs["user"].uuid, True)
    User.get_user_by_id(kwargs["user"].uuid).status = 'online'
    # emit("force_username", ("", None), broadcast=True)