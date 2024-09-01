"""private.py: Backend functions for the private messaging system.
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
import random
from datetime import datetime, timedelta
from string import ascii_uppercase

from flask_socketio import emit

from app import database, log, filtering
from app.user import User
from app.commands.other import format_system_msg
from app.online import add_unread, clear_unread


@app.route("/<prefix>/Private/<private_chat>")
@login_required
def specific_private_page(prefix, private_chat) -> ResponseReturnValue:
    """Get the specific private chat in the uri."""
    # later we can set this up to get the specific room (with permssions)
    # request.cookies.get('Userid')
    # print(prefix)
    # print(private_chat)
    return flask.redirect(flask.url_for("chat_page"))


def handle_private_message(message, pmid, userid):
    """New New chat message handling pipeline."""
    # user = database.find_account_data(userid)
    user = User.get_user_by_id(userid)
    result = filtering.run_filter_private(user, message, userid)
    private = get_messages(pmid, userid)
    if result[0] == "msg":
        # print(private.sids)
        private.add_message(result[1], userid)
        # emit("message_chat", (result[1], pmid), broadcast=True)
        if "$sudo" in message and result[2] != 3:
            filtering.find_cmds(message, user, pmid, private)
        # if "$sudo" in message and result[2] != 3:
        #     filtering.find_cmds(message, user, roomid)
        # elif '$sudo' in message and result[2] == 3:
        #     filtering.failed_message(('permission', 9), roomid)
    # else:
    #     filtering.failed_message(result, roomid)


@socketio.on("private_connect")
def private_connect(sender, receiver, roomid):
    """Switch rooms for the user"""
    socketid = request.sid
    receiverid = database.find_userid(receiver)
    if sender == receiverid:
        emit(
            "message_chat",
            (
                "[SYSTEM]: <font color='#ff7f00'>Don't be a loaner get some friends.</font>",
                roomid,
            ),
            namespace="/",
        )
        return

    active_privates = [
        private
        for private in Private.chats.values()
        if (sender in private.userlist and private.active.get(sender, False))
        or socketid in private.sids
    ]

    for private in active_privates:
        private.active[sender] = False
        if socketid in private.sids:
            private.sids.remove(socketid)

    active_chats = [chat for chat in Chat.chats.values() if socketid in chat.sids]

    for chat in active_chats:
        chat.sids.remove(socketid)

    try:
        chat = get_messages_list(sender, receiverid)
        list = {"message": chat.messages, "pmid": chat.vid, "name": receiver}
    except TypeError:
        emit("room_data", "failed", namespace="/", to=socketid)
        return

    chat.sids.append(socketid)
    emit("private_data", list, to=socketid, namespace="/")


def get_messages_list(sender, receiver):
    """gets the chats with 2 users."""
    userlist = format_userlist(sender, receiver)

    chat = Private.create_or_get_private(userlist, sender)

    return chat


def get_messages(vid, sender):
    """gets the chats with 2 users."""
    chat = Private.create_or_get_private(vid, sender)
    return chat


def format_userlist(uuid1, uuid2):
    """Formats the userlist value."""
    return sorted([uuid1, uuid2], key=lambda x: (not x.isdigit(), x.lower()))

def generate_unique_code(length):
    """Make a room code that doesen't exist yet."""
    rooms = database.distinct_pmid()
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)

        if code not in rooms:
            break

    return code


class Private:
    """The Private chat class."""
    chats = {}  # Dictionary to store existing chats
    chats_userlist = {} #or do i make it

    def __init__(self, private, vid, userlist):
        """Initialize the chat."""
        lst = private["userIds"]
        self.userlist = lst
        self.active = {lst[0]: False, lst[1]: False}
        self.vid = vid
        self.messages = database.get_private_messages(userlist)
        self.unread = private['unread']
        self.backup_values = [
            [0, 0], # 1st is total and 2nd is total sense last message
            datetime.now()
        ]
        self.sids = []

    @classmethod
    def create_or_get_private(cls, vid, sender):
        """Will create or get a private chat."""
        if isinstance(vid, list):
            vid_tuple = tuple(vid)
            existing_private = cls.chats_userlist.get(vid_tuple)
        else:
            existing_private = cls.chats.get(vid)

        if existing_private:
            existing_private.set_active(sender)
            return existing_private

        if isinstance(vid, list):
            private = database.get_private_chat(vid)
        else:
            private = database.find_private(vid)

        if private is None:
            code = generate_unique_code(12)
            private = database.create_private_chat(vid, code)

        userlist = private['userIds']
        priv_id = private['pmid']
        new_private = cls(private, priv_id, userlist)
        cls.chats[priv_id] = new_private
        cls.chats_userlist[tuple(userlist)] = new_private
        new_private.set_active(sender)

        return new_private

    @classmethod
    def get_unread(cls, userlist):
        """Gets the unread count of a user."""
        userlist = (userlist[0], userlist[1])
        if userlist in cls.chats_userlist:
            return cls.chats_userlist[userlist].unread
        return 0

    @classmethod
    def get_userids_list(cls, pmid):
        """Gets the unread count of a user."""
        return cls.chats[pmid].userlist

    def add_message(self, message_text: str, uuid) -> None:
        """Handler for messages so they get logged."""
        self.backup_values[1] = datetime.now()

        for receiver in self.unread:
            if receiver != uuid and not self.active[receiver]:
                self.unread[receiver] += 1
                add_unread(receiver, uuid)

        if len(self.messages) >= 250:
            self.reset_chat()
        else:
            for sid in self.sids:
                emit("message_chat", (message_text), to=sid)
            self.messages.append(message_text)

        log.backup_log(message_text, self.vid, True, self.userlist)
        return ('room', 1)

    def set_active(self, sender):
        """Sets the active user."""
        self.active[sender] = True
        self.unread[sender] = 0
        for receiver in self.unread:
            if receiver != sender and not self.active[receiver]:
                clear_unread(receiver, sender)

    def reset_chat(self):
        """Reset the chat."""
        self.messages.clear()
        msg = format_system_msg('This Private room has been reset.')
        self.messages.append(msg)
        emit("reset_chat", ("admin", self.vid), broadcast=True, namespace="/")


    def backup_data(self):
        """Backups the private chat data."""
        database.update_private(self)
        self.backup_values[0][0] += 1
        if self.backup_values[1] > datetime.now() + timedelta(minutes=30):
            self.backup_values[0][1] += 1
            if self.backup_values[0][1] > 3:
                self.delete()

    def delete(self):
        """Deletes a private chat."""
        del Private.chats[self.vid]
