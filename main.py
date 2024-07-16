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
import hashlib
import logging
import os
import random
from string import ascii_uppercase

# import time
# import uuid
# from datetime import datetime, timedelta
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

# these are the files that do not import dbm
# import appConfig
import filtering
import log
import uploading
import word_lists
from appConfig import application
from chat import Chat
from commands.other import end_ping, format_system_msg
from online import socketids, update_userlist, users_list
from private import Private, get_messages, get_messages_list
from user import User, login_manager

try:
    import setup

    print(False)
except ModuleNotFoundError:
    print(True)

# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address  #, default_error_responder

scheduler = APScheduler()


def setup_func():
    """sets up the server"""
    if not os.path.exists("static/profiles"):
        os.makedirs("static/profiles")
    if not os.path.exists("backend/accounts.txt"):
        with open("backend/accounts.txt", "w"):
            pass
    if not os.path.exists("backend/Chat-backup.txt"):
        with open("backend/Chat-backup.txt", "w"):
            pass
    if not os.path.exists("backend/command_log.txt"):
        with open("backend/command_log.txt", "w"):
            pass
    if not os.path.exists("backend/permission.txt"):
        with open("backend/permission.txt", "w"):
            pass
    if not os.path.exists("backend/chat-rooms_log.txt"):
        with open("backend/chat-rooms_log.txt", "w"):
            pass
    if not os.path.exists("backend/webserver.log"):
        with open("backend/webserver.log", "w"):
            pass
    if not os.path.exists("backend/unbanned_words.txt"):
        with open("backend/unbanned_words.txt", "w"):
            pass
    if not os.path.exists("backend/banned_words.txt"):
        with open("backend/banned_words.txt", "w"):
            pass
    database.setup_chatrooms()


if __name__ == "__main__":
    setup_func()
if os.path.exists(os.path.abspath("setup.py")):
    setup.chcek_if_data_is_missing()
    setup.self_destruct()
    print(False)
else:
    print(True)

app = flask.Flask(__name__)
app.secret_key = os.urandom(9001)  # ITS OVER 9000!!!!!!

# rate limiting
# limiter = Limiter(get_remote_address,
#                   app=app,
#                   on_breach=default_error_responder)

logging.basicConfig(filename="backend/webserver.log", filemode="a", level=logging.ERROR)
root = logging.getLogger().setLevel(logging.ERROR)

socketio = SocketIO(app)

scheduler.init_app(app)
scheduler.api_enabled = True
database.clear_online()

login_manager.init_app(app)
login_manager.login_view = "login_page"

# pylint: enable=E0213

# license stuff
if __name__ == "__main__":
    print("Copyright (C) 2023  cserver45, cseven")
    print("License info can be viewed in main.py or the LICENSE file.")


@app.route("/chat")
@login_required
def chat_page() -> ResponseReturnValue:
    """Serve the main chat window."""
    return flask.render_template("chat.html")


@app.route("/chat/<room_name>")
@login_required
def specific_chat_page(room_name) -> ResponseReturnValue:
    """Get the specific room in the uri."""
    # later we can set this up to get the specific room (with permssions)
    # request.cookies.get('Userid')
    # print(room_name)
    return flask.redirect(flask.url_for("chat_page"))


@app.route("/admin")
@login_required
def admin_page() -> ResponseReturnValue:
    """Get the specific room in the uri."""
    user = database.find_login_data(request.cookies.get("Userid"), True)
    if "adminpass" in user["SPermission"]:
        return flask.render_template("admin.html")
    return flask.redirect(flask.url_for("chat_page"))


@app.route("/admin/<room_name>")
@login_required
def specific_admin_page(room_name) -> ResponseReturnValue:
    """Get the specific room in the uri."""
    # later we can set this up to get the specific room (with permssions)
    # request.cookies.get('Userid')
    # print(room_name)
    return flask.redirect(flask.url_for("admin_page"))


