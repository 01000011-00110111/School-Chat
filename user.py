"""user.py: User class for the chat app"""
import hashlib
from datetime import datetime, timedelta

from flask_login import LoginManager, logout_user
from flask_socketio import emit

import database
from private import Private, format_userlist

# inactive_users = []

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
    def add_user_class(cls, username, user, userid):
        user_class = cls(username, user, userid)
        database.set_online(userid, False)
        cls.Users.update({userid: user_class})
        tupple = (userid, user['displayName'], user['SPermission'][0])
        # if tupple in inactive_users:
        #     inactive_users.remove(tupple)
        return user_class

    @classmethod
    def delete_user(cls, userid):
        if userid in cls.Users:
            u = cls.Users[userid]
            u.backup()
            # inactive_users.append((u.uuid, u.displayName, u.perm[0]))
            del cls.Users[userid]
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

    def update_account(self, messageC, roleC, userC, displayname, role, profile, theme):
        """Update the user's account details."""
        self.Mcolor = messageC
        self.Rcolor = roleC
        self.Ucolor = userC
        self.displayName = displayname
        self.role = role
        self.profile = profile
        self.theme = theme
        
    def backup(self):
        """Backup the user's data."""
        database.backup_user(self)
        
"""    def unique_online_list(self, userid, visibilty, location, sid):
        # print(visibility)
        icon_perm = {
            "Debugpass": '🔧',
            'modpass': "🛡️",
            'adminpass': "⚒️",
            "": ""
        }
        visibilty_icon = {
            True: '',
            False: '💤',
        }
        
        if self.status == "offline":
            self.status = "online"
        if self.active != visibilty:
            self.active = visibilty

        online_developers = []
        online_admins = []
        online_moderators = []
        online_regular_users = []
        offline_users = []
        online = 0

        for key in User.Users.values():
            if key.status == "online":
                online += 1
                unread = Private.get_unread(
                    format_userlist(self.uuid, key.uuid))
                if isinstance(unread, dict):
                    unread = 0 if key.uuid == self.uuid else unread.get(self.uuid, 0)
                else:
                    unread = 0
                # user_icon = icon_perm.get(key.perm[0]) if key.perm[0] in icon_perm else ""
                unread_list = f"<font color='#FF0000'>{unread}</font>." if unread > 0 else ''
                visibility_stat = visibilty_icon.get(key.active)
                # print(visibility_stat)
                if key.perm[0] == "adminpass":
                    online_admins.append(
                        (f"{unread_list} ⚒️", key.displayName + visibility_stat))
                elif key.perm[0] == "modpass":
                    online_moderators.append(
                        (f"{unread_list} 🛡️", key.displayName + visibility_stat))
                elif key.perm[0] == "Debugpass":
                    online_developers.append(
                        (f"{unread_list} 🔧", key.displayName + visibility_stat))
                else:
                    online_regular_users.append(
                        (f"{unread_list} ", key.displayName + visibility_stat))

            else:
                unread = Private.get_unread(
                    format_userlist(self.uuid, key.uuid))
                if isinstance(unread, dict):
                    unread = 0 if key.uuid == self.uuid else unread.get(self.uuid, 0)
                else:
                    unread = 0
                user_icon = icon_perm.get(key.perm[0])
                unread_list = f"<font color='#FF0000'>{unread}</font>." if unread > 0 else ''
                offline_users.append(
                    (f"{unread_list} {user_icon}", key.displayName))
        
        online_list = online_developers + online_admins + online_moderators + online_regular_users
        if len(online_list) == online:
            pass
        else:
            emit('force')
        # online_developers = []
        # online_admins = []
        # online_moderators = []
        # online_regular_users = []
        # offline_users = []

        for user in inactive_users:
            user_icon = icon_perm.get(user[2], "")
            unread_list = ""  # f"<font color='#FF0000'>{unread}</font>." if unread > 0 else ""
            offline_users.append((f"{unread_list} {user_icon}", user[1]))

        offline_list = offline_users#sorted(offline_users, key=lambda x: (('Debugpass' in x[0]), ('adminpass' in x[0]), ('modpass' in x[0]), ('' in x[0])))

        # if online_list != self.online_list:
        emit("online", (online_list, offline_list), to=sid)
        # self.online_list = online_list
        """


# #####not in the class#####
# for user in database.get_all_offline():
#     if user["userid"] not in User.Users:
#         inactive_users.append(
#             (user["userid"], user["displayName"], user["SPermission"][0]))
