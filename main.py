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
import logging
import os

# import time
# import uuid
# from datetime import datetime, timedelta
import flask
from flask import request
from flask.typing import ResponseReturnValue
from flask_apscheduler import APScheduler
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_socketio import SocketIO, emit

# these are the files that do not import dbm
import accounting
import database
import filtering
import log
from private import Private, get_messages, get_messages_list
import uploading
import word_lists
from chat import Chat
from commands.other import end_ping, format_system_msg
from user import User, Users, add_user_class, delete_user, get_user_by_id, login_manager

# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address  #, default_error_responder

scheduler = APScheduler()


def setup_func():
    """sets up the server"""
    if not os.path.exists('static/profiles'):
        os.makedirs('static/profiles')
    if not os.path.exists('backend/accounts.txt'):
        with open('backend/accounts.txt', 'w'):
            pass
    if not os.path.exists('backend/Chat-backup.txt'):
        with open('backend/Chat-backup.txt', 'w'):
            pass
    if not os.path.exists('backend/command_log.txt'):
        with open('backend/command_log.txt', 'w'):
            pass
    if not os.path.exists('backend/permission.txt'):
        with open('backend/permission.txt', 'w'):
            pass
    if not os.path.exists('backend/chat-rooms_log.txt'):
        with open('backend/chat-rooms_log.txt', 'w'):
            pass
    if not os.path.exists('backend/Chat-backup.txt'):
        with open('backend/webserver.log', 'w'):
            pass
    database.setup_chatrooms()

app = flask.Flask(__name__)
app.secret_key = os.urandom(9001)  #ITS OVER 9000!!!!!!

# rate limiting
# limiter = Limiter(get_remote_address,
#                   app=app,
#                   on_breach=default_error_responder)

logging.basicConfig(filename="backend/webserver.log",
                    filemode='a',
                    level=logging.ERROR)
root = logging.getLogger().setLevel(logging.ERROR)

socketio = SocketIO(app)

scheduler.init_app(app)
scheduler.api_enabled = True
database.clear_online()

login_manager.init_app(app)
login_manager.login_view = 'login_page'

# pylint: enable=E0213

# license stuff
if __name__ == "__main__":
    print("Copyright (C) 2023  cserver45, cseven")
    print("License info can be viewed in main.py or the LICENSE file.")


@app.route('/chat')
@login_required
def chat_page() -> ResponseReturnValue:
    """Serve the main chat window."""
    return flask.render_template('chat.html')


@app.route('/chat/<room_name>')
@login_required
def specific_chat_page(room_name) -> ResponseReturnValue:
    """Get the specific room in the uri."""
    # later we can set this up to get the specific room (with permssions)
    # request.cookies.get('Userid')
    print(room_name)
    return flask.redirect(flask.url_for("chat_page"))


@app.route('/Private/<private_chat>')
@login_required
def specific_private_page(private_chat) -> ResponseReturnValue:
    """Get the specific private chat in the uri."""
    # later we can set this up to get the specific room (with permssions)
    # request.cookies.get('Userid')
    print(private_chat)
    return flask.redirect(flask.url_for("chat_page"))


@app.route('/logout')
@login_required
def logout():
    """Log out the current user"""
    delete_user(request.cookies.get("Userid"))
    # emit("force_username", ("", None), brodcast=True)
    logout_user()
    return flask.redirect(flask.url_for('login_page'))


