import os
from dataclasses import dataclass
from datetime import datetime, timedelta
import flask
from flask import Blueprint, request
from flask.typing import ResponseReturnValue

from flask_socketio import emit
from flask_login import (
    login_required,
)

from app import socketio
from app import database#, log, filtering
from app.user import User

chat_bp = Blueprint('chat', __name__)

##### chat route code #####

@chat_bp.route("/chat")
@login_required
def chat_page() -> ResponseReturnValue:
    """Serve the main chat window."""
    return flask.render_template("chat.html")


@chat_bp.route("/chat/<room_name>")
@login_required
def specific_chat_page(room_name) -> ResponseReturnValue:
    """Get the specific room in the uri."""
    # later we can set this up to get the specific room (with permssions)
    # request.cookies.get('Userid')
    # print(room_name)
    return flask.redirect(flask.url_for("chat_page"))


@chat_bp.route("/admin")
@login_required
def admin_page() -> ResponseReturnValue:
    """Get the specific room in the uri."""
    user = database.find_login_data(request.cookies.get("Userid"), True)
    if "adminpass" in user["SPermission"]:
        return flask.render_template("admin.html")
    return flask.redirect(flask.url_for("chat_page"))


@chat_bp.route("/admin/<room_name>")
@login_required
def specific_admin_page(room_name) -> ResponseReturnValue:
    """Get the specific room in the uri."""
    # later we can set this up to get the specific room (with permssions)
    # request.cookies.get('Userid')
    # print(room_name)
    return flask.redirect(flask.url_for("admin_page"))


##### chat code ######


def handle_chat_message(message, roomid, userid, hidden):
    """New New chat message handling pipeline."""
    # print(roomid)
    # later I will check the if the username is the same as the one for the session somehow

    room = Chat.create_or_get_chat(roomid)

    # print(room)
    # user = database.find_account_data(userid)
    user = User.get_user_by_id(userid)
    result = filtering.run_filter_chat(user, room, message, roomid, userid)
    if result[0] == "msg":
        if room is not None and not hidden:
            room.add_message(result[1])
            # emit("message_chat", (result[1], roomid), broadcast=True)
            # addons.message_addons(message, user, roomid, room)
            # above is not offical again, so commented out
            if "$sudo" in message and result[2] != 3:
                filtering.find_cmds(message, user, roomid, room)
            elif "$sudo" in message and result[2] == 3:
                filtering.failed_message(("permission", 9), roomid)
        elif room is not None and hidden:
            if "$sudo" in message and result[2] != 3:
                filtering.find_cmds(message, user, roomid, room)
        else:
            filtering.failed_message(7, roomid)
    else:
        filtering.failed_message(result, roomid)


@socketio.on("room_connect")
def connect(roomid, sender):
    """Switch rooms for the user"""
    socketid = request.sid
    try:
        room = Chat.create_or_get_chat(roomid)
        list = {"roomid": room.vid, "name": room.name, "msg": room.messages}
    except TypeError:
        emit("room_data", "failed", namespace="/", to=socketid)
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

    room.sids.append(socketid)
    # print(room.sids)
    emit("room_data", (list), to=socketid, namespace="/")


@socketio.on("get_rooms")
def get_rooms(userid):
    """Grabs the chat rooms."""
    user_info = database.find_account_room_data(userid)
    user_name = user_info["displayName"]
    user_permissions = user_info["SPermission"]

    room_access = database.get_rooms()
    # print(room_access)
    if "Debugpass" in user_permissions:
        emit(
            "roomsList",
            (
                [{"vid": room["vid"], "name": room["name"]} for room in room_access],
                "dev",
            ),
            namespace="/",
            to=request.sid,
        )
        return

    if "adminpass" in user_permissions:
        room_access = [room for room in room_access if room["whitelisted"] != "devonly"]
        emit(
            "roomsList",
            (
                [{"vid": room["vid"], "name": room["name"]} for room in room_access],
                "mod",
            ),
            namespace="/",
            to=request.sid,
        )
        return

    if "modpass" in user_permissions:
        room_access = [
            room
            for room in room_access
            if "devonly" not in room["whitelisted"]
            and "adminonly" not in room["whitelisted"]
        ]
        emit(
            "roomsList",
            (
                [{"vid": room["vid"], "name": room["name"]} for room in room_access],
                "mod",
            ),
            namespace="/",
            to=request.sid,
        )
        return

    if user_info["locked"] == "locked":
        emit(
            "roomsList",
            ([{"vid": "zxMhhAPfWOxuZylxwkES", "name": ""}], "locked"),
            namespace="/",
            to=request.sid,
        )

    accessible_rooms = []
    for room in room_access:
        if (
            (room["blacklisted"] == "empty" and room["whitelisted"] == "everyone")
            or (
                room["whitelisted"] != "everyone"
                and "users:" in room["whitelisted"]
                and user_name in room["whitelisted"].split("users:")[1].split(",")
            )
            or (
                room["blacklisted"] != "empty"
                and "users:" in room["blacklisted"]
                and user_name not in room["blacklisted"].split("users:")[1].split(",")
                and room["whitelisted"] == "everyone"
            )
            and (
                "devonly" not in room["whitelisted"]
                and "modonly" not in room["whitelisted"]
                and "lockedonly" not in room["whitelisted"]
            )
        ):
            accessible_rooms.append({"vid": room["vid"], "name": room["name"]})

    # print(accessible_rooms)
    emit(
        "roomsList",
        (accessible_rooms, user_info["locked"]),
        namespace="/",
        to=request.sid,
    )


