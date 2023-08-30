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
import os
import logging
import hashlib
# import keys
import re
import flask
import pymongo
import uuid
from flask import request
from flask.typing import ResponseReturnValue
from flask_socketio import SocketIO, emit
from flask_apscheduler import APScheduler
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address  #, default_error_responder
from datetime import datetime, timedelta

client = pymongo.MongoClient(os.environ["mongo_key"])
dbm = client.Chat
scheduler = APScheduler()

import chat
import cmds
import filtering
import rooms
import accounting
import log

LOGFILE = "backend/chat.txt"

app = flask.Flask(__name__)
app.config['SECRET'] = os.urandom(9001)  #ITS OVER 9000!!!!!!

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

# clear db, so that old users don't stay
dbm.Online.delete_many({})

# note for later: rename profanity_words.py to word_lists.py and move this there
# along with any other static lists
banned_usernames = ('Admin', 'admin', '[admin]', '[ADMIN]', 'ADMIN', '[Admin]',
                    '[URL]', 'mod', 'Mod', '[mod]', '[Mod]', '[MOD]', 'MOD',
                    'SYSTEM', '[SYSTEM]', "SONG", "[Song]", "[SONG]", "[song]",
                    " ", "  ", "   ", "cseven", "cserver", 'system',
                    '[system]', '[System]', 'System')

# license stuff
if __name__ == "__main__":
    print("Copyright (C) 2023  cserver45, cseven")
    print("License info can be viewed in main.py or the LICENSE file.")


# easter egg time lol
@app.route("/f")
def f_but_better() -> ResponseReturnValue:
    """Not an easter egg I promise."""
    return flask.redirect(flask.url_for('signup'))


# this will not make sense for a little bit
@app.route('/defnotchat')
def chat_page() -> ResponseReturnValue:
    """Serve the main chat, stops bypass bans."""
    html_file = flask.render_template('chat.html')
    return html_file


@app.route('/', methods=["POST", "GET"])
def login_page() -> ResponseReturnValue:
    """Show the login page"""
    if request.method == "POST":
        # redo client side checks here on server side, like signup
        username = request.form.get("username")
        password = request.form.get("password")
        TOSagree = request.form.get("TOSagree")
        try:
            # not 100% sure this will catch a failed attempt, doesnt get them
            user = dbm.Accounts.find_one({"username": username})
            if user is None:
                return flask.render_template(
                    'login.html', error="That account does not exist!")
        except TypeError:
            return flask.render_template('login.html',
                                         error="That account does not exist!")
        if TOSagree != "on":
            return flask.render_template('login.html',
                                         error='You did not agree to the TOS!')
        if username == user["username"] and hashlib.sha384(
                bytes(password, 'utf-8')).hexdigest() == user["password"]:
            # I have no idea if this will work, and it shoulden't, but lets see
            # exactly what I thought, hmmmmm
            # its because there is no socketid here, how to get said id hm
            """emit("return_prefs", {
                "displayName": user["displayName"],
                "profile": user["profile"],
                "theme": user["theme"],
            },
                 namespace="/")"""
            return flask.render_template(
                'chat.html', user=username
            )  # this could be a security issue later on (if they figure out this) this is how most things do it so we are file
        else:
            return flask.render_template(
                'login.html', error="That username or password is incorrect!")
    else:
        return flask.render_template('login.html')


# @app.route('/changelog')
# def changelog_page() -> ResponseReturnValue:
#     """Serve the changelog, so old links don't break (after making the main page be the changelog)."""
#     html_file = flask.render_template('update-log.html')
#     return html_file

# custom error message for signup, instead of generic 429 error
#def signup_ratelimit_error_responder(request_limit: RequestLimit):
#    return jsonify({"error": "rate_limit_exceeded"})
# yes ik the stuff above is horibbly broken, but the other stuff is fine


