"""Main webserver file for school-chat, a chat server
Copyright (C) 2023  cserver45, cseven

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

# import hashlib
# import hashlib
# import logging
# import os
# import random
# from string import ascii_uppercase

# import time
# import uuid
# from datetime import datetime, timedelta
# import flask
from flask import request
from flask_socketio import emit
# from appConfig import application
from chat import Chat
from commands.other import end_ping, format_system_msg
from online import socketids, update_userlist
# from private import Private, get_messages, get_messages_list
# from user import User, login_manager

try:
    import setup

    print(False)
except ModuleNotFoundError:
    print(True)

# @app.route("/backup")
# @login_required
# def get_logs_page() -> ResponseReturnValue:
#     """Serve the chat logs (backup)"""
#     html_file = flask.render_template("Backup-chat.html")
#     return html_file


@socketio.on("pingtest")
def handle_ping_tests(start, roomid):
    """Respond with the start time, so ping times can be calculated"""
    end_ping(start, roomid)


# start background tasks should we move this down to 533?
scheduler.start()
startup_msg = True


@socketio.on("connect")
def emit_on_startup():
    socketid = request.sid
    uuid = request.cookies.get("Userid")
    global startup_msg
    if startup_msg:
        emit(
            "message_chat",
            (
                format_system_msg(
                    "If you can see this message, please refresh your client"
                ),
                "ilQvQwgOhm9kNAOrRqbr",
            ),
            broadcast=True,
            namespace="/",
        )
        startup_msg = False
    if uuid in socketids:
        socketids[uuid] = socketid
    if uuid is not None:
        update_userlist(socketid, {"status": "active"}, uuid)


@socketio.on("class_backups")
def backup_classes(_exception=None):
    """Runs after each request."""
    while True:
        chat_chats_copy = dict(Chat.chats)
        for _, chat_instance in chat_chats_copy.items():
            chat_instance.backup_data()
        private_chats_copy = dict(Private.chats)
        for _, private_instance in private_chats_copy.items():
            private_instance.backup_data()
        users_copy = dict(User.Users)
        for user in users_copy:
            if not isinstance(user, str):
                user.backup()
        socketio.sleep(900)


@app.teardown_appcontext
def teardown_request(_exception=None):
    """Runs after each request."""
    chat_chats_copy = dict(Chat.chats)
    for _, chat_instance in chat_chats_copy.items():
        chat_instance.backup_data()
    private_chats_copy = dict(Private.chats)
    for _, private_instance in private_chats_copy.items():
        private_instance.backup_data()
    users_copy = dict(User.Users)
    for user in users_copy:
        if not isinstance(user, str):
            user.backup()