@app.route('/login', methods=["POST", "GET"])
@app.route('/', methods=['GET', 'POST'])
def login_page() -> ResponseReturnValue:
    """Show the login page."""
    # print(current_user,'current user')
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for('chat_page'))

    if request.method == "POST":
        # redo client side checks here on server side, like signup
        username = request.form.get("username")
        password = request.form.get("password")
        TOSagree = request.form.get("TOSagree")
        next_page = request.args.get("next")
        user = database.find_login_data(username, False)
        # print(userids)
        if user is None:
            return flask.render_template('login.html',
                                         error="That account does not exist!")
        # userid = user["userId"]
        if TOSagree != "on":
            return flask.render_template('login.html',
                                         error='You did not agree to the TOS!')

        if User.check_username(
                username, user["username"]) and User.check_password(
                    user['password'], password):
            user_obj = add_user_class(username, user["status"], user["SPermission"],
                                      user["displayName"], user["userId"])
            login_user(user_obj)
            if next_page is None:
                next_page = flask.url_for('chat_page')
            else:
                if next_page not in word_lists.approved_links:
                    next_page = flask.url_for('chat_page')
            resp = flask.make_response(flask.redirect(next_page))
            resp.set_cookie('Username', user['username'])
            resp.set_cookie('Theme', user['theme'])
            resp.set_cookie('Profile', user['profile'] if user["profile"] != "" else \
                '/static/favicon.ico')
            resp.set_cookie('Userid', user['userId'])
            resp.set_cookie('DisplayName', user["displayName"])
            return resp
        else:
            return flask.render_template(
                'login.html', error="That username or password is incorrect!")
    else:
        return flask.render_template('login.html')


# @app.route('/changelog')
# def changelog_page() -> ResponseReturnValue:
#     """Serve the changelog, so old links don't break."""
#     html_file = flask.render_template('update-log.html')
#     return html_file

# we should retire the above link

# custom error message for signup, instead of generic 429 error
#def signup_ratelimit_error_responder(request_limit: RequestLimit):
#    return jsonify({"error": "rate_limit_exceeded"})
# yes ik the stuff above is horibbly broken, but the other stuff is fine


@app.route('/signup', methods=["POST"])
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
        return flask.render_template("signup-index.html",
                                     error='That email is banned!')
    elif email_check == 1:
        return flask.render_template("signup-index.html",
                                     error='That email is not valid!')
    if SPassword != SPassword2:
        return flask.render_template("signup-index.html",
                                     error='Password boxes do not match!',
                                     SUsername=SUsername,
                                     SRole=SRole,
                                     SDisplayname=SDisplayname)
    possible_user = database.find_account({'username': SUsername}, 'id')
    possible_dispuser = database.find_account({'displayName': SDisplayname},
                                              'customization')
    # print("again")
    if possible_user is not None or possible_dispuser is not None or SUsername in \
        word_lists.banned_usernames or SDisplayname in word_lists.banned_usernames:
        return flask.render_template(
            "signup-index.html",
            error='That Username/Display name is already taken!',
            SRole=SRole)
    possible_email = database.find_account({"email": SEmail}, 'id')
    if possible_email is not None:
        return flask.render_template("signup-index.html",
                                     error='That Email is allready used!',
                                     SEmail=SEmail,
                                     SUsername=SUsername,
                                     SDisplayname=SDisplayname,
                                     SRole=SRole)
    accounting.create_user(SUsername, SPassword, SEmail, SRole, SDisplayname)
    log.log_accounts(f'A user has made a account named {SUsername}')
    return flask.redirect(flask.url_for('login_page'))


@app.route('/signup', methods=["GET"])
def signup_get() -> ResponseReturnValue:
    """Serve the signup page."""
    return flask.render_template('signup-index.html')


@app.route('/verify/<userid>/<verification_code>')
def verify(userid, verification_code):
    """Verify a user."""
    user_id = database.find_account({"userId": userid}, 'id')
    if user_id is not None:
        user_code = accounting.create_verification_code(user_id)
        if user_code == verification_code:
            database.update_account_set('perm', {"userId": user_id["userId"]},
                                        {'$set': {
                                            "locked": "false"
                                        }})
            user = user_id["username"]
            log.log_accounts(
                f'The account {user} is now verified and may now chat in any chat room.'
            )
            return f"{user} has been verified. You may now chat in other chat rooms."
    return "Invalid verification code."


@app.route('/backup')
@login_required
def get_logs_page() -> ResponseReturnValue:
    """Serve the chat logs (backup)"""
    html_file = flask.render_template('Backup-chat.html')
    return html_file