@app.route('/signup', methods=["POST"])
# @limiter.limit("1 per day")
def signup_post() -> ResponseReturnValue:
    """The creating of an account."""
    global verification_code_list
    global verification_code
    SUsername = request.form.get("SUsername")
    SPassword = request.form.get("SPassword")
    SPassword2 = request.form.get("SPassword2")
    SRole = request.form.get("SRole")
    SDisplayname = request.form.get("SDisplayname")
    SEmail = request.form.get("SEmail")

    if bool(re.search(r'[\s\[,"\'<>{\]]', SUsername)) is True:
        return flask.render_template(
            "signup-index.html",
            error='The display name contains a space or a special character.',
        )
    elif bool(re.search(r'[\s[,"\'<>{\]]', SUsername)) is True:
        return flask.render_template(
            "signup-index.html",
            error='The username contains a space or a special character.',
        )
    elif bool(re.search(r'[\s[,"\'<>{\]]', SRole)) is True:
        return flask.render_template(
            "signup-index.html",
            error='The Role contains a space or a special character.',
        )
    check = r'^[A-Za-z]{3,12}$'
    user_allowed = re.match(
        check, SUsername
    )  # and not re.search(r'dev|mod', SUsername, re.IGNORECASE) #The and needs to be moved to a seperate one to check for letter limit
    desplayname_allowed = re.match(
        check, SDisplayname
    )  # and not re.search(r'dev|mod', SDisplayname, re.IGNORECASE)
    if re.match(r'^[A-Za-z]{3,18}$', SRole) is True:
        return flask.render_template(
            "signup-index.html",
            error='That Role name is too long. It must be at least 1 letter long or under 18 and under.',
        )
        
    if user_allowed == 'false' or desplayname_allowed == 'false':
        return flask.render_template(
            "signup-index.html",
            error=
            'That Username/Display name is too long. It must be at least 1 letter long or 12 and under',
            # error='That Username/Display name is not allowed!',
            SRole=SRole,
        )
    if SPassword != SPassword2:
        return flask.render_template("signup-index.html",
                                     error='Password boxes do not match!',
                                     SUsername=SUsername,
                                     SRole=SRole,
                                     SDisplayname=SDisplayname)
    possible_user = dbm.Accounts.find_one({"username": SUsername})
    possible_dispuser = dbm.Accounts.find_one({"displayName": SDisplayname})
    if possible_user is not None or possible_dispuser is not None or SUsername in banned_usernames or SDisplayname in banned_usernames:
        return flask.render_template(
            "signup-index.html",
            error='That Username/Display name is already taken!',
            SRole=SRole)
    possible_email = dbm.Accounts.find_one({"email": SEmail})
    if possible_email is not None:
        return flask.render_template("signup-index.html",
                                     error='That Email is allready used!',
                                     SEmail=SEmail,
                                     SUsername=SUsername,
                                     SDisplayname=SDisplayname,
                                     SRole=SRole)
    verification_code = str(uuid.uuid4())
    current_time = datetime.now()
    time = current_time + timedelta(hours=10)
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S")
    dbm.Accounts.insert_one({
        "username":
        SUsername,
        "password":
        hashlib.sha384(bytes(SPassword, 'utf-8')).hexdigest(),
        "userId":
        verification_code,
        "email":
        SEmail,
        "role":
        SRole,
        "profile":
        "",
        "theme":
        "dark",
        "displayName":
        SDisplayname,
        "messageColor":
        "#ffffff",
        "roleColor":
        "#ffffff",
        "userColor":
        "#ffffff",
        "permission":
        f"locked {formatted_time}",
        "warned":
        '0',
        "SPermission":
        ""
    })
    accounting.email_var_account(SUsername, SEmail, verification_code)
    accounting.log_accounts(f'A user has made a account named {SUsername}')
    return flask.redirect(flask.url_for('login_page'))


@app.route('/signup', methods=["GET"])
def signup_get() -> ResponseReturnValue:
    """Serve the signup page."""
    return flask.render_template('signup-index.html')


@app.route('/verify/<verification_code>')
def verify(verification_code):
    user_id = dbm.Accounts.find_one({"userId": verification_code})
    if user_id is not None:
        dbm.Accounts.update_one({"userId": verification_code},
                                {"$set": {
                                    "permission": 'true'
                                }})
        user = user_id["username"]
        accounting.log_accounts(
            f'The account {user} has been verified and may now chat in any chat room'
        )
        return f"User: {user} has been verified You may now chat in any chat room you like"
    return "Invalid verification code."


@app.route('/backup')
def get_logs_page() -> ResponseReturnValue:
    """Serve the chat logs (backup)"""
    html_file = flask.render_template('Backup-chat.html')
    return html_file


