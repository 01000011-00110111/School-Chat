"""Main webserver file"""
import os
import logging
import json
import hashlib
import time
import re
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

LOGFILE = "backend/chat.txt"

app = flask.Flask(__name__)
app.config['SECRET'] = os.urandom(
    9001)  #lets hope our hacker does not have a quantum computer
# lol
logging.basicConfig(filename="backend/webserver.log",
                    filemode='a',
                    level=logging.INFO)
root = logging.getLogger()
root.addHandler(default_handler)
# make this load from replit secrets later
socketio = SocketIO(app, cors_allowed_origins="*")

# clear db, so that old users don't stay
#dbm.Online.delete_many({})

################################################################
#       Functions needed to allow clients to access files      #
################################################################


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


@app.route('/chat')
def chat_page() -> ResponseReturnValue:
    """Serve the main chat, stops bypass bans."""
    html_file = flask.render_template('index.html')
    return html_file


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
        return flask.redirect(flask.url_for('chat_page'))
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


################################################################
#             Functions handling AJAX interactions             #
################################################################


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


# send total lines in chat
@app.get('/chat_count')
def chat_list() -> str:
    """Print line count of the chat in the chat."""
    lines = chat.get_line_count()
    emit("message_chat",
         f"[SYSTEM]: <font color='#ff7f00'>Line count is {lines}</font>",
         broadcast=True,
         namespace="/")
    return "done"


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


@socketio.on('signup')
def signup_handle(SUsername, SDesplayname, SPassword, SRole, Sprofile):
    """make the signup work."""
    emit("signup_pass", namespace="/")


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
    Edit = os.environ["edit_key"]
    JOTD = os.environ["JOTD_key"]
    time.sleep(.000001)
    emit("return_perms", (Dev, Mod, Edit, JOTD), namespace="/")


@socketio.on('get_prefs')
def return_user_prefs(username):
    """Return roles, colors, and theme to logged in user."""
    user = dbm.Accounts.find_one({"username": username})

    try:
        emit("return_prefs", {
            "displayName": user["displayName"],
            "role": user["role"],
            "profile": user["profile"],
            "userColor": user["userColor"],
            "theme": user["theme"],
            "messageColor": user["messageColor"],
            "roleColor": user["roleColor"],
            "permission": user["permission"],
            "SPermission": user["SPermission"]
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
    cmds.ban_user(username, user)


@socketio.on("mute_cmd")
def mute_user(username: str, user):
    """mute a user from the chat."""
    cmds.mute_user(username, user)


@socketio.on("unmute_cmd")
def unmute_user(username: str, user):
    """unmute a user from the chat."""
    cmds.unmute_user(username, user)


@socketio.on("admin_cmd")
def handle_admin_stuff(cmd: str, user):
    """Admin commands will be sent here."""
    cmds.handle_admin_cmds(cmd, user)


# pylint: disable=C0103
@socketio.on('message_chat')
def handle_message(user_name, message):
    """New New chat message handling pipeline."""
    result = filtering.run_filter(user_name, message, dbm)
    if result[0] == 'msg':
        chat.add_message(result[1])
        emit("message_chat", result[1], broadcast=True)
    else:
        filtering.failed_message(result)


# pylint: enable=C0103


@socketio.on('pingtest')
def handle_ping_tests(start):
    emit('ping_test', {
        "start": start,
    }, namespace='/')


@socketio.on('wisper_chat')
def handle_wisper(message, recipient, sender):
    """Wisper a message to another user."""
    user = dbm.Online.find_one({"username": recipient})
    message_comp = "<i><b>" + sender + "</b>  wispers to you: </i>" + message
    pings = re.findall(r'(?<=\[).+?(?=\])', message)

    for ping in pings:
        emit(
            "ping",
            {
                "who": ping,
                "from": sender,
                # "pfp": profile_img
            },
            namespace="/",
            broadcast=True)

    try:
        emit("message_chat", message_comp, namespace="/", to=user["socketid"])
    except TypeError:
        return


# temporary, will be in diffrent namespace soon that seems to never get done at this point I SAID NOTHING
@socketio.on('admin_message')
def handle_admin_message(message, user):
    """Bypass message filtering, used when chat is locked."""
    chat.force_message(message)
    emit("message_chat", message, broadcast=True, namespace="/")


################################################################
#      Start the webserver                                     #
################################################################

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8080)
