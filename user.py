"""user.py: User class for the chat app"""
import hashlib
from datetime import datetime, timedelta

from flask_login import LoginManager, login_user, logout_user
from flask_socketio import emit

import database
from private import format_userlist

Users = {}
inactive_users = []

login_manager = LoginManager()


for user in database.get_all_offline():
    if user["userid"] not in Users:
        inactive_users.append((user["userid"], user["displayName"], user["SPermission"][0]))

def get_user_by_id(userid):
    user = Users.get(userid, None)
    return user


def add_user_class(username, status, perm, displayName, userid):
    user_class = User(username, status, perm, displayName, userid)
    database.set_online(userid, False)
    Users.update({userid: user_class})
    tupple = (userid, displayName, perm[0])
    if tupple in inactive_users:
        inactive_users.remove(tupple)
    return user_class

def delete_user(userid):
    if userid in Users:
        u = Users[userid]
        inactive_users.append((u.uuid, u.displayName, u.perm[0]))
        del Users[userid]
        u.remove_user()

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
        self.mute_time = 0
        self.online_list = []

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
    
    def remove_user(self):
        logout_user()

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
        difference = datetime.now() - self.last_message
        if self.limit <= 15 and difference.total_seconds() < 5:
            self.limit += 1
            self.last_message = datetime.now()
            return True
        if self.limit > 15:
            if not self.pause:
                self.pause = True
                self.mute_time = datetime.now() + timedelta(minutes=5)
            else:
                return self.check_mute()
            return False
        self.limit = 0
        self.last_message = datetime.now()
        return True

    def check_mute(self):
        if self.mute_time <= datetime.now():
            self.pause = False
            self.limit = 0
            self.mute_time = None
            return True
        return False

    
    def unique_online_list(self, userid, location, sid):
        # icons = {'settings': '⚙️', 'chat': ''}
        icon_perm = {"Debugpass": '🔧', 'modpass': "🛡️", 'adminpass': "⚒️", "": ""}
        # database.set_online(userid, False)
        if self.status == "offline":
            self.status = "online"

        offline_users = set()
        online_developers = []
        online_admins = []
        online_moderators = []
        online_regular_users = []

        for key in Users.values():
            unread = database.get_unread(format_userlist(self.uuid, key.uuid), self.uuid)
            unread = 0 if key.uuid == self.uuid else unread
            user_icon = icon_perm.get(key.perm[0])
            unread_list = f"<font color='#FF0000'>{unread}</font>." if unread > 0 else ''

            if key.status == "online":
                if key.perm[0] == "adminpass":
                    online_admins.append((f"{unread_list} {user_icon}", key.displayName))
                elif key.perm[0] == "modpass":
                    online_moderators.append((f"{unread_list} {user_icon}", key.displayName))
                elif key.perm[0] == "Debugpass":
                    online_developers.append((f"{unread_list} {user_icon}", key.displayName))
                else:
                    online_regular_users.append((f"{unread_list} {user_icon}", key.displayName))

        online_list = online_developers + online_admins + online_moderators + online_regular_users

        for user in inactive_users:
            unread = database.get_unread(format_userlist(self.uuid, user[0]), self.uuid)
            unread = 0 if user[0] == self.uuid else unread
            user_icon = icon_perm.get(user[2])
            unread_list = f"<font color='#FF0000'>{unread}</font>." if unread > 0 else ''
            offline_users.add((f"{unread_list} {user_icon}", user[1]))

        offline_list = list(offline_users)
        
        emit("online", (online_list, offline_list), to=sid) if online_list != self.online_list else None
        if online_list != self.online_list:
            self.online_list = online_list
