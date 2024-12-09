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

    uuid = User.check_credentials(username, password)

    if uuid:
        user = User(username, database.get_user_data(uuid), uuid)
        User.Users[user.suuid] = user
        await sio.emit("login_success", user.suuid, to=sid)
    else:
        await sio.emit("login_fail", to=sid)
