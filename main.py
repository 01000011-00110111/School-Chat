"""main.py: Main webserver file for school-chat, a chat server
    Copyright (C) 2023, 2024  cserver45, cseven

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

import hashlib
import logging
import os
import random
import time
from string import ascii_uppercase
from threading import Timer
import configparser

import flask
from flask import make_response, request
from flask.typing import ResponseReturnValue
from flask_apscheduler import APScheduler
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_socketio import SocketIO, emit

import accounting
import database

import filtering
import log
import uploading
import word_lists
from app_config import application
from chat import Chat
from commands.other import end_ping, format_system_msg
from online import (
    socketids,
    update_userlist,
    update_display,
    users_list,
    user_connections,
    user_last_heartbeat,
    HEARTBEAT_TIMEOUT,
    check_user_heartbeat
    )
from private import Private, get_messages, get_messages_list
from user import User, login_manager

try:
    import setup

    print(False)
except ModuleNotFoundError:
    print(True)

scheduler = APScheduler()

def setup_func():
    """sets up the server"""
    if not os.path.exists("static/profiles"):
        os.makedirs("static/profiles")
    if not os.path.exists("backend/accounts.txt"):
        with open("backend/accounts.txt", "w", encoding="utf-8"):
            pass
    if not os.path.exists("backend/Chat-backup.txt"):
        with open("backend/Chat-backup.txt", "w", encoding="utf-8"):
            pass
    if not os.path.exists("backend/command_log.txt"):
        with open("backend/command_log.txt", "w", encoding="utf-8"):
            pass
    if not os.path.exists("backend/permission.txt"):
        with open("backend/permission.txt", "w", encoding="utf-8"):
            pass
    if not os.path.exists("backend/chat-rooms_log.txt"):
        with open("backend/chat-rooms_log.txt", "w", encoding="utf-8"):
            pass
    if not os.path.exists("backend/webserver.log"):
        with open("backend/webserver.log", "w", encoding="utf-8"):
            pass
    if not os.path.exists("backend/unbanned_words.txt"):
        with open("backend/unbanned_words.txt", "w", encoding="utf-8"):
            pass
    if not os.path.exists("backend/banned_words.txt"):
        with open("backend/banned_words.txt", "w", encoding="utf-8"):
            pass
    database.setup_chatrooms()
    word_lists.whitelist_words, word_lists.blacklist_words = word_lists.start()


if __name__ == "__main__":
    setup_func()
if os.path.exists(os.path.abspath("setup.py")):
    setup.chcek_if_data_is_missing()
    setup.self_destruct()
    print(False)
else:
    print(True)

app = flask.Flask(__name__)
app.secret_key = os.urandom(500)  # ITS ONLY AT 500!!!!!!
config = configparser.ConfigParser()
config.read("config/keys.conf")
app.config['ENV'] = config['backend']['ENV']

logging.basicConfig(filename="backend/webserver.log", filemode="a", level=logging.ERROR)
root = logging.getLogger().setLevel(logging.ERROR)

socketio = SocketIO(app)

scheduler.init_app(app)
scheduler.api_enabled = True
database.clear_online()

login_manager.init_app(app)
login_manager.login_view = "login_page"

# pylint: disable=C0302
# pylint: enable=E0213

# license stuff
if __name__ == "__main__":
    print("Copyright (C) 2023, 2024  cserver45, cseven")
    print("License info can be viewed in main.py or the LICENSE file.")


def void(*_):
    """voids any values sent"""
    return None


@app.route("/chat")
@login_required
def chat_page() -> ResponseReturnValue:
    """Serve the main chat window."""
    template = "chat.html"
    user = database.find_login_data(request.cookies.get("Userid"), True)
    if "Debugpass" in user["SPermission"][0]:
        template = 'dev.html'
    elif "adminpass" in user["SPermission"][0]:
        template = 'admin.html'
    elif "modpass" in user["SPermission"][0]:
        template = 'mod.html'
    return flask.render_template(template)


@app.route("/chat/<room_name>")
@login_required
def specific_chat_page(room_name) -> ResponseReturnValue:
    """Get the specific room in the uri."""
    # later we can set this up to get the specific room (with permssions)
    void(room_name)
    return flask.redirect(flask.url_for("chat_page"))


@app.route("/chat/Private/<private_chat>")
@login_required
def specific_private_page(private_chat) -> ResponseReturnValue:
    """Get the specific private chat in the uri."""
    # later we can set this up to get the specific room (with permssions)
    void(private_chat)
    return flask.redirect(flask.url_for("chat_page"))


@app.route("/logout")
@login_required
def logout():
    """Log out the current user"""
    uuid = request.cookies.get("Userid")
    resp = make_response(flask.redirect(flask.url_for("login_page")))
    resp.set_cookie("Userid", "", expires=0)
    user = User.get_user_by_id(uuid)
    if user and user.status != "offline-locked":
        user.status = "offline"
    database.set_offline(uuid)
    update_userlist(socketids[uuid], {"status": "offline"}, uuid)
    User.delete_user(uuid)
    logout_user()
    del socketids[uuid]
    return resp


@app.route("/login", methods=["POST", "GET"])
@app.route("/", methods=["GET", "POST"])
def login_page() -> ResponseReturnValue:
    """Show the login page."""
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for("chat_page"))

    if request.method == "POST":
        # redo client side checks here on server side, like signup
        username = request.form.get("username")
        password = request.form.get("password")
        tos_agree = request.form.get("TOSagree")
        socketid = request.form.get("socket")
        next_page = request.args.get("next")
        user = database.find_login_data(username, False)
        if user is None:
            return flask.render_template(
                "login.html", error="That account does not exist!"
            )
        if tos_agree != "on":
            return flask.render_template(
                "login.html", error="You did not agree to the TOS!"
            )

        if User.check_username(username, user["username"]) and User.check_password(
            user["password"], password
        ):
            user_obj = User.add_user_class(username, user, user["userId"])
            login_user(user_obj)
            socketids[user["userId"]] = socketid
            update_userlist(socketid, {"status": "active"}, user["userId"])
            if next_page is None:
                next_page = flask.url_for("chat_page")
            else:
                if "editor" in next_page:
                    next_page = flask.url_for("projects")
                if next_page not in word_lists.approved_links:
                    next_page = flask.url_for("chat_page")
            resp = flask.make_response(flask.redirect(next_page))
            resp.set_cookie("Username", user["username"])
            resp.set_cookie("Theme", user["theme"])
            profile_image = (
                user.get("profile")
                or "/static/favicon.ico"
            )
            resp.set_cookie("Profile",profile_image)
            resp.set_cookie("Userid", user["userId"])
            resp.set_cookie("DisplayName", user["displayName"])
            return resp
        # else:
        return flask.render_template(
            "login.html", error="That username or password is incorrect!"
        )
    # else:
    return flask.render_template("login.html", appVersion=application.app_version)


@app.route("/signup", methods=["POST"])
def signup_post() -> ResponseReturnValue:
    """The creating of an account."""
    username = request.form.get("SUsername")
    password = request.form.get("SPassword")
    password2 = request.form.get("SPassword2")
    role = request.form.get("SRole")
    displayname = request.form.get("SDisplayname")
    email = request.form.get("SEmail")

    result, msg = accounting.run_regex_signup(username, role, displayname)
    if result is not False:
        return flask.render_template(
            "signup-index.html",
            error=msg,
        )
    email_check = accounting.check_if_disposable_email(email)

    if email_check in [1,2]:
        return flask.render_template("signup-index.html", error="That email is not valid!")

    if password != password2:
        return flask.render_template(
            "signup-index.html",
            error="Password boxes do not match!",
            SUsername=username,
            SRole=role,
            SDisplayname=displayname,
        )
    possible_user = database.find_account({"username": username}, "vid")
    possible_dispuser = database.find_account(
        {"displayName": displayname}, "customization"
    )
    if (
        possible_user is not None
        or possible_dispuser is not None
        or username in word_lists.banned_usernames
        or displayname in word_lists.banned_usernames
    ):
        return flask.render_template(
            "signup-index.html",
            error="That Username/Display name is already taken!",
            SRole=role,
        )
    possible_email = database.find_account({"email": email}, "vid")
    if possible_email is not None:
        return flask.render_template(
            "signup-index.html",
            error="That Email is already used!",
            SEmail=email,
            SUsername=username,
            SDisplayname=displayname,
            SRole=role,
        )
    accounting.create_user(username, password, email, role, displayname)
    log.log_accounts(f"A user has made a account named {username}")
    return flask.redirect(flask.url_for("login_page"))


@app.route("/signup", methods=["GET"])
def signup_get() -> ResponseReturnValue:
    """Serve the signup page."""
    return flask.render_template("signup-index.html")


@app.route("/verify/<userid>/<verification_code>")
def verify(userid, verification_code):
    """Verify a user."""
    template_string = "verified.html"
    user_id = database.find_account({"userId": userid}, "vid")
    if user_id is not None:
        user_code = accounting.create_verification_code(user_id)
        if user_code == verification_code:
            database.update_account_set(
                "perm", {"userId": user_id["userId"]}, {"$set": {"locked": "false"}}
            )
            user = user_id["username"]
            log.log_accounts(
                f"The account {user} is now verified and may now chat in any chat room."
            )
            page_title = "Account Verified"
            background = "success"
            verifiedicon = 'fa-solid fa-check success'
            verified_text = "You are now verified!"
            verified_sub_text1 = "Thank you for using School Chat"
            verified_sub_text2 = "You can close this page when you're ready"
            return flask.render_template(template_string, icon = verifiedicon,
                                            verifiedText = verified_text,
                                            verifiedsubText1 = verified_sub_text1,
                                            verifiedsubText2 = verified_sub_text2,
                                            page_title = page_title, background = background)
    page_title = "Account Verification Failed"
    background = "failed"
    unverifiedicon = 'fa-solid fa-x failed'
    verified_text = "Verification Failed"
    verified_sub_text = "Sorry but we failed to verify your School Chat account, please try again"
    return flask.render_template(template_string, icon = unverifiedicon,
                                 verifiedText = verified_text,
                                 verifiedsubText1 = verified_sub_text,
                                 page_title = page_title, background = background)


@app.route("/change-password", methods=["POST", "GET"])
def change_password() -> ResponseReturnValue:
    """Handles the user password reset request and sends the reset email."""
    if request.method == "GET":
        return flask.render_template("password_part1.html")

    if request.method == "POST":
        username = request.form.get("username")
        user = database.find_login_data(username, False)
        if user:
            accounting.password(user)
        return "check the email you used to make the account for a password reset link"
    return None


@app.route("/reset/<userid>/<verification_code>", methods=["POST", "GET"])
def reset_password(userid, verification_code) -> ResponseReturnValue:
    """Handles the user password reset request and sends the reset email."""
    user_id = database.find_account({"userId": userid}, "vid")
    if request.method == "GET":
        return flask.render_template(
            "password_part2.html", username=user_id["username"]
        )

    if request.method == "POST":
        password = request.form.get("password")
        password2 = request.form.get("password2")
        if user_id is not None:
            user_code = accounting.create_verification_code(user_id)

            if user_code == verification_code:
                if password != password2:
                    return flask.render_template(
                        "password_part2.html",
                        error="Your passwords do not match!",
                        username=user_id["username"],
                    )

                password_hash = hashlib.sha384(bytes(password, "utf-8")).hexdigest()

                if password_hash == user_id["password"]:
                    return flask.render_template(
                        "password_part2.html",
                        error="You can not use your previous password!",
                        username=user_id["username"],
                    )

                database.update_account_set(
                    "vid",
                    {"userId": user_id["userId"]},
                    {"$set": {"password": password_hash}},
                )
                return flask.redirect(flask.url_for("login_page"))
    return "Invalid reset code."


##### Backup file code ######

@app.route("/backup")
@login_required
def get_logs_page() -> ResponseReturnValue:
    """Serve the chat logs (backup)"""
    uuid = request.cookies.get('Userid')
    user = User.get_user_by_id(uuid)

    if 'adminpass' in user.perm:
        return flask.render_template("Backup-chat.html")

    return flask.redirect(flask.url_for("chat_page"))


@socketio.on("change_chunk")
def handle_chunk_change(direction):
    """Sends a chunk of the backup file to the backup page."""
    uuid = request.cookies.get('Userid')
    backup_sesson = log.FileHandler.get_handler(uuid)
    lines = None
    if direction == 'next':
        lines = backup_sesson.read_chunk()
    if direction == 'prev':
        lines = backup_sesson.read_chunk_reverse()
    if direction == 'reset':
        lines = backup_sesson.read_chunk()

    emit('load_chunk', lines)


@app.route("/settings", methods=["GET"])
@login_required
def settings_page() -> ResponseReturnValue:
    """Serve the settings page for the user."""
    user = database.find_login_data(request.cookies.get("Userid"), True)
    if request.cookies.get("Userid") != user["userId"]:
        # someone is trying something funny
        return flask.Response(
            "Something funny happened. Try Again (Unauthorized)", status=401
        )

    return flask.render_template(
        "settings.html",
        user=user["username"],
        passwd="we are not adding password editing just yet",
        email=user["email"],
        displayName=user["displayName"],
        role=user["role"],
        user_color=user["userColor"],
        role_color=user["roleColor"],
        message_color=user["messageColor"],
        profile=user["profile"],
        theme=user["theme"],
    )


@app.route("/settings", methods=["POST"])
@login_required
def customize_accounts() -> ResponseReturnValue:
    """Customize the account."""
    return_val = None
    # Gather form and cookie data into a single dictionary
    data = {
        "username": request.form.get("user"),
        "userid": request.cookies.get("Userid"),
        "displayname": request.form.get("display"),
        "role": request.form.get("role"),
        "message_color": request.form.get("message_color"),
        "role_color": request.form.get("role_color"),
        "user_color": request.form.get("user_color"),
        "email": request.form.get("email"),
        "file": request.files.get('profile'),
        "theme": request.form.get("theme"),
    }

    user = User.get_user_by_id(data["userid"])
    user_email = database.get_email(user.uuid)
    old_path = user.profile
    blank = "<FileStorage: '' ('application/octet-stream')>"

    # Handle file upload
    profile_location = (
        old_path if data.get("file") == blank else (
            uploading.upload_file(data["file"], old_path) or old_path
        )
    )

    if profile_location == 0:
        return flask.render_template(
            "settings.html", error="That file format is now allowed!", **data
        )
        # profile_location = old_path

    # Check theme
    if data["theme"] is None:
        return flask.render_template(
            "settings.html", error="Pick a theme before updating!", **data
        )

    # Validate username and other inputs
    theme = user.theme if data["theme"] == "" else data["theme"]
    result, error = accounting.run_regex_signup(data["username"], data["role"], data["displayname"])
    if result is not False:
        return flask.render_template("settings.html", error=error, **data)

    # Check display name
    if (
        database.find_account({"displayName": data["displayname"]}, "customization") is not None
        and user.display_name != data["displayname"]
    ) and data["displayname"] in word_lists.banned_usernames:
        return flask.render_template(
            "settings.html", error="That display name is already taken!", **data
        )

    # Check email
    email_check = database.find_account({"email": data["email"]}, "vid")
    if email_check is None and user_email != data["email"]:
        verification_code = accounting.create_verification_code(user)
        accounting.send_verification_email(
            user.username, data["email"], verification_code, user.uuid
        )
    elif email_check is not None and user_email != data["email"]:
        return flask.render_template(
            "settings.html", error="That email is taken", **data
        )
    # Update account details
    if user.locked != "locked":
        account_update_data = {
            "userid": user.uuid,
            "message_color": data["message_color"],
            "role_color": data["role_color"],
            "user_color": data["user_color"],
            "displayname": data["displayname"],
            "role": data["role"],
            "profile": profile_location,
            "theme": theme,
            "email": data["email"]
        }
        if data["displayname"] != user.display_name:
            update_display({"username": data["displayname"], "status": "active"}, data["userid"])
        database.update_account(account_update_data)
        user.update_account(account_update_data)
        resp = flask.make_response(flask.redirect(flask.url_for("chat_page")))
        resp.set_cookie("Username", user.username)
        resp.set_cookie("Theme", theme)
        resp.set_cookie("Profile", profile_location)
        resp.set_cookie("Userid", user.uuid)
        error = "Updated account!"
        return_val = resp
    else:
        if user_email == data["email"]:
            return_val = flask.render_template(
                "settings.html",
                error="You must verify your account before you can change settings",
                **data,
            )
        database.update_account_set(
            "vid", {"username": data["username"]}, {"$set": {"email": data["email"]}}
        )
        error = "Updated email!"

    log.log_accounts(f"The account {user} has updated some setting(s)")
    return return_val

@app.route("/support/docs")
def docx():
    """Opens support documentation."""
    return flask.render_template("support/documentation.html")

@app.route("/support/docs/categories/<page>")
def category():
    """Opens support documentation."""
    return flask.render_template("support/chat_docs.html")


##### THEME STUFF #####
@app.route("/editor")
@login_required
def editor():
    """Opens the theme editor page."""
    return flask.render_template("theme/editor.html")


@app.route("/projects")
@login_required
def projects():
    """Opens the project page."""
    return flask.render_template("theme/projects.html")


@socketio.on("get_projects")
def handle_project_requests():
    """Sends all projects the user has access to."""
    socketid = request.sid
    userid = request.cookies.get("Userid")
    displayname = request.cookies.get("DisplayName").replace('"', "")
    theme_projects = database.get_projects(userid, displayname)
    projects_fixed = []
    for project in theme_projects:
        del project["_id"]
        del project['theme']
        project["author"] = project["author"][1:]
        projects_fixed.append(project)
    emit("projects", (projects_fixed), to=socketid)


@socketio.on("create_project")
def handle_projecet_creation():
    """Creates a theme project to edit."""
    socketid = request.sid
    userid = request.cookies.get("Userid")
    user = User.get_user_by_id(userid)
    while True:
        code = ""
        for _ in range(5):
            code += random.choice(ascii_uppercase)

        if code not in database.get_all_projects():
            break
    project = database.create_project(userid, user.display_name, code)
    del project["_id"]
    project['theme'] = {}
    project["author"] = project["author"][1:]
    emit("set_theme", project, to=socketid)


@socketio.on("get_project")
def send_project(theme_id):
    """Sends the requested project to the user."""
    socketid = request.sid
    project = database.get_project(theme_id)
    del project["_id"]
    project['theme'] = {}
    project["author"] = project["author"][1:]
    emit("set_theme", project, to=socketid)


@socketio.on("save_project")
def handle_save_project(theme_id, theme, name, publish):
    """Saves/Publish a project."""
    socketid = request.sid
    database.save_project(theme_id, theme, name, publish)
    message = 'Project Published' if publish else 'Project Saved'
    emit("response", (message, False), to=socketid)


@socketio.on("update_theme_status")
def handle_status_change(theme_id, status):
    """Changes the themes status"""
    database.update_theme_status(theme_id, status)


@socketio.on("delete_project")
def handle_delete_project(project):
    """Deletes a project."""
    socketid = request.sid
    database.delete_project(project)
    emit("response", ("Project deleted", False), to=socketid)


@socketio.on("get_themes")
def handle_theme_requests():
    """gets all themes you have access"""
    socketid = request.sid
    uuid = request.cookies.get("Userid")
    themes = database.get_all_projects()
    themes_fixed = []
    for theme in themes:
        if theme['theme'] == {}:
            continue
        if theme["status"] == "private" and theme['author'][0] != uuid:
            continue
        if theme['name'] == 'Untitled Project':
            continue
        del theme["_id"]
        if 'project' in theme:
            del theme['project']
        del theme["status"]
        del theme["theme"]
        theme["author"] = theme["author"][1:]
        themes_fixed.append(theme)
    emit("receive_themes", (themes_fixed), to=socketid)


@socketio.on("get_theme")
def send_theme(theme_id):
    """Sends the theme the user requested."""
    socketid = request.sid
    theme = database.get_project(theme_id)
    if theme is None:
        theme = database.get_project("dark")
    del theme["_id"]
    if 'project' in theme:
        del theme['project']
    theme["author"] = theme["author"][1:]
    del theme["status"]
    emit("set_theme", theme, to=socketid)


##### END OF THEME STUFF #####

@socketio.on("status_change")
def handle_connect(data):
    """Will be used later for online users."""
    socketid = request.sid
    update_userlist(socketid, data, request.cookies.get("Userid"))


@socketio.on("get_full_list")
def handle_full_list_request():
    """updates the full list of users in the online list"""
    socketid = request.sid
    emit("update_list_full", (list(users_list.values())), namespace="/", to=socketid)


@socketio.on("connect")
def emit_on_startup():
    """Handle a new connection."""
    socketid = request.sid
    userid = request.cookies.get("Userid")

    if userid is not None:
        if userid not in user_connections:
            user_connections[userid] = set()
        user_connections[userid].add(socketid)
        user_last_heartbeat[userid] = time.time()

        socketids[userid] = socketid
        update_userlist(socketid, {"status": "active"}, userid)

        Timer(HEARTBEAT_TIMEOUT + 5, check_user_heartbeat,
              args=[userid, handle_disconnect]).start()


@socketio.on("disconnect")
def handle_disconnect(socketid=None, userid=None):
    """Handle user disconnection."""
    if not socketid:
        socketid = request.sid
    if not userid:
        userid = request.cookies.get("Userid")

    if userid is None:
        return

    if userid in user_connections:
        user_connections[userid].discard(socketid)
        if not user_connections[userid]:
            del user_connections[userid]

    active_privates = [
        private
        for private in Private.chats.values()
        if userid in private.userlist and private.active.get(userid, False)
        or socketid in private.sids
    ]

    for private in active_privates:
        if userid in private.active:
            private.active[userid] = False
        if socketid in private.sids:
            private.sids.remove(socketid)

    active_chats = [chat for chat in Chat.chats.values() if socketid in chat.sids]

    for chat in active_chats:
        chat.sids.remove(socketid)

    if not user_connections.get(userid):
        try:
            user = User.get_user_by_id(userid)
            if user and user.status != "offline-locked":
                user.status = "offline"
            database.set_offline(userid)
            update_userlist(socketid, {"status": "offline"}, userid)
        except TypeError as e:
            print(f"Error setting user offline: {e}")


@socketio.on("heartbeat")
def handle_heartbeat(status, roomid, priv):
    """Handle heartbeat from the client."""
    socketid = request.sid
    userid = request.cookies.get("Userid")

    if userid is not None:
        user_last_heartbeat[userid] = time.time()

        if userid in user_connections:
            update_userlist(socketid, {"status": status}, userid)
            if priv == "true":
                room = get_messages(roomid, userid)
            else:
                room = Chat.create_or_get_chat(roomid)
            if socketid not in room.sids:
                socketids[userid] = socketid
                room.sids.append(socketid)


@socketio.on("get_rooms")
def get_rooms(userid):
    """Grabs the chat rooms."""
    user_info = database.find_account_room_data(userid)
    user_name = user_info["displayName"]
    user_permissions = user_info["SPermission"]

    room_access = database.get_rooms()

    def emit_rooms(rooms, access_level):
        emit(
            "roomsList",
            (
                [{"vid": room["vid"], "name": room["name"]} for room in rooms],
                access_level,
            ),
            namespace="/",
            to=request.sid,
        )

    if "Debugpass" in user_permissions:
        emit_rooms(room_access, "dev")
        return

    if "adminpass" in user_permissions:
        room_access = [room for room in room_access if room["whitelisted"] != "devonly"]
        emit_rooms(room_access, "mod")
        return

    if "modpass" in user_permissions:
        room_access = [
            room for room in room_access
            if "devonly" not in room["whitelisted"]
            and "adminonly" not in room["whitelisted"]
        ]
        emit_rooms(room_access, "mod")
        return

    if user_info["locked"] == "locked":
        emit(
            "roomsList",
            ([{"vid": "zxMhhAPfWOxuZylxwkES", "name": ""}], "locked"),
            namespace="/",
            to=request.sid,
        )
        return

    def is_accessible(room, user_name):
        return (
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
        )

    accessible_rooms = [
        {"vid": room["vid"], "name": room["name"]}
        for room in room_access
        if is_accessible(room, user_name)
    ]

    emit_rooms(accessible_rooms, user_info["locked"])


@socketio.on("message_chat")
def handle_message(_, message, vid, userid, private, hidden):
    """sends mesage data to the proper function."""
    if private == 'false':
        handle_chat_message(
            message, vid, userid, hidden
        )
    else:
        handle_private_message(message, vid, userid)


def handle_chat_message(message, roomid, userid, hidden):
    """New New chat message handling pipeline."""
    room = Chat.create_or_get_chat(roomid)
    user = User.get_user_by_id(userid)
    result = filtering.run_filter_chat(user, room, message, roomid, userid)
    if result[0] == "msg":
        if room is not None and not hidden:
            room.add_message(result[1], user)
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


def handle_private_message(message, pmid, userid):
    """New New chat message handling pipeline."""
    # user = database.find_account_data(userid)
    user = User.get_user_by_id(userid)
    result = filtering.run_filter_private(user, message, userid)
    private = get_messages(pmid, userid)
    if result[0] == "msg":
        private.add_message(result[1], user, userid)
        if "$sudo" in message and result[2] != 3:
            filtering.find_cmds(message, user, pmid, private)
    else:
        filtering.failed_message(result, pmid)


@socketio.on("pingtest")
def handle_ping_tests(start, roomid):
    """Respond with the start time, so ping times can be calculated"""
    end_ping(start, roomid)


@socketio.on("room_connect")
def connect(roomid, sender):
    """Switch rooms for the user"""
    socketid = request.sid
    try:
        room = Chat.create_or_get_chat(roomid)
        lst = {"roomid": room.vid, 'user_data': room.user_data,\
                "name": room.name, "msg": room.messages}
    except TypeError:
        emit("room_data", "failed", namespace="/", to=socketid)
        return

    active_privates = [
        private
        for private in Private.chats.values()
        if sender in private.userlist and private.active.get(sender, False)
        or socketid in private.sids
    ]

    for private in active_privates:
        if sender in private.active:
            private.active[sender] = False
        if socketid in private.sids:
            private.sids.remove(socketid)

    active_chats = [chat for chat in Chat.chats.values() if socketid in chat.sids]

    for chat in active_chats:
        chat.sids.remove(socketid)

    room.sids.append(socketid)
    emit("room_data", (lst), to=socketid, namespace="/")


@socketio.on("private_connect")
def private_connect(sender, receiver, roomid):# rework the connect code later
    """Switch rooms for the user"""
    socketid = request.sid
    receiverid = database.find_userid(receiver)
    if sender == receiverid:
        emit(
            "message_chat",
            (
                format_system_msg("Don't be a loaner get some friends"),
                roomid,
            ),
            namespace="/",
        )
        return

    active_privates = [
        private
        for private in Private.chats.values()
        if sender in private.userlist and private.active.get(sender, False)
        or socketid in private.sids
    ]

    for private in active_privates:
        if sender in private.active:
            private.active[sender] = False
        if socketid in private.sids:
            private.sids.remove(socketid)

    active_chats = [chat for chat in Chat.chats.values() if socketid in chat.sids]

    for chat in active_chats:
        chat.sids.remove(socketid)

    try:
        chat = get_messages_list(sender, receiverid)
        lst = {"message": chat.messages, "pmid": chat.vid, "name": receiver}
    except TypeError:
        emit("room_data", "failed", namespace="/", to=socketid)
        return

    chat.sids.append(socketid)
    emit("private_data", lst, to=socketid, namespace="/")


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
        time.sleep(900)


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
            if user is not None:
                user.backup()


if __name__ == "__main__":
    socketio.start_background_task(backup_classes)
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