@app.route("/<prefix>/Private/<private_chat>")
@login_required
def specific_private_page(_prefix, _private_chat) -> ResponseReturnValue:
    """Get the specific private chat in the uri."""
    # later we can set this up to get the specific room (with permssions)
    # request.cookies.get('Userid')
    # print(prefix)
    # print(private_chat)
    return flask.redirect(flask.url_for("chat_page"))


@app.route("/logout")
@login_required
def logout():
    """Log out the current user"""
    User.delete_user(request.cookies.get("Userid"))
    logout_user()
    # sid = socketids[request.cookies.get("Userid")]
    del socketids[request.cookies.get("Userid")]
    # update_userlist(sid, {'status': 'offline'}, request.cookies.get("Userid"))
    resp = make_response(flask.redirect(flask.url_for("login_page")))
    resp.set_cookie("Userid", "", expires=0)
    return resp


@app.route("/login", methods=["POST", "GET"])
@app.route("/", methods=["GET", "POST"])
def login_page() -> ResponseReturnValue:
    """Show the login page."""
    # socketid = request.sid
    # print(current_user,'current user')
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for("chat_page"))

    if request.method == "POST":
        # redo client side checks here on server side, like signup
        username = request.form.get("username")
        password = request.form.get("password")
        TOSagree = request.form.get("TOSagree")
        socketid = request.form.get("socket")
        next_page = request.args.get("next")
        user = database.find_login_data(username, False)
        # print(userids)
        if user is None:
            return flask.render_template(
                "login.html", error="That account does not exist!"
            )
        # userid = user["userId"]
        if TOSagree != "on":
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
                if "adminpass" in user["SPermission"]:
                    next_page = flask.url_for("admin_page")
                else:
                    next_page = flask.url_for("chat_page")
            else:
                if "editor" in next_page:
                    next_page = flask.url_for("projects")
                if next_page not in word_lists.approved_links:
                    next_page = flask.url_for("chat_page")
                    if "adminpass" in user["SPermission"]:
                        next_page = flask.url_for("admin_page")
            resp = flask.make_response(flask.redirect(next_page))
            resp.set_cookie("Username", user["username"])
            resp.set_cookie("Theme", user["theme"])
            resp.set_cookie(
                "Profile",
                user["profile"] if user["profile"] != "" else "/static/favicon.ico",
            )
            resp.set_cookie("Userid", user["userId"])
            resp.set_cookie("DisplayName", user["displayName"])
            resp.set_cookie("test", "e e")
            return resp
        else:
            return flask.render_template(
                "login.html", error="That username or password is incorrect!"
            )
    else:
        return flask.render_template("login.html", appVersion=application.appVersion)


# @app.route('/changelog')
# def changelog_page() -> ResponseReturnValue:
#     """Serve the changelog, so old links don't break."""
#     html_file = flask.render_template('update-log.html')
#     return html_file

# we should retire the above link

# custom error message for signup, instead of generic 429 error
# def signup_ratelimit_error_responder(request_limit: RequestLimit):
#    return jsonify({"error": "rate_limit_exceeded"})
# yes ik the stuff above is horibbly broken, but the other stuff is fine


