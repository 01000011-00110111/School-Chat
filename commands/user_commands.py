"""user_commands.py: Commands relating to user stuff.
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
# from flask_socketio import emit
import database

from user import User
from commands.other import format_system_msg
# from online import users_list

def add_badge(**kwargs):
    """add badges."""
    # roomid = kwargs['roomid']
    room = kwargs['room']
    target = kwargs["commands"]["v1"]
    name =  kwargs["commands"]["v2"]
    background = kwargs["commands"]["v3"]
    color = kwargs["commands"]["v4"]
    dev = kwargs["user"]
    delete = False
    for users in User.Users.values():
        if users.display_name == target:
            user = users
        else:
            user = None
    if user is None:
        userdb = database.find_target_data(target)
        user = User.add_user_class(userdb["username"], userdb, userdb["userId"], True)
        delete = True
    user.badges.append([name, background, color])
    if delete:
        User.delete_user(user.uuid)
    msg = format_system_msg(f"Congratulations on the new badge {target}!")
    room.add_message(msg, dev, True)


def remove_badge(**kwargs):
    """remove badges."""
    # roomid = kwargs['roomid']
    room = kwargs['room']
    target = kwargs["commands"]["v1"]
    name =  kwargs["commands"]["v2"]
    dev = kwargs["user"]
    delete = False
    for users in User.Users.values():
        if users.display_name == target:
            user = users
        else:
            user = None
    if user is None:
        userdb = database.find_target_data(target)
        user = User.add_user_class(userdb["username"], userdb, userdb["userId"], True)
        delete = True
    if name in user.badges:
        user.badges.remove([name])
        return
    else:
        room.send_message(format_system_msg(f"{target} does not have that badge"    ))
    if delete:
        User.delete_user(user.uuid)
    msg = format_system_msg(f"Congratulations what did you do to lose it {target}?")
    room.add_message(msg, dev, True)


def block(**kwargs):
    """temp"""
    # roomid = kwargs['roomid']
    user = kwargs['user']
    target = kwargs["commands"]["v1"]
    user.blocked.append(target)


def unblock(**kwargs):
    """temp"""
    # roomid = kwargs['roomid']
    user = kwargs['user']
    target = kwargs["commands"]["v1"]
    user.blocked.remove(target)

# def gif(**kwargs):
    # pass
