"""user/login.py: Backend functions for message handling.
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in app.py or the LICENSE file.
"""
from socketio_confg import sio
from user.user import User
import user.database as database


@sio.on("login")
async def login(sid, data):
    """
    This function is called when a client sends a login request to the server.
    """
    username = data["username"]
    password = data["password"]

    print(username, password)

    uuid = User.check_credentials(username, password)

    if uuid:
        user = User(username, database.get_user_data(uuid), uuid)
        User.Users[user.suuid] = user
        await sio.emit("login", {'suuid': user.suuid, 'status': 'successful'}, to=sid)
    else:
        await sio.emit("login", { 'suuid': False, 'status': 'failed'}, to=sid)


@sio.on("logout")
async def logout(sid, data):
    """
    This function is called when a client sends a logout request to the server.
    """
    suuid = data["suuid"]
    if suuid in User.Users:
        del User.Users[suuid]
        await sio.emit("send_to_login", to=sid)


def check_suuid(suuid):
    """
    Checks if a user is logged in.
    """
    if suuid in User.Users:
        return True
    else:
        return False
