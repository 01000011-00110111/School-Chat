"""All online commands for the chat
    Copyright (C) 2023  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
import database

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