@app.route("/signup", methods=["POST"])
# @limiter.limit("1 per day")
def signup_post() -> ResponseReturnValue:
    """The creating of an account."""
    # global verification_code_list
    # global verification_code
    SUsername = request.form.get("SUsername")
    SPassword = request.form.get("SPassword")
    SPassword2 = request.form.get("SPassword2")
    SRole = request.form.get("SRole")
    SDisplayname = request.form.get("SDisplayname")
    SEmail = request.form.get("SEmail")

    result, msg = accounting.run_regex_signup(SUsername, SRole, SDisplayname)
    if result is not False:
        return flask.render_template(
            "signup-index.html",
            error=msg,
        )
    email_check = accounting.check_if_disposable_email(SEmail)
    if email_check == 2:
        return flask.render_template("signup-index.html", error="That email is banned!")
    elif email_check == 1:
        return flask.render_template(
            "signup-index.html", error="That email is not valid!"
        )
    if SPassword != SPassword2:
        return flask.render_template(
            "signup-index.html",
            error="Password boxes do not match!",
            SUsername=SUsername,
            SRole=SRole,
            SDisplayname=SDisplayname,
        )
    possible_user = database.find_account({"username": SUsername}, "vid")
    possible_dispuser = database.find_account(
        {"displayName": SDisplayname}, "customization"
    )
    # print("again")
    if (
        possible_user is not None
        or possible_dispuser is not None
        or SUsername in word_lists.banned_usernames
        or SDisplayname in word_lists.banned_usernames
    ):
        return flask.render_template(
            "signup-index.html",
            error="That Username/Display name is already taken!",
            SRole=SRole,
        )
    possible_email = database.find_account({"email": SEmail}, "vid")
    if possible_email is not None:
        return flask.render_template(
            "signup-index.html",
            error="That Email is already used!",
            SEmail=SEmail,
            SUsername=SUsername,
            SDisplayname=SDisplayname,
            SRole=SRole,
        )
    accounting.create_user(SUsername, SPassword, SEmail, SRole, SDisplayname)
    log.log_accounts(f"A user has made a account named {SUsername}")
    return flask.redirect(flask.url_for("login_page"))


@app.route("/signup", methods=["GET"])
def signup_get() -> ResponseReturnValue:
    """Serve the signup page."""
    return flask.render_template("signup-index.html")


@app.route("/verify/<userid>/<verification_code>")
def verify(userid, verification_code):
    """Verify a user."""
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
            return f"{user} has been verified. You may now chat in other chat rooms."
    return "Invalid verification code."


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
        # return flask.render_template("password_part1.html")


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


@app.route("/backup")
@login_required
def get_logs_page() -> ResponseReturnValue:
    """Serve the chat logs (backup)"""
    html_file = flask.render_template("Backup-chat.html")
    return html_file


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
    username = request.form.get("user")
    userid = request.cookies.get("Userid")
    displayname = request.form.get("display")
    role = request.form.get("role")
    messageC = request.form.get("message_color")
    roleC = request.form.get("role_color")
    userC = request.form.get("user_color")
    email = request.form.get("email")
    file = request.files.get("profile")  # if 'profile' in request.files else None
    theme = request.form.get("theme")
    # print(theme)
    user = User.get_user_by_id(userid)
    user_email = database.get_email(user.uuid)
    return_list = {
        "user": username,
        "passwd": "we are not adding password editing just yet",
        "displayName": displayname,
        "role": role,
        "user_color": userC,
        "role_color": roleC,
        "message_color": messageC,
        "profile": file,
        "theme": theme,
        "email": email,
    }
    # print(theme)
    old_path = user.profile
    # print(file)
    profile_location = (
        uploading.upload_file(file, old_path) if file is not None else old_path
    )

    if theme is None:
        return flask.render_template(
            "settings.html", error="Pick a theme before updating!", **return_list
        )

    theme = user.theme if theme == "" else theme
    result, error = accounting.run_regex_signup(username, role, displayname)
    if result is not False:
        return flask.render_template("settings.html", error=error, **return_list)

    if (
        database.find_account({"displayName": displayname}, "customization") is not None
        and user.displayName != displayname
    ) and displayname in word_lists.banned_usernames:
        return flask.render_template(
            "settings.html", error="That Display name is already taken!", **return_list
        )
    email_check = database.find_account({"email": email}, "vid")
    if email_check is None and user_email != email:
        verification_code = accounting.create_verification_code(user)
        accounting.send_verification_email(
            user.username, email, verification_code, user.uuid
        )
    elif email_check is not None and user_email != email:
        return flask.render_template(
            "settings.html", error="that email is taken", **return_list
        )

    if user.locked != "locked":
        database.update_account(
            user.uuid,
            messageC,
            roleC,
            userC,
            displayname,
            role,
            profile_location,
            theme,
            email,
        )
        user.update_account(
            messageC, roleC, userC, displayname, role, profile_location, theme
        )

        resp = flask.make_response(flask.redirect(flask.url_for("chat_page")))
        resp.set_cookie("Username", user.username)
        resp.set_cookie("Theme", theme)
        resp.set_cookie("Profile", profile_location)
        resp.set_cookie("Userid", user.uuid)
        error = "Updated account!"
        return resp
    else:
        if user_email == email:
            return flask.render_template(
                "settings.html",
                error="You must verify your account before you can change settings",
                **return_list,
            )
        database.update_account_set(
            "vid", {"username": username}, {"$set": {"email": email}}
        )
        error = "Updated email!"
    log.log_accounts(f"The account {user} has updated some setting(s)")
    return flask.render_template("settings.html", error=error, **return_list)


