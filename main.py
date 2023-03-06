"""Main webserver file"""
import os
import logging
import json
from time import sleep
import hashlib
import flask
from flask import request
from flask.logging import default_handler
from flask.typing import ResponseReturnValue
from flask_socketio import SocketIO, emit
from replit import db
# import sqlite3
import chat
import filtering

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

# who is online, why no one use my chat program
db.clear()
# connection = sqlite3.connect("myDatabase.db")
# connection.execute("CREATE TABLE IF NOT EXISTS online (id STRING PRIMARY KEY, username STRING);")
# cursor = connection.cursor("SELECT * FROM online")
################################################################
#       Functions needed to allow clients to access files      #
################################################################


@app.route('/')
def index() -> ResponseReturnValue:
    """Serve the main html page, modified if permission is granted."""
    dev = request.args.get('dev')
    mod = request.args.get('mod')
    # this is probaby overengineered, but it works and works well
    if hashlib.sha224(bytes((dev if dev is not None else "none"),
                            'utf-8')).hexdigest() == os.environ['unknownkey']:
        html_file = flask.render_template("dev-index.html")
    elif request.args.get('editor') == "begonenotowens":
        html_file = flask.render_template("editor-index.html")
    elif hashlib.sha224(bytes(
        (mod if mod is not None else "none"),
            'utf-8')).hexdigest() == os.environ['Unknownvalue']:
        html_file = flask.render_template("mod-index.html")
    elif request.args.get('dev') == "true":
        html_file = flask.render_template("chaos-index.html")
    elif request.args.get('jotd') == "true":
        html_file = flask.render_template("JOTD-index.html")
    else:
        html_file = flask.render_template("index.html")

    return html_file


# easter egg time lol
@app.route("/f")
def f_but_better() -> ResponseReturnValue:
    """Not an easter egg I promise."""


@app.route('/changelog')
def changelog() -> ResponseReturnValue:
    """Serve the changelog."""
    html_file = flask.render_template('update-log.html')
    return html_file


@app.route('/signup')
def signup() -> ResponseReturnValue:
    """Serve the signup page."""
    html_file = flask.render_template('signup-index.html')
    return html_file


@app.route('/backup')
def get_logs_page() -> ResponseReturnValue:
    """Serve the chat logs (backup)"""
    html_file = flask.render_template('Backup-chat.html')
    return html_file


@app.route("/view")
def viewer_page() -> ResponseReturnValue:
    """Serve the viewer page."""
    html_file = flask.render_template('viewer.html')
    return html_file


################################################################
#             Functions handling AJAX interactions             #
################################################################


@app.get('/backup_logs')
def get_backup_chat():
    """Return the backup-chat.txt contents."""
    ret_val = chat.get_chat("Chat-backup")
    return ret_val


@app.get('/chat')
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
    db[socketid] = username
    username_list = []
    keys = db.keys()
    for key in keys:
        username_list.append(db[key])
    emit("online", username_list, broadcast=True)


@socketio.on('disconnect')
def handle_disconnect():
    """Remove the user from the online user db on disconnect."""
    socketid = request.sid
    try:
        del db[socketid]
        username_list = []
        keys = db.keys()
        for key in keys:
            username_list.append(db[key])
        emit("online", username_list, broadcast=True)
    except KeyError:
        pass


@socketio.on('username_msg')
def handle_online(username: str, p_username: str):
    """Add username to currently online people list."""
    if p_username != username:
        keys = db.keys()
        for key in keys:
            if db[key] == p_username:
                db[key] = username
                username_list = []
                # rewrite in a second, because it makes no sense lol
                for key in keys:
                    username_list.append(db[key])
                emit("online", username_list, broadcast=True)
                return


@socketio.on("ban_cmd")
def ban_user(username: str):
    """Ban a user from the chat forever (until cookie wipe.)"""
    emit("ban", username, broadcast=True)
    chat.force_message('[SYSTEM]: <font color="#ff7f00">' + username +
                       " is mutted for an undefned period of time.</font>")
    emit("message_chat",
         '[SYSTEM]: <font color="#ff7f00">' + username +
         " is Banned for forever.</font>",
         broadcast=True)


@socketio.on("mute_cmd")
def mute_user(username: str):
    """mute a user from the chat untilled mutted or until cookie wipe."""
    emit("mute", username, broadcast=True)
    chat.force_message('[SYSTEM]: <font color="#ff7f00">' + username +
                       " is mutted for an undefned period of time.</font>")
    emit("message_chat",
         '[SYSTEM]: <font color="#ff7f00">' + username +
         " is mutted for an undefned period of time.</font>",
         broadcast=True)


@socketio.on("unmute_cmd")
def unmute_user(username: str):
    """unmute a user from the chat"""
    emit("unmute", username, broadcast=True)
    chat.force_message('[SYSTEM]: <font color="#ff7f00">' + username +
                       " is unmuted.</font>")
    emit("message_chat",
         '[SYSTEM]: <font color="#ff7f00">' + username +
         " is unmutted.</font>",
         broadcast=True)


@socketio.on("admin_cmd")
def handle_admin_stuff(cmd: str):
    """Admin commands will be sent here."""
    if cmd == "blanks":
        chat.line_blanks()
    elif cmd == "cookieEater":
        sleep(5)
        emit("message_chat", "[Admin]: 5 seconds")
        sleep(4)  # because of other latency and for jokes.
        emit("cookieEater", "true", broadcast=True)
        emit("message_chat",
             "[Admin]: Cookies have been wiped from all clients online.")
    elif cmd == "full_status":
        result = chat.get_stats()
        emit("message_chat", result, broadcast=True)
    elif cmd == "lock":
        chat.add_message(
            "[SYSTEM]: <font color='#ff7f00'>Chat Locked by Admin.</font>")
        emit("message_chat",
             "[SYSTEM]: <font color='#ff7f00'>Chat Locked by Admin.</font>",
             broadcast=True)
        with open("backend/chat.lock", "w", encoding="utf8"):
            pass
    elif cmd == "unlock":
        if os.path.exists("backend/chat.lock"):
            os.remove("backend/chat.lock")
            chat.add_message(
                "[SYSTEM]: <font color='#ff7f00'>Chat Unlocked by Admin.</font>"
            )
            emit(
                "message_chat",
                "[SYSTEM]: <font color='#ff7f00'>Chat Unlocked by Admin.</font>",
                broadcast=True)
    elif cmd == "username_clear":
        db.clear()
    elif cmd == "refresh_users":
        db.clear()
        emit("force_username", "", broadcast=True)
    elif cmd == "reset_chat":
        chat.reset_chat(False, True)
        emit("reset_chat", broadcast=True, namespace="/")


@socketio.on('message_chat')
def handle_message(message):
    """New socketio implemntation for chat message handling."""
    result = filtering.filter_username(message)
    if result is not True and result is not None:
        chat.add_message(result)
        emit("message_chat", result, broadcast=True)


# temporary, will be in diffrent namespace soon
@socketio.on('admin_message')
def handle_admin_message(message):
    """Bypass message filtering, used when chat is locked."""
    chat.force_message(message)
    emit("message_chat", message, broadcast=True, namespace="/")


################################################################
#      Start the webserver                                     #
################################################################

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8080)