@app.route('/settings', methods=['GET'])
@login_required
def settings_page() -> ResponseReturnValue:
    """Serve the settings page for the user."""
    user = database.find_login_data(request.cookies.get('Userid'), True)
    if request.cookies.get('Userid') != user['userId']:
        # someone is trying something funny
        return flask.Response(
            "Something funny happened. Try Again (Unauthorized)", status=401)

    return flask.render_template(
        'settings.html',
        user=user['username'],
        passwd='we are not adding password editing just yet',
        email=user["email"],
        displayName=user["displayName"],
        role=user["role"],
        user_color=user["userColor"],
        role_color=user["roleColor"],
        message_color=user["messageColor"],
        profile=user["profile"],
        theme=user["theme"])


@app.route('/settings', methods=['POST'])
@login_required
def customize_accounts() -> ResponseReturnValue:
    """Customize the account."""
    username = request.form.get("user")
    userid = request.cookies.get('Userid')
    displayname = request.form.get("display")
    role = request.form.get("role")
    messageC = request.form.get("message_color")
    roleC = request.form.get("role_color")
    userC = request.form.get("user_color")
    email = request.form.get("email")
    file = request.files['profile']
    theme = request.form.get("theme")
    user = database.find_account_data(userid)
    return_list = {
        "user": username,
        "passwd": 'we are not adding password editing just yet',
        "displayName": displayname,
        "role": role,
        "user_color": userC,
        "role_color": roleC,
        "message_color": messageC,
        "profile": file,
        "theme": theme,
        "email": email
    }
    # print(theme)
    old_path = user["profile"]
    # print()
    profile_location = uploading.upload_file(file, old_path) if file.filename != '' else \
    old_path
    if theme is None:
        return flask.render_template("settings.html",
                                     error='Pick a theme before updating!',
                                     **return_list)

    theme = user['theme'] if theme == '' else theme
    result, error = accounting.run_regex_signup(username, role, displayname)
    if result is not False:
        return flask.render_template("settings.html",
                                     error=error,
                                     **return_list)

    if (database.find_account({"displayName": displayname}, 'customization')
            is not None and user["displayName"] != displayname
        ) and displayname in word_lists.banned_usernames:
        return flask.render_template(
            "settings.html",
            error='That Display name is already taken!',
            **return_list)
    email_check = database.find_account({"email": email}, 'id')
    if (email_check is None and user["email"] != email):
        verification_code = accounting.create_verification_code(user)
        accounting.email_var_account(user["username"], email,
                                     verification_code, user['userid'])
    elif (email_check is not None and user["email"] != email):
        return flask.render_template("settings.html",
                                     error='that email is taken',
                                     **return_list)

    if user['locked'] != 'locked':
        database.update_account(user["userId"], messageC, roleC, userC, displayname,
                                role, profile_location, theme, email)

        resp = flask.make_response(flask.redirect(flask.url_for('chat_page')))
        resp.set_cookie('Username', user['username'])
        resp.set_cookie('Theme', theme)
        resp.set_cookie('Profile', profile_location)
        resp.set_cookie('Userid', user['userId'])
        error = "Updated account!"
        return resp
    else:
        if user['email'] == email:
            return flask.render_template(
                'settings.html',
                error=
                'You must verify your account before you can change settings',
                **return_list)
        database.update_account_set('id', {"username": username},
                                    {'$set': {
                                        "email": email
                                    }})
        error = 'Updated email!'
    log.log_accounts(f'The account {user} has updated some setting(s)')
    return flask.render_template('settings.html', error=error, **return_list)


# socketio stuff
@socketio.on('username')
def handle_connect(userid: str, location):
    """Will be used later for online users."""
    sid = request.sid
    # for user in Users.values():
        # user.status = 'offline' if user.status != 'offline-locked' else 'offline-locked'
    user = get_user_by_id(userid)
    if user is not None:
        user.unique_online_list(userid, location, sid)