##### THEME STUFF #####
@app.route("/editor")
@login_required
def editor():
    return flask.render_template("theme/editor.html")


@app.route("/projects")
@login_required
def projects():
    return flask.render_template("theme/projects.html")


@socketio.on("get_projects")
def handle_project_requests():
    socketid = request.sid
    userid = request.cookies.get("Userid")
    displayname = request.cookies.get("DisplayName").replace('"', "")
    projects = database.get_projects(userid, displayname)
    projects_fixed = []
    # print(projects)
    for project in projects:
        del project["_id"]
        del project['theme']
        if "author" in project and len(project["author"]) > 1:
            project["author"] = project["author"][1:]
        projects_fixed.append(project)
    # print(projects_fixed)
    emit("projects", (projects_fixed), to=socketid)


@socketio.on("create_project")
def handle_projecet_creation():
    socketid = request.sid
    userid = request.cookies.get("Userid")
    user = User.get_user_by_id(userid)
    if user.themeCount >= 3:
        emit("response", ("You have hit your project limit", True), to=socketid)
        return
    print(user.themeCount)
    # displayname = request.cookies.get('DisplayName').replace('"', '')
    while True:
        code = ""
        for _ in range(5):
            code += random.choice(ascii_uppercase)

        if code not in database.get_all_projects():
            break
    project = database.create_project(userid, user.displayName, code)
    user.themeCount += 1
    del project["_id"]
    del project['theme']
    emit("set_theme", project, to=socketid)


@socketio.on("get_project")
def send_project(theme_id):
    socketid = request.sid
    # userid = request.cookies.get('Userid')
    # displayname = request.cookies.get('DisplayName').replace('"', '')
    project = database.get_project(theme_id)
    del project["_id"]
    project['project'] = {}
    if "author" in project and len(project["author"]) > 1:
        project["author"] = project["author"][1:]
    emit("set_theme", project, to=socketid)


@socketio.on("save_project")
def handle_save_project(project):
    socketid = request.sid
    project['author'].insert(0, request.cookies.get('Userid'))
    # user = User.get_user_by_id(request.cookies.get('Userid'))
    # if user.themeCount < 3:
    database.save_project(project)
    emit("response", ("Project Saved", False), to=socketid)
    

@socketio.on("update_theme_status")
def handel_status_change(themeID, status):
    # socketid = request.sid
    # user = User.get_user_by_id(request.cookies.get('Userid'))
    # if user.themeCount < 3:
    database.update_theme_status(themeID, status)
    # emit("response", ("Project Saved", False), to=socketid)


@socketio.on("delete_project")
def handle_delete_project(project):
    socketid = request.sid
    user = User.get_user_by_id(request.cookies.get("Userid"))
    user.themeCount -= 1
    database.delete_project(project)
    emit("response", ("Project Saved", False), to=socketid)


@socketio.on("get_themes")
def handle_theme_requests():
    socketid = request.sid
    # userid = request.cookies.get('Userid')
    # displayname = request.cookies.get('DisplayName').replace('"', '')
    projects = database.get_all_projects()
    projects_fixed = []
    # print(list(projects))
    for project in projects:
        if project["status"] == "private":
            continue
        del project["_id"]
        del project["theme"]
        del project['project']
        del project["status"]
        if "author" in project and len(project["author"]) > 1:
            project["author"] = project["author"][1:]
        projects_fixed.append(project)
    # print(projects_fixed)
    emit("receve_themes", (projects_fixed), to=socketid)


