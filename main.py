"""Main webserver file"""
import os
import logging
import hashlib
import keys
import flask
import pymongo
import re
from flask import request
from flask.logging import default_handler
from flask.typing import ResponseReturnValue
from flask_socketio import SocketIO, emit

client = pymongo.MongoClient(os.environ["devmongo"])
dbm = client.Chat
import chat
import cmds
import filtering
import rooms

LOGFILE = "backend/chat.txt"

app = flask.Flask(__name__)
app.config['SECRET'] = os.urandom(9001)

logging.basicConfig(filename="backend/webserver.log",
                    filemode='a',
                    level=logging.INFO)
root = logging.getLogger()
root.addHandler(default_handler)
socketio = SocketIO(app)

# clear db, so that old users don't stay
dbm.Online.delete_many({})

banned_usernames = ('Admin', 'admin', '[admin]', '[ADMIN]', 'ADMIN', '[Admin]',
                    '[URL]', 'mod', 'Mod', '[mod]', '[Mod]', '[MOD]', 'MOD',
                    'SYSTEM', '[SYSTEM]', "SONG", "[Song]", "[SONG]", "[song]",
                    " ", "  ", "   ", "cseven", "cserver", 'system',
                    '[system]', '[System]', 'System')


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


@app.route('/changelog')
def changelog_page() -> ResponseReturnValue:
    """Serve the changelog, so old links don't break (after making the main page be the changelog)."""
    html_file = flask.render_template('update-log.html')
    return html_file


@app.route('/signup', methods=["POST", "GET"])
def signup() -> ResponseReturnValue:
    """Serve the signup page."""
    # I wonder if moving this to filtering.py would work
    # to be done later TM
    if request.method == "POST":
        SUsername = request.form.get("SUsername")
        SPassword = request.form.get("SPassword")
        SPassword2 = request.form.get("SPassword2")
        SRole = request.form.get("SRole")
        SDisplayname = request.form.get("SDisplayname")
        check = r'^[A-Za-z]{3,12}$'
        user_allowed = re.match(
            check, SUsername
        )  # and not re.search(r'dev|mod', SUsername, re.IGNORECASE) #The and needs to be moved to a seperate one to check for letter limit
        desplayname_allowed = re.match(
            check, SDisplayname
        )  # and not re.search(r'dev|mod', SDisplayname, re.IGNORECASE)
        if user_allowed == 'false' or desplayname_allowed == 'false':
            return flask.render_template(
                "signup-index.html",
                error='That Username/Display name is not allowed!',
                SRole=SRole,
            )
        if SPassword != SPassword2:
            return flask.render_template("signup-index.html",
                                         error='Password boxes do not match!',
                                         SUsername=SUsername,
                                         SRole=SRole,
                                         SDisplayname=SDisplayname)
        possible_user = dbm.Accounts.find_one({"username": SUsername})
        possible_dispuser = dbm.Accounts.find_one(
            {"displayName": SDisplayname})
        if possible_user is not None or possible_dispuser is not None or SUsername in banned_usernames or SDisplayname in banned_usernames:
            return flask.render_template(
                "signup-index.html",
                error='That Username/Display name is already taken!',
                SRole=SRole)
        dbm.Accounts.insert_one({
            "username":
            SUsername,
            "password":
            hashlib.sha384(bytes(SPassword, 'utf-8')).hexdigest(),
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
            "true",
            "SPermission":
            ""
        })
        return flask.redirect(flask.url_for('login_page'))
    else:
        return flask.render_template('signup-index.html')


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
                return flask.render_template(
                    'login.html', error="That account does not exist!")
            if TOSagree != "on":
                return flask.render_template(
                    'login.html', error='You did not agree to the TOS!')
            if username == user["username"] and hashlib.sha384(
                    bytes(password, 'utf-8')).hexdigest() == user["password"]:
                return flask.render_template(
                    'settings.html',
                    user=username,
                    passwd=
                    'we are not adding password editing just yet',  #hashlib.sha384(bytes(password, 'utf-8')).hexdigest(),
                    displayName=user["displayName"],
                    role=user["role"],
                    user_color=user["userColor"],
                    role_color=user["roleColor"],
                    message_color=user["messageColor"],
                    profile=user["profile"],
                    theme=user["theme"]
                )  # this could be a security issue later on (if they figure out this) we can move editing passwords to the same system as reseting passwords
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
                "theme": theme
            }
            if theme is None: return flask.render_template("settings.html", error='That Display name is already taken!', **return_list)
            if (dbm.Accounts.find_one({"displayName": displayname}) is not None and user["displayName"] != displayname) or displayname in banned_usernames:
                return flask.render_template(
                    "settings.html",
                    error='That Display name is already taken!',
                    **return_list)

            # if passwd != user["password"]: #need to make a check if they are not changing or we can just remove password changing from this methid to somthing else
            #     return flask.render_template("settings.html",
            #          error='Your password must not match your current one.',
            # **return_list)

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
                        "theme": theme
                        # "username": userid,
                        # "password": hashlib.sha384(bytes(passwd, 'utf-8')).hexdigest()
                    }
                })
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

    # Assuming you are using a MongoDB database called 'db' and a collection called 'Online'
    dbm.Online.insert_one({"username": username, "socketid": socketid, "location": location})

    for key in dbm.Online.find():
        user_info = key["username"]
        if key.get("location") == "settings":
            user_info = f"⚙️{user_info}"  # Add the settings icon in front of the user
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
    # lets see if this works
    for key in dbm.Online.find():
        username_list.append(key["username"])
    emit("online", username_list, broadcast=True)


@socketio.on("ban_cmd")
def ban_user(username: str, user):
    """Ban a user from the chat forever."""
    cmds.ban_user(username, user, '')


@socketio.on("mute_cmd")
def mute_user(username: str, user):
    """mute a user from the chat."""
    cmds.mute_user(username, user, '', '')


@socketio.on("unmute_cmd")
def unmute_user(username: str, user):
    """unmute a user from the chat."""
    cmds.unmute_user(username, user)


@socketio.on("admin_cmd")
def handle_admin_stuff(cmd: str, user, roomid):
    """Admin commands will be sent here."""
    cmds.find_command(commands={"v0": cmd}, user=user, roomid=roomid)


@socketio.on("get_rooms")
def get_rooms(username):
    """Grabs the chat rooms."""
    user_name = dbm.Accounts.find_one({"username": username})
    user = user_name["displayName"]
    room_access = rooms.get_chat_rooms()
    if user_name["SPermission"] == "Debugpass":
        emit('roomsList', room_access, namespace='/', to=request.sid)
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
                    ] and r['whitelisted'] == 'everyone')) and (
                        r['whitelisted'] != 'devonly')]
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
        else:
            filtering.failed_message("return", roomid)
    else:
        filtering.failed_message(result, roomid)


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


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8080)
