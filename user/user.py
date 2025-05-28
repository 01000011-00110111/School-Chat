"""user/user.py: Backend functions for message handling.
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in app.py or the LICENSE file.
"""
# import asyncio
import hashlib
import uuid
from datetime import datetime

# pylint: disable=W0406

# from socketio_confg import sio
from user.database import get_login_data, get_diplay_names


class User:
    """Represents a logged in user."""
    # pylint: disable=too-many-instance-attributes
    login_data = {(data["username"], data["password"]): data["userId"] for data in get_login_data()}
    usernames = {data["displayName"]: data["userId"] for data in get_diplay_names()}
    Users = {}

    def __init__(self, username, user, userid):
        """Initialize the user."""
        self.username = username
        self.display_name = user['displayName']
        self.perm = user['SPermission']
        self.uuid = userid
        # self.onlineId = user['onlineId']
        self.suuid = str(uuid.uuid4())
        self.status = user['status']
        self.active = True
        self.limit = 0
        self.pause = False
        self.last_message = datetime.now()
        # self.mutes = user['mutes']  # later ill add a mute db value # user['mute_time']
        # self.active = {}
        # other user values
        self.badges = user['badges']
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
                if hashlib.sha384(password.encode('utf-8')).hexdigest() == stored_password:
                    return user_id
        return None

    @staticmethod
    def hash_password(password):
        """Hash a password for storing."""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    @staticmethod
    def get_user(suuid):
        """Get a user by their suuid."""
        return User.Users.get(suuid, None)