@socketio.on("get_theme")
def send_theme(theme_id):
    socketid = request.sid
    theme = database.get_project(theme_id)
    # print(theme)
    if theme is None:
        theme = database.get_project("dark")
    del theme["_id"]
    del theme['project']
    del theme["author"]
    # del project['themeID']
    del theme["status"]
    # del project['name']
    # print(theme)
    emit("set_theme", theme, to=socketid)


##### END OF THEME STUFF #####


# socketio stuff
# @socketio.on('username')
# def handle_connect(userid, isVisible, location):
#     """Will be used later for online users."""
#     sid = request.sid
#     user = User.get_user_by_id(userid)
#     if user is not None:
#         user.unique_online_list(userid, isVisible, location, sid)
@socketio.on("status_change")
def handle_connect(data):
    """Will be used later for online users."""
    socketid = request.sid
    # user = User.get_user_by_id(request.cookies.get('Userid'))
    update_userlist(socketid, data, request.cookies.get("Userid"))
    # if user is not None:
    #     user.unique_online_list(userid, isVisible, location, sid)


@socketio.on("get_full_list")
def handle_full_list_request():
    socketid = request.sid
    emit("update_list_full", (list(users_list.values())), namespace="/", to=socketid)


@socketio.on("disconnect")
def handle_disconnect():
    """Remove the user from the online user db on disconnect."""
    socketid = request.sid
    userid = request.cookies.get("Userid")

    active_privates = [
        private
        for private in Private.chats.values()
        if (userid in private.userlist and private.active.get(userid, False))
        or socketid in private.sids
    ]

    for private in active_privates:
        private.active[userid] = False
        if socketid in private.sids:
            private.sids.remove(socketid)

    active_chats = [chat for chat in Chat.chats.values() if socketid in chat.sids]

    for chat in active_chats:
        chat.sids.remove(socketid)

    try:
        user = User.get_user_by_id(userid)
        if user is not None and user.status != "offline-locked":
            user.status = "offline"
        database.set_offline(userid)
        # emit('update_list', (list(users_list.values())), brodcast=True)
        if userid is not None:
            update_userlist(socketid, {"status": "offline"}, userid)
        # del socketids[request.cookies.get("Userid")]
    except TypeError:
        pass


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


@socketio.on("message_chat")
def handle_message(_, message, vid, userid, private, hidden):
    # print(hidden)
    handle_chat_message(
        message, vid, userid, hidden
    ) if private == "false" else handle_private_message(message, vid, userid)


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
    emit("room_data", list, to=socketid, namespace="/")


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


"""
@scheduler.task('interval',
                vid='permission_gc',
                seconds=60,
                misfire_grace_time=500)
def update_permission():
    Background task to see if user should be unmuted.
    users = database.find_all_account()
    # filtering.reload_users(e = '1')
    for user_info in users:
        user = user_info['username']
        permission = user_info['permission']
        username = user_info['displayName']

        if filtering.is_user_expired(permission):
            print(f"{username} is no longer muted.")
            database.update_account_set('perm', {"userId": user_info["userId"]},
            {'$set': {"permission": "true"}})
            log.log_mutes(f"{username} is no longer muted.")

        elif filtering.is_warned_expired(permission):
            print(f"{username} warnings have been reset.")
            database.update_account_set('perm', {"userId": user_info["userId"]},
            {'$set': {"warned": "0"}})
            log.log_mutes(f"{username} warnings have been reset.")
        elif accounting.is_account_expired(permission):
            log.log_accounts(
                f'The account {user} has been deleted because it was not verified'
            )
            database.delete_account(user)
"""

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


if __name__ == "__main__":
    # o = threading.Thread(target=online_refresh)
    # o.start()
    socketio.start_background_task(backup_classes)
    socketio.run(app, host="0.0.0.0", debug=True, port=5000)
