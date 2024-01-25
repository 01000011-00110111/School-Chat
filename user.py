"""user.py: User class for the chat app"""
import hashlib
from datetime import datetime, timedelta

from flask_login import LoginManager, login_user
from flask_socketio import emit

import database

Users = {}

login_manager = LoginManager()


def get_user_by_id(userid):
    user = Users.get(userid, None)
    return user


def add_user_class(username, status, perm, displayName, userid):
    user_class = User(username, status, perm, displayName, userid)
    database.set_online(userid, False)
    Users.update({userid: user_class})
    return user_class

def delete_user(userid):
    Users.pop(userid)


class User:
    """Represents a logged in user."""

    def __init__(self, username, status, perm, displayName, uuid):
        """Initialize the user."""
        self.username = username
        self.displayName = displayName
        self.perm = perm
        self.uuid = uuid
        self.status = status
        self.limit = 0
        self.pause = False
        self.last_message = datetime.now()
        self.pause_time = 0

    @staticmethod
    def is_authenticated():
        """Check if the user is authenitcated."""
        # this would only be used if we needed to check 2fa or something like that.
        return True

    @staticmethod
    def is_active():
        """Check if the user's session is recent."""
        # we could implement some kind of token expire here I think
        return True

    @staticmethod
    def is_anonymous():
        """Check if the user is anonymous (never will be)."""
        # We disabled anonymous users a while ago
        return False

    def get_id(self):
        """Return the user's username."""
        # whenever we get arround to it, maybe switch this to userid?
        return self.username

    @staticmethod
    def check_password(password_hash, password):
        """Check the user's password against the one entered in the login field."""
        return hashlib.sha384(bytes(password,
                                    'utf-8')).hexdigest() == password_hash

    @staticmethod
    def check_username(username, db_username):
        """Check the username against the one entered in the login field."""
        return username == db_username

    # pylint: disable=E0213
    @login_manager.user_loader
    def load_user(username):
        """Load the user into flask-login."""
        u = database.find_account({'username': username}, 'id')
        obj = Users.get(u['userId'], None)
        if not u:
            return None
        # add_user_class(obj, u["userId"])
        return obj

    def send_limit(self):
        # print(self.limit)
        # print(self.pause)
        # priint(self.last_message)
        # print(self.pause_time)
        difference = self.last_message - datetime.now()
        # print(difference)
        # print(difference.totalseconds())
        if self.limit <= 15 and difference.seconds < 5:
            self.limit += 1
            self.last_message = datetime.now()
            return True
        if self.limit > 15:
            if not self.pause:
                dt = datetime.now()
                td = timedelta(minutes=5)
                self.pause = True
                self.pause_time = dt + td
            else:
                return self.check_pause()
            return False
        self.limit = 0
        self.last_message = datetime.now()
        return True

    def check_pause(self):
        dt = self.pause_time
        td = timedelta(minutes=5)
        if dt + td == datetime.now():
            self.pause = False
            self.limit = 0
            self.pause_time = None
            return True
        return False

    
    def unique_online_list(self, userid, location, sid):
        icons = {'settings': '⚙️', 'chat': ''}
        icon_perm = {"Debugpass": '🔧', 'modpass': "⚒️", "": ""}
        # database.set_online(userid, False)
            

        online_users = set()
        for key in Users.values():
            if key.status == 'offline-locked':
                continue
            icon = icons.get(location)
            user_icon = icon_perm.get(key.perm)
            online_users.add((f"{icon} {user_icon}", key.displayName))

        username_list = list(online_users)
        emit("online", username_list, to=sid)
