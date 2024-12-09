import asyncio
import hashlib
import uuid
from datetime import datetime

import bcrypt # type: ignore

from socketio_confg import sio
from user.database import get_login_data


class User:
    """Represents a logged in user."""
    # pylint: disable=too-many-instance-attributes
    login_data = {(data["username"], data["password"]): data["userId"] for data in get_login_data()}
    Users = {}

    def __init__(self, username, user, uuid):
        """Initialize the user."""
        self.username = username
        self.display_name = user['displayName']
        self.perm = user['SPermission']
        self.uuid = uuid
        self.suuid = str(uuid.uuid4())
        self.status = user['status']
        self.active = True
        self.limit = 0
        self.pause = False
        self.last_message = datetime.now()
        self.mutes = user['mutes']  # later ill add a mute db value # user['mute_time']
        self.active = {}
        # other user values
        self.r_color = user['roleColor']
        self.m_color = user['messageColor']
        self.u_color = user['userColor']
        self.role = user['role']
        self.profile = user['profile']
        self.theme = user['theme']
        self.locked = ['locked']
        self.theme_count = user['themeCount']
        # self.blocked = user['blocked']

    @staticmethod
    def check_credentials(username, password):
        """Check the user's password against the one entered in the login field."""
        for (stored_username, stored_password), user_id in User.login_data.items():
            if stored_username == username:
                # Compare the stored hashed password with the provided password
                if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                    return user_id
        return None

    @staticmethod
    def hash_password(password):
        """Hash a password for storing."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
