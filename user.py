"""user.py: User class for the chat app"""
import hashlib
from datetime import datetime, timedelta

from flask_login import LoginManager, login_user
from flask_socketio import emit

import database
from private import format_userlist

Users = {}
inactive_users = []

login_manager = LoginManager()


for user in database.get_all_offline():
    if user["userid"] not in Users:
        inactive_users.append((user["userid"], user["displayName"], user["SPermission"]))

def get_user_by_id(userid):
    user = Users.get(userid, None)
    return user


def add_user_class(username, status, perm, displayName, userid):
    user_class = User(username, status, perm, displayName, userid)
    database.set_online(userid, False)
    Users.update({userid: user_class})
    tupple = (userid, displayName, perm)
    if tupple in inactive_users:
        inactive_users.remove(tupple)
    return user_class

def delete_user(userid):
    u = Users[userid]
    inactive_users.append((u.uuid, u.displayName, u.perm))
    Users.pop(userid)
    u.kill()


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
        # icons = {'settings': '⚙️', 'chat': ''}
        icon_perm = {"Debugpass": '🔧', 'modpass': "⚒️", 'adminpass': "⚒️", "": ""}
        # database.set_online(userid, False)
        if self.status == "offline":
            self.status = "online"

        online_users = set()
        offline_users = set()
        for key in Users.values():
            unread = database.get_unread(format_userlist(self.uuid, key.uuid), self.uuid)
            unread = 0 if key.uuid == self.uuid else unread
            # icon = icons.get(location)
            user_icon = icon_perm.get(key.perm[0])
            unread_list = f"<font color='#FF0000'>{unread}</font>." if unread > 0 else ''
            if key.status == "online":
                # online_users.add((f"{unread_list}{icon} {user_icon}", key.displayName))
                online_users.add((f"{unread_list} {user_icon}", key.displayName))
            else:
                # offline_users.add((f"{unread_list}{icon} {user_icon}", key.displayName))
                offline_users.add((f"{unread_list} {user_icon}", key.displayName))
                
        for user in inactive_users:
            unread = database.get_unread(format_userlist(self.uuid, user[0]), self.uuid)
            unread = 0 if user[0] == self.uuid else unread
            # icon = icons.get(location)
            user_icon = icon_perm.get(user[2][0])
            unread_list = f"<font color='#FF0000'>{unread}</font>." if unread > 0 else ''
            # offline_users.add((f"{unread_list}{icon} {user_icon}", user[1]))
            offline_users.add((f"{unread_list} {user_icon}", user[1]))

        online_list = list(online_users)
        offline_list = list(offline_users)
        emit("online", (online_list, offline_list), to=sid)
