from datetime import datetime, timedelta
from flask_socketio import emit
import database


def refresh_online(**kwargs):
    database.clear_online()
    emit("force_username", ("", None), brodcast=True)


def appear_offline(**kwargs):
    """sets the user to appear offline"""
    database.force_set_offline(kwargs["user"]["userId"])
    emit("force_username", ("", None), broadcast=True)
    

def appear_online(**kwargs):
    """sets the user to appear online"""
    database.set_online(kwargs["user"]["userId"])
    emit("force_username", ("", None), broadcast=True)