@app.route('/customizepagereal')
def settings_page() -> ResponseReturnValue:
    """this is the settings page"""
    return flask.render_template('settings.html')


@app.route('/settings', methods=['GET', 'POST'])
def customize_accounts() -> ResponseReturnValue:
    """customize the accounts"""
    if request.method == "POST":
        if 'login' in request.form:
            username = request.form.get("username")
            password = request.form.get("password")
            TOSagree = request.form.get("TOSagree")
            try:
                # not 100% sure this will catch a failed attempt, doesnt get them
                user = dbm.Accounts.find_one({"username": username})
                if user is None:
                    return flask.render_template(
                        'login.html', error="That account does not exist!")
            except TypeError:
                return flask.render_template(
                    'login.html', error="That account does not exist!")
            if TOSagree != "on":
                return flask.render_template(
                    'login.html', error='You did not agree to the TOS!')
            if user["permission"].split(' ') == 'locked':
                return flask.render_template(
                    'login.html',
                    error=
                    'You must verifiy your account before you can customize it!'
                )
            if username == user["username"] and hashlib.sha384(
                    bytes(password, 'utf-8')).hexdigest() == user["password"]:
                return flask.render_template(
                    'settings.html',
                    user=username,
                    passwd=
                    'we are not adding password editing just yet',  #hashlib.sha384(bytes(password, 'utf-8')).hexdigest(),
                    email=user["email"],
                    displayName=user["displayName"],
                    role=user["role"],
                    user_color=user["userColor"],
                    role_color=user["roleColor"],
                    message_color=user["messageColor"],
                    profile=user["profile"],
                    theme=user["theme"])
            else:
                return flask.render_template(
                    'login.html',
                    error="That username or password is incorrect!")
        elif 'update' in request.form:
            userid = request.form.get("user")
            displayname = request.form.get("display")
            role = request.form.get("role")
            messageC = request.form.get("message_color")
            roleC = request.form.get("role_color")
            userC = request.form.get("user_color")
            email = request.form.get("email")
            # passwd = request.form.get("password")
            profile = request.form.get("profile")
            theme = request.form.get("theme")
            user = dbm.Accounts.find_one({"username": userid})
            return_list = {
                "user": userid,
                "passwd": 'we are not adding password editing just yet',
                "displayName": displayname,
                "role": role,
                "user_color": userC,
                "role_color": roleC,
                "message_color": messageC,
                "profile": profile,
                "theme": theme,
                "email": email
            }
            if theme is None:
                return flask.render_template(
                    "settings.html",
                    error='Pick a theme before updating!',
                    **return_list)
            if (dbm.Accounts.find_one({"displayName": displayname}) is not None
                    and user["displayName"]
                    != displayname) and displayname in banned_usernames:
                return flask.render_template(
                    "settings.html",
                    error='That Display name is already taken!',
                    **return_list)
            if bool(re.search(r'[\s\[,"\'<>{\]]', displayname)) is True:
                return flask.render_template(
                    "settings.html",
                    error='The display name contains a space or a special character.',
                )
            elif bool(re.search(r'[\s[,"\'<>{\]]', role)) is True:
                return flask.render_template(
                    "settings.html",
                    error='The Role contains a space or a special character.',
                )
            if (dbm.Accounts.find_one({"email": email}) is None
                    and user["email"] != email):
                verification_code = str(uuid.uuid4())
                # print(verification_code)
                dbm.Accounts.update_one(
                    {'username': userid},
                    {"$set": {
                        'userId': verification_code
                    }})
                accounting.email_var_account(
                    user["username"], email, verification_code
                )  # it gets a invalid code when the verify link is perssed
            elif (dbm.Accounts.find_one({"email": email}) is not None
                  and user["email"] != email):
                return flask.render_template("settings.html",
                                             error='that email is taken',
                                             **return_list)
            # if passwd != user["password"]: #need to make a check if they are not changing or we can just remove password changing from this methid to somthing else
            #     return flask.render_template("settings.html",
            #          error='Your password must not match your current one.',
            # **return_list)
            if bool(re.search(r'[\s[,"\'<>{\]]', displayname)) is True:
                return flask.render_template(
                    "settings.html",
                    error=
                    'The display name contains a space or a special character.',
                    **return_list)
            check = r'^[A-Za-z]{3,12}$'
            # user_allowed = re.match(check, user)# and not re.search(r'dev|mod', SUsername, re.IGNORECASE)
            desplayname_allowed = re.match(
                check, displayname
            )  # and not re.search(r'dev|mod', SDisplayname, re.IGNORECASE)
            if desplayname_allowed == 'false':
                return flask.render_template(
                    "settings.html",
                    error='That Display name is not allowed!',
                    **return_list)

            dbm.Accounts.update_one(
                {"username": userid},
                {
                    "$set": {
                        "messageColor": messageC,
                        "roleColor": roleC,
                        "userColor": userC,
                        "displayName": displayname,
                        "role": role,
                        "profile": profile,
                        "theme": theme,
                        "email": email
                        # "username": userid,
                        # "password": hashlib.sha384(bytes(passwd, 'utf-8')).hexdigest()
                    }
                })
            accounting.log_accounts(
                f'The account {user} has updated some settings (one day ill add what they updated)'
            )
            return flask.render_template('settings.html',
                                         error="updated account",
                                         **return_list)
    else:
        return flask.render_template('login.html')


