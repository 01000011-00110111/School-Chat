from socketio_confg import sio
from user.user import User
from user.database import database

@sio.on("signup")
async def signup(sid, data):
    """
    This function is called when a client sends a signup request to the server.
    """
    username = data.get("username", "").strip()
    password = data.get("password", "")

    # Validate input
    if not username or not password:
        await sio.emit("signup", {'suuid': False, 'status': 'failed', 'reason': 'missing_fields'}, to=sid)
        return

    # Check if username already exists
    if database.username_exists(username):
        await sio.emit("signup", {'suuid': False, 'status': 'failed', 'reason': 'username_taken'}, to=sid)
        return

    # Check password strength (example: at least 6 characters)
    if len(password) < 6:
        await sio.emit("signup", {'suuid': False, 'status': 'failed', 'reason': 'weak_password'}, to=sid)
        return

    # Attempt to sign up
    uuid = User.sign_up(username, password)

    if uuid:
        user = User(username, database.get_user_data(uuid), uuid)
        User.Users[user.suuid] = user
        await sio.emit("signup", {'suuid': user.suuid, 'status': 'successful'}, to=sid)
    else:
        await sio.emit("signup", {'suuid': False, 'status': 'failed', 'reason': 'internal_error'}, to=sid)
