"""online_commands.py: All online commands for the chat
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
from flask_socketio import emit
from app import database

from app.user import User
from app.online import users_list


def appear_offline(**kwargs):
    """sets the user to appear offline"""
    uuid = kwargs["user"].uuid
    database.force_set_offline(uuid)
    User.get_user_by_id(uuid).status = 'offline-locked'
    users_list[uuid]['status'] = 'offline-locked'

    emit("update_list", users_list[uuid], namespace="/", broadcast=True)


def appear_online(**kwargs):
    """sets the user to appear online"""
    uuid = kwargs["user"].uuid
    database.set_online(kwargs["user"].uuid, True)
    User.get_user_by_id(kwargs["user"].uuid).status = 'online'
    users_list[uuid]['status'] = 'active'

    emit("update_list", users_list[uuid], namespace="/", broadcast=True)