@app.get('/backup_logs')
def get_backup_chat():
    """Return the backup-chat.txt contents."""
    ret_val = chat.get_chat("Chat-backup")
    return ret_val


# socketio stuff
@socketio.on('username')
def handle_connect(username: str, location):
    """Will be used later for online users."""
    socketid = request.sid
    username_list = []
    icons = {'settings': '⚙️', 'chat': ''}

    dbm.Online.insert_one({
        "username": username,
        "socketid": socketid,
        "location": location
    })

    for key in dbm.Online.find():
        user_info = key["username"]
        icon = icons.get(key.get("location"))
        user_info = f"{icon}{user_info}"
        username_list.append(user_info)

    emit("online", username_list, broadcast=True)


@socketio.on('disconnect')
def handle_disconnect():
    """Remove the user from the online user db on disconnect."""
    socketid = request.sid
    try:
        dbm.Online.delete_one({"socketid": socketid})
        username_list = []
        for key in dbm.Online.find():
            username_list.append(key["username"])
        emit("online", username_list, broadcast=True)
    except TypeError:
        pass


@socketio.on('login')
def login_handle(username, password):
    """make the login work."""
    try:
        # not 100% sure this will catch a failed attempt, doesnt get them
        user = dbm.Accounts.find_one({"username": username})
    except TypeError:
        emit("login_att", "failed", namespace="/")
    if username == user["username"] and hashlib.sha384(bytes(
            password, 'utf-8')).hexdigest() == user["password"]:
        emit("login_att", "true", namespace="/")
    else:
        emit("login_att", "failed", namespace="/")


@socketio.on('get_prefs')
def return_user_prefs(username):
    """Return roles, colors, and theme to logged in user."""
    user = dbm.Accounts.find_one({"username": username})

    try:
        emit("return_prefs", {
            "displayName": user["displayName"],
            "profile": user["profile"],
            "theme": user["theme"],
        },
             namespace="/")
    except TypeError:
        emit("return_prefs", {"failed": True}, namespace="/")


@socketio.on('username_msg')
def handle_online(username: str):
    """Add username to currently online people list."""
    dbm.Online.update_one({"socketid": request.sid},
                          {"$set": {
                              "username": username
                          }})
    username_list = []
    for key in dbm.Online.find():
        username_list.append(key["username"])
    emit("online", username_list, broadcast=True)


