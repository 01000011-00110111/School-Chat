"""user.py: User class for the chat app"""
import hashlib
from datetime import datetime, timedelta

from flask_login import LoginManager, logout_user

import database


login_manager = LoginManager()


class User:
    """Represents a logged in user."""
    Users = {}

    def __init__(self, username, user, uuid):
        """Initialize the user."""
        self.username = username
        self.displayName = user['displayName']
        self.perm = user['SPermission']
        self.uuid = uuid
        self.status = user['status']
        self.active = True
        self.limit = 0
        self.pause = False
        self.last_message = datetime.now()
        self.mutes = user['mutes'] #later ill add a mute db value # user['mute_time']
        self.online_list = []
        #other user values
        self.Rcolor = user['roleColor']
        self.Mcolor = user['messageColor']
        self.Ucolor = user['userColor']
        self.role = user['role']
        self.profile = user['profile']
        self.theme = user['theme']
        self.locked = ['locked']
        self.permission = user['permission']  # temp will go away
        self.themeCount = user['themeCount']
        # self.warned = user['warned']

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

    @classmethod
    def get_user_by_id(cls, userid):
        user = cls.Users.get(userid, None)
        return user
    
    @classmethod
    def get_userid(cls, displayname):
        for _, user in cls.Users.items():
            # print(user)
            if user.displayName == displayname:
                # print(f'e{user}')
                userid = user.uuid
        return userid
    
    @classmethod
    def get_display(cls, uuid):
        user = cls.Users.get(uuid, None)
        displayname = user.displayName
        return displayname

    @classmethod
    def add_user_class(cls, username, user, userid):
        user_class = cls(username, user, userid)
        database.set_online(userid, False)
        cls.Users.update({userid: user_class})
        return user_class

    @classmethod
    def delete_user(cls, userid):
        if userid in cls.Users:
            u = cls.Users[userid]
            del cls.Users[userid]
            u.backup()
            u.remove_user()

    # pylint: disable=E0213
    @login_manager.user_loader
    def load_user(username):
        """Load the user into flask-login."""
        u = database.find_account({'username': username}, 'vid')
        obj = User.Users.get(u['userId'], None)
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
        if self.limit > 15 or self.pause:
            if not self.pause:
                self.pause = True
                self.mutes.append({'spam': datetime.now() + timedelta(minutes=5)})
            return False
        
        self.limit = 0
        self.last_message = datetime.now()
        return True


    def check_mute(self):
        current_time = datetime.now()
        to_remove = []

        for mute in self.mutes:
            for mute_duration in mute.values():
                if mute_duration <= current_time:
                    to_remove.append(mute)

        for remove in to_remove:
            self.mutes.remove(remove)

        if not self.mutes:
            self.pause = False
            
        return bool(to_remove)

    def get_perm(self, roomid):
        mute_list = self.mutes
        current_time = datetime.now()

        for mute_entry in mute_list:
            if isinstance(mute_entry, dict):
                if "all" in mute_entry and mute_entry["all"] >= current_time:
                    return True
                else:
                    self.check_mute()
                    
                if roomid in mute_entry and mute_entry[roomid] >= current_time:
                    return True
                else:
                    self.check_mute()
                
        # print(self.mutes)
        return False

    def update_account(self, messageColor, roleColor, userColor, displayname, role, profile, theme):
        """Update the user's account details."""
        self.Mcolor = messageColor
        self.Rcolor = roleColor
        self.Ucolor = userColor
        self.displayName = displayname
        self.role = role
        self.profile = profile
        self.theme = theme
        
    def backup(self):
        """Backup the user's data."""
        database.backup_user(self)
        