##### chat class code #####

def format_system_msg(msg):
    """Format a message [SYSTEM] would send."""
    return f'[SYSTEM]: <font color="#ff7f00">{msg}</font>'

# import cmds
@dataclass
class ChatConfig:
    """Config stuff for chats."""

    def __init__(self, config):
        self.whitelisted = config["whitelisted"]
        self.banned = config["blacklisted"]
        self.can_send = config["canSend"]
        self.locked = config["locked"]
        self.backups = [0, 0]
        self.last_message =  datetime.now()



class Chat:
    """Chat class."""
    chats = {}  # Dictionary to store existing chats

    def __init__(self, room, roomid):
        """Initialize the chat."""
        self.name = room["roomName"]
        self.vid = roomid
        self.config = ChatConfig(room)
        self.messages = database.get_messages(roomid)
        self.sids = []
        self.sids = []


    @classmethod
    def create_or_get_chat(cls, roomid):
        """Create a new chat or return an existing one."""
        cls.log_rooms()
        if roomid in cls.chats:
            return cls.chats[roomid]
        if roomid not in cls.chats:
            room = database.get_room_data(roomid)
            new_chat = cls(room, roomid)
            cls.chats[roomid] = new_chat
            return new_chat
        return None

    @classmethod
    def log_rooms(cls):
        """add what this does here."""
        if os.path.exists("backend/chatlog.txt"):
            with open("backend/chatlog.txt", "a", encoding="utf-8") as logfile:
                logfile.write(f"{datetime.now()} - Chat log updated\nChats:\n")
                for key, _chat in cls.chats.items():
                    logfile.write(key+'\n')


    @classmethod
    def set_all_lock_status(cls, status):
        """Sets the lo9ck status on all active chat rooms."""
        for chat in cls.chats:
            chat.config.locked = status

    @classmethod
    def add_message_to_all(cls, message_text: str, _rooms, _permission='false'):
        """ads messsages to all chatrooms"""
        for chat in cls.chats:
            chat.config.last_message = datetime.now()
            _lines = len(chat.messages)
            chat.messages.append(message_text)

            log.backup_log(message_text, chat.vid, False, None)
            return ('room', 1)


    def send_message(self, message_text: str):
        """Emits the message to the chat"""
        emit("message_chat", (message_text), broadcast=True, namespace="/")


    def add_message(self, message_text: str, permission='false') -> None:
        """Handler for messages so they get logged."""
        # private = self.vid == "all"
        self.config.last_message = datetime.now()
        lines = len(self.messages)# if not private else 1

        if ((lines >= 350) and permission != 'true'):
            self.reset_chat()
        else:
            self.messages.append(message_text)

        for sid in self.sids:
            emit("message_chat", (message_text), to=sid)

        log.backup_log(message_text, self.vid, False, None)
        return ('room', 1)


    def reset_chat(self):
        """Reset the chat."""
        self.messages.clear()
        msg = format_system_msg('Chat reset by an admin.')
        self.messages.append(msg)
        emit("reset_chat", ("admin", self.vid), broadcast=True, namespace="/")


    def set_lock_status(self, status):
        """Changes the chat lock status."""
        self.config.locked = status


    def backup_data(self):
        """Backups the chat room."""
        database.update_chat(self)
        self.config.backups[0] += 1
        if self.config.last_message > datetime.now() + timedelta(minutes=90):
            self.config.backups[1] += 1
            if self.config.backups[1] > 3:
                self.delete()

    def delete(self):
        """Deletes the chat."""
        del Chat.chats[self.vid]