@socketio.on('disconnect')
def handle_disconnect():
    """Remove the user from the online user db on disconnect."""
    try:
        user = get_user_by_id(request.cookies.get('Userid'))
        if user is not None and user.status != "offline-locked":
            user.status = 'offline'
        database.set_offline(request.cookies.get('Userid'))
        emit("force_username", ("", None), broadcast=True)
    except TypeError:
        pass


@socketio.on("get_rooms")
def get_rooms(userid):
    """Grabs the chat rooms."""
    user_name = database.find_account({"userId": userid}, 'perm')
    user = database.find_account({"userId": userid},
                                 'customization')["displayName"]
    room_access = database.get_rooms()  # rooms.get_chat_rooms()
    permission = user_name["locked"].split(' ')
    # print(room_access)

    if user_name["SPermission"] == "Debugpass":
        emit('roomsList', (room_access, 'dev'), namespace='/', to=request.sid)
    elif user_name['SPermission'] == "modpass":
        rooms_to_remove = []
        for r in room_access:
            if r['whitelisted'] == 'devonly':
                # this could be simplfied into one for loop you know
                rooms_to_remove.append(r)

        for r in rooms_to_remove:
            room_access.remove(r)
        emit('roomsList', (room_access, 'mod'), namespace='/', to=request.sid)
    elif permission[0] == "locked":
        emit('roomsList', ([{
            'id': 'zxMhhAPfWOxuZylxwkES',
            'name': ''
        }], 'locked'),
             namespace='/',
             to=request.sid)
    else:
        accessible_rooms = [
            {
                'id': r['id'],
                'name': r['name']
            } for r in room_access if
            ((r['blacklisted'] == 'empty' and r['whitelisted'] == 'everyone')
             or (r['whitelisted'] != 'everyone'
                 and 'users:' in r['whitelisted'] and user in [
                     u.strip()
                     for u in r['whitelisted'].split("users:")[1].split(",")
                 ]) or
             (r['blacklisted'] != 'empty' and 'users:' in r['blacklisted']
              and user not in [
                  u.strip()
                  for u in r['blacklisted'].split("users:")[1].split(",")
              ] and r['whitelisted'] == 'everyone')) and
            (
                # user_name['username'] == r['generatedBy']
                # or user_name['displayName'] == r['mods']) and (
                r['whitelisted'] != 'devonly' or r['whitelisted'] != 'modonly'
                or r['whitelisted'] != 'lockedonly')
        ]

        # print(accessible_rooms)

        emit('roomsList', (accessible_rooms, user_name['locked']),
             namespace='/',
             to=request.sid)


@socketio.on('message_chat')
def handle_message(_, message, id, userid, private):
    handle_chat_message(message, id, userid) if private == 'false' else \
        handle_private_message(message, id, userid)


def handle_chat_message(message, roomid, userid):
    """New New chat message handling pipeline."""
    # print(roomid)
    # later I will check the if the username is the same as the one for the session somehow
    
    room = Chat.create_or_get_chat(roomid)
    
    # print(room)
    user = database.find_account_data(userid)
    result = filtering.run_filter_chat(user, room, message, roomid, userid)
    if result[0] == 'msg':
        if room is not None:
            room.add_message(result[1])
            emit("message_chat", (result[1], roomid), broadcast=True)
            # addons.message_addons(message, user, roomid, room)
            # above is not offical again, so commented out
            if "$sudo" in message and result[2] != 3:
                filtering.find_cmds(message, user, roomid)
            elif '$sudo' in message and result[2] == 3:
                filtering.failed_message(('permission', 9), roomid)
        else:
            filtering.failed_message("return", roomid)
    else:
        filtering.failed_message(result, roomid)


