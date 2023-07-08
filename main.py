"""Main webserver file"""
import os
import logging
import json
import hashlib
import time
import keys
import flask
import pymongo
from flask import request
from flask.logging import default_handler
from flask.typing import ResponseReturnValue
from flask_socketio import SocketIO, emit
# because python is weird
client = pymongo.MongoClient(os.environ["acmongo_key"])
dbm = client.Chat
import chat
import cmds
import filtering
import rooms

LOGFILE = "backend/chat.txt"

app = flask.Flask(__name__)
app.config['SECRET'] = os.urandom(9001)
#lets hope our hacker does not have a quantum computer
# lol
logging.basicConfig(filename="backend/webserver.log",
                    filemode='a',
                    level=logging.INFO)
root = logging.getLogger()
root.addHandler(default_handler)
socketio = SocketIO(app, cors_allowed_origins="*")

# clear db, so that old users don't stay
dbm.Online.delete_many({})

banned_usernames = ('Admin', 'admin', '[admin]', '[ADMIN]', 'ADMIN', '[Admin]',
                    '[URL]', 'mod', 'Mod', '[mod]', '[Mod]', '[MOD]', 'MOD',
                    'SYSTEM', '[SYSTEM]', "SONG", "[Song]", "[SONG]", "[song]",
                    " ", "  ", "   ", "cseven", "cserver", 'system',
                    '[system]', '[System]', 'System')


@app.route('/')
def index() -> ResponseReturnValue:
    """Serve the main html page, modified if permission is granted."""
    return flask.render_template('update-log.html')
    # html_file = flask.render_template("update-log.html")
    # return html_file


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


@app.route('/chat', methods=["POST", "GET"])
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
        except TypeError:
            return flask.render_template(
                'login.html',
                error="That account does not exist! Go to the signup page")
        if TOSagree != "on":
            return flask.render_template('login.html',
                                         error='You did not agree to the TOS!')
        if username == user["username"] and hashlib.sha384(
                bytes(password, 'utf-8')).hexdigest() == user["password"]:
            return flask.render_template(
                'chat.html', user=username
            )  # this could be a security issue later on (if they figure out this)
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


@app.route("/debugmenu")
def debuging_page() -> ResponseReturnValue:
    """Host the menu for devs"""
    return flask.render_template('DPM.html')


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
        SDesplayname = request.form.get("SDesplayname")
        if SPassword != SPassword2:
            return flask.render_template("signup-index.html",
                                         error='Password boxes do not match!',
                                         SUsername=SUsername,
                                         SRole=SRole,
                                         SDesplayname=SDesplayname)
        possible_user = dbm.Accounts.find_one({"username": SUsername})
        possible_dispuser = dbm.Accounts.find_one(
            {"displayName": SDesplayname})
        if possible_user is not None or possible_dispuser is not None or SUsername in banned_usernames or SDesplayname in banned_usernames:
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
            SDesplayname,
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


@app.route('/settings')
def customize_accounts() -> ResponseReturnValue:
    """customize the accounts"""
    html_file = flask.render_template('acc-edit-index.html')
    return html_file


@app.route("/view")
def viewer_page() -> ResponseReturnValue:
    """Serve the viewer page."""
    html_file = flask.render_template('viewer.html')
    return html_file


@app.route("/aboutus")
def aboutus_page() -> ResponseReturnValue:
    """The about page"""
    html_file = flask.render_template('about-us.html')
    return html_file


@app.get('/backup_logs')
def get_backup_chat():
    """Return the backup-chat.txt contents."""
    ret_val = chat.get_chat("Chat-backup")
    return ret_val


@app.get('/chat_logs')
def respond_with_chat():
    """Legacy function only used now for inital chat load."""
    messages = chat.get_chat("chat")
    ret_val = json.dumps(messages)
    return ret_val


@app.post('/force_send')
def force_chat() -> str:
    """Legacy function that will be removed later."""
    json_receive = request.get_json(force=True)
    chat.force_message(json_receive['message'])
    emit("message_chat",
         json_receive['message'],
         broadcast=True,
         namespace="/")
    return "done"