@socketio.on("get_rooms")
def get_rooms(username):
    """Grabs the chat rooms."""
    user_name = dbm.Accounts.find_one({"username": username})
    user = user_name["displayName"]
    room_access = rooms.get_chat_rooms()
    permission = user_name["permission"].split(' ')
    if user_name["SPermission"] == "Debugpass":
        emit('roomsList', room_access, namespace='/', to=request.sid)
    elif user_name['SPermission'] == "modpass":
        rooms_to_remove = []
        for r in room_access:
            if (r['whitelisted'] == 'devonly'):
                # this could be simplfied into one for loop you know
                rooms_to_remove.append(r)

        for r in rooms_to_remove:
            room_access.remove(r)
        emit('roomsList', room_access, namespace='/', to=request.sid)
    elif permission[0] == "locked":
        emit('roomsList', [{
            'id': 'ilQvQwgOhm9kNAOrRqbr',
            'name': 'e'
        }],
             namespace='/',
             to=request.sid)
    else:
        accessible_rooms = [{
            'id': r['id'],
            'name': r['name']
        } for r in room_access if (
            (r['blacklisted'] == 'empty' and r['whitelisted'] == 'everyone') or
            (r['whitelisted'] != 'everyone' and 'users:' in r['whitelisted']
             and user in [
                 u.strip()
                 for u in r['whitelisted'].split("users:")[1].split(",")
             ]) or (r['blacklisted'] != 'empty'
                    and 'users:' in r['blacklisted'] and user not in [
                        u.strip()
                        for u in r['blacklisted'].split("users:")[1].split(",")
                    ] and r['whitelisted'] == 'everyone')
        ) and (r['whitelisted'] != 'devonly' or r['whitelisted'] != 'modonly')]
        emit('roomsList', accessible_rooms, namespace='/', to=request.sid)


# pylint: disable=C0103
@socketio.on('message_chat')
def handle_message(user_name, message, roomid):
    """New New chat message handling pipeline."""
    room = dbm.rooms.find_one({"roomid": roomid})
    user = dbm.Accounts.find_one({"username": user_name})
    if dbm.rooms.find_one({"roomid": roomid}) is None:
        result = ("Permission", 6)
    else:
        result = filtering.run_filter(user, room, message, roomid)
    if result[0] == 'msg':
        if dbm.rooms.find_one({"roomid": roomid}) is not None:
            chat.add_message(result[1], roomid, room)
            emit("message_chat", (result[1], roomid), broadcast=True)
            if "$sudo" in message and result[2] != 3:
                filtering.find_cmds(message, user, roomid)
            elif '$sudo' in message and result[2] == 3:
                filtering.failed_message(('permission', 9), roomid, user)
        else:
            filtering.failed_message("return", roomid, user)
    else:
        filtering.failed_message(result, roomid, user)


# pylint: enable=C0103


@socketio.on('pingtest')
def handle_ping_tests(start, roomid):
    """Respond with the start time, so ping times can be calculated"""
    cmds.end_ping(start, roomid)


@socketio.on("room_connect")
def connect(roomid):
    """Switch rooms for the user"""
    socketid = request.sid
    try:
        room = dbm.rooms.find_one({"roomid": roomid})
    except TypeError:
        emit('room_data', "failed", namespace='/', to=socketid)
    # don't need to let the client know the mongodb id
    del room['_id']

    emit("room_data", room, to=socketid, namespace='/')


@scheduler.task('interval',
                id='permission_gc',
                seconds=60,
                misfire_grace_time=500)
def update_permission():
    """Background task to see if user should be unmuted."""
    users = dbm.Accounts.find()
    for user_info in users:
        user = user_info['username']
        permission = user_info['permission']
        username = user_info['displayName']

        if filtering.is_user_expired(permission):
            print(f"{username} is no longer muted.")
            dbm.Accounts.update_one({'username': user},
                                    {'$set': {
                                        'permission': 'true'
                                    }})
            log.log_mutes(f"{username} is no longer muted.")

        elif filtering.is_warned_expired(permission):
            print(f"{username} warnings have been reset.")
            dbm.Accounts.update_one({'username': user},
                                    {'$set': {
                                        'warned': '0'
                                    }})
            log.log_mutes(f"{username} warnings have been reset.")
        elif accounting.is_account_expired(permission):
            accounting.log_accounts(
                f'The account {user} has been deleted because it was not verified'
            )
            dbm.Accounts.delete_one({'username': user})


# start background tasks should we move this down to 533?
scheduler.start()
startup_msg = True


@socketio.on('connect')
def emit_on_startup():
    global startup_msg
    if startup_msg:
        emit("message_chat",
             ("[SYSTEM]: <font color='#ff7f00'>Server is back online!</font>",
              'ilQvQwgOhm9kNAOrRqbr'),
             broadcast=True,
             namespace='/')
        startup_msg = False


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8080)