def handle_private_message(message, pmid, userid):
    """New New chat message handling pipeline."""
    user = database.find_account_data(userid)
    result = filtering.run_filter_private(user, message, userid)
    private = get_messages(pmid)
    if result[0] == 'msg':
        private.add_message(result[1], userid)
        emit("message_chat", (result[1], pmid), broadcast=True)
        if "$sudo" in message and result[2] != 3:
            filtering.find_cmds(message, user, pmid)
        # if "$sudo" in message and result[2] != 3:
        #     filtering.find_cmds(message, user, roomid)
        # elif '$sudo' in message and result[2] == 3:
        #     filtering.failed_message(('permission', 9), roomid)
    # else:
    #     filtering.failed_message(result, roomid)


@socketio.on('pingtest')
def handle_ping_tests(start, roomid):
    """Respond with the start time, so ping times can be calculated"""
    end_ping(start, roomid)


@socketio.on("room_connect")
def connect(roomid):
    """Switch rooms for the user"""
    socketid = request.sid
    try:
        # room = database.get_room_msg_data(
        #     roomid)  # WHY ERROR YOU WORK NOW WORK
        # ah yes the best kind of error
        room = Chat.create_or_get_chat(roomid)
        list = {"roomid": room.id, "name": room.name, "msg": room.messages}
    except TypeError:
        emit('room_data', "failed", namespace='/', to=socketid)
        return
    # don't need to let the client know the mongodb id
    # del room['_id']
    # print(room)

    emit("room_data", list, to=socketid, namespace='/')


@socketio.on("private_connect")
def private_connect(sender, receiver, roomid):
    """Switch rooms for the user"""
    socketid = request.sid
    receiverid = database.find_userid(receiver)
    if sender == receiverid:
        emit("message_chat", (
            "[SYSTEM]: <font color='#ff7f00'>Don't be a loaner get some friends.</font>",
            roomid),
             namespace="/")
        return

    chat = get_messages_list(sender, receiverid)
    # print(sender, receiver)
    emit("private_data", {'message': chat.messages, 'pmid': chat.id, \
        'name': receiver}, to=socketid, namespace='/')


"""
@scheduler.task('interval',
                id='permission_gc',
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
            database.update_account_set('perm', {"userId": user_info["userId"]}, {'$set': {"permission": "true"}})
            log.log_mutes(f"{username} is no longer muted.")

        elif filtering.is_warned_expired(permission):
            print(f"{username} warnings have been reset.")
            database.update_account_set('perm', {"userId": user_info["userId"]}, {'$set': {"warned": "0"}})
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


@socketio.on('connect')
def emit_on_startup():
    global startup_msg
    if startup_msg:
        emit("message_chat", (format_system_msg("Server is back online!"),
                              'ilQvQwgOhm9kNAOrRqbr'),
             broadcast=True,
             namespace='/')
        startup_msg = False
        emit("force_username", ("", None), brodcast=True)


@socketio.on('online_refresh')
def online_refresh():
    """Background task for online list"""
    while True:
        # database.clear_online()
        socketio.emit("force_username", ("", None))
        socketio.sleep(5)  # this is using a socketio refresh
        
@socketio.on('chat_backups')
def backup_chats(exception=None):
    """Runs after each request."""
    while True:
        for chat_instance in Chat.chats.values():
            chat_instance.backup_data() 
        for private_instance in Private.chats.values():
            private_instance.backup_data()
        socketio.sleep(4)
        
@app.teardown_appcontext
def teardown_request(exception=None):
    """Runs after each request."""
    chat_chats_copy = dict(Chat.chats)
    for chat_id, chat_instance in chat_chats_copy.items():
        chat_instance.backup_data() 
    private_chats_copy = dict(Private.chats)
    for private_id, private_instance in private_chats_copy.items():
        private_instance.backup_data() 
    socketio.sleep(4)

if __name__ == "__main__":
    # o = threading.Thread(target=online_refresh)
    # o.start()
    setup_func()
    socketio.start_background_task(online_refresh)
    socketio.start_background_task(backup_chats)
    socketio.run(app, host="0.0.0.0", debug=True, port=5000)