# socketio stuff
@socketio.on('username')
def handle_connect(username: str):
    """Will be used later for online users."""
    socketid = request.sid
    username_list = []
    dbm.Online.insert_one({"username": username, "socketid": socketid})
    for key in dbm.Online.find():
        username_list.append(key["username"])
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


# pylint: disable=C0103, R0913
@socketio.on('update')
def update_handle(Euser, Erole, Cmessage, Crole, Cuser, Auser, Apass,
                  loginuser, Cprofile):
    """make the signup work."""
    dbm.Accounts.update_one({"username": loginuser}, {
        "$set": {
            "messageColor": Cmessage,
            "roleColor": Crole,
            "userColor": Cuser,
            "displayName": Euser,
            "role": Erole,
            "profile": Cprofile,
            "username": Auser,
            "password": hashlib.sha384(bytes(Apass, 'utf-8')).hexdigest(),
        }
    })
    emit("update_acc", namespace="/")


# pylint: enable=C0103, R0913
@socketio.on('get_perms')
def return_perms():
    "get perms for menus"
    Dev = os.environ["dev_key"]
    Mod = os.environ["mod_key"]
    time.sleep(.000001)
    emit("return_perms", (Dev, Mod), namespace="/")


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
def handle_admin_stuff(cmd: str, user):
    """Admin commands will be sent here."""
    cmds.handle_admin_cmds(cmd, user)


@socketio.on("create_room")
def create_rooms(name, user, username):
    """Someone wants to make a chat room."""
    if len(name) > 10:
        result = ('fail', 2)
    else:
        result = rooms.create_chat_room(username, dbm, name, user)
    emit('chatCreateResult', result)
    # emit new list to users (really just steal the get_rooms code more or less, but broadcast it now)
    if result[1] == 0:
        all_rooms = rooms.get_chat_rooms(dbm)
        emit('roomsList', all_rooms, namespace='/', broadcast=True)
        # :skull_emoji: :skull_emoji: :skull_emoji: :skull_emoji: :skull_emoji: taken in 4k


@socketio.on("get_rooms")
def get_rooms(user):
    """Grabs the chat rooms."""
    # later user will be used for the private chatrooms (to see if they have access to them or not)
    result = rooms.get_chat_rooms(dbm)
    emit('roomsList', result, namespace='/', to=request.sid)


# pylint: disable=C0103
@socketio.on('message_chat')
def handle_message(user_name, message, roomid):
    """New New chat message handling pipeline."""
    result = filtering.run_filter(user_name, message, dbm, roomid)
    if result[0] == 'msg':
        chat.add_message(result[1], roomid, dbm)
        emit("message_chat", (result[1], roomid), broadcast=True)
    else:
        filtering.failed_message(result, roomid)


# pylint: enable=C0103


@socketio.on('pingtest')
def handle_ping_tests(start):
    """Respond with the start time, so ping times can be calculated"""
    emit('ping_test', {
        "start": start,
    }, namespace='/')


# temporary, will be in diffrent namespace soon that seems to never get done at this point I SAID NOTHING
@socketio.on('admin_message')
def handle_admin_message(message, user):
    """Bypass message filtering, used when chat is locked."""
    chat.force_message(message)
    emit("message_chat", message, broadcast=True, namespace="/")


@socketio.on("room_connect")
def connect(roomid):
    """Switch rooms for the user"""
    socketid = request.sid
    try:
        room = dbm.rooms.find_one({"roomid": roomid})
    except TypeError:
        emit('room_data', "failed", namespace='/', to=socketid)

    if roomid == "ilQvQwgOhm9kNAOrRqbr":
        messages = chat.get_chat("chat")
        msgs = json.dumps(messages)
        response = {
            "messages": msgs,
            "name": room['roomName'],
            "roomid": "ilQvQwgOhm9kNAOrRqbr",
            "generatedBy": room['generatedBy'],
            "generatedAt": room['generatedAt']
        }
    else:
        del room['_id']
        response = room

    emit("room_data", response, to=socketid, namespace='/')


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8080)