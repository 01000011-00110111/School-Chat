"""user_commands.py: Commands relating to user stuff.
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
# from flask_socketio import emit
# import database

# from user import User
# from online import users_list

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
