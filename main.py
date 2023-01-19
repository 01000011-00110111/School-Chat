"""Main webserver file"""
import os
import logging
import json
import flask
from time import sleep
from flask import request
from flask.logging import default_handler
from flask_socketio import SocketIO, emit
from replit import db
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

################################################################
#       Functions needed to allow clients to access files      #
################################################################


@app.route('/')
def index():
    """Serve the main html page, modified if permission is granted."""
    if request.args.get('dev') == os.environ['unknownkey']:
        html_file = flask.render_template("dev-index.html")
        return html_file
    elif request.args.get('editor') == "true":
        html_file = flask.render_template("editor-index.html")
        return html_file
    elif request.args.get('mod') == os.environ['Unknownvalue']:
        html_file = flask.render_template("mod-index.html")
        return html_file
    elif request.args.get('dev') == "true":
        html_file = flask.render_template("chaos-index.html")
        return html_file

    html_file = flask.render_template("index.html")
    return html_file


@app.route('/changelog')
def changelog():
    """Serve the changelog."""
    html_file = flask.render_template('update-log.html')
    return html_file


################################################################
#             Functions handling AJAX interactions             #
################################################################


@app.get('/chat')
def respond_with_chat():
    """Legacy function only used now for inital chat load."""
    messages = chat.get_chat()
    ret_val = json.dumps(messages)
    return ret_val


# send total lines in chat
@app.get('/chat_count')
def chat_list():
    """Print line count of the chat in the chat."""
    lines = chat.get_line_count()
    emit("message_chat",
         f"[SYSTEM]: <font color='#ff7f00'>Line count is {lines}</font>",
         broadcast=True,
         namespace="/")
    return "done"


@app.post('/force_send')
def force_chat():
    """Legacy function that will be removed later."""
    json_receive = request.get_json(force=True)
    chat.force_message(json_receive['message'])
    emit("message_chat",
         json_receive['message'],
         broadcast=True,
         namespace="/")
    return "done"


@app.get('/reset')
def reset_chat():
    """Wipe the chat on admin request."""
    chat.reset_chat(False, True)
    emit("reset_chat", broadcast=True, namespace="/")
    return "done"


# socketio stuff
@socketio.on('username')
def handle_connect(username, socketid):
    """Will be used later for online users."""
    db[socketid] = username
    username_list = []
    for onlineuser in db:
        username_list.append(onlineuser)
    emit("online", username_list, broadcast=True)
    # not working at the moment, possibly different, will check docs later


@socketio.on('username_msg')
def handle_online(username, p_username, socketid):
    """Add username to currently online people list."""
    if p_username != username:
        for socketid_db in db:
            if socketid_db[socketid] == p_username:
                socketid_db[socketid] = username
                username_list = []
                # rewrite in a second, because it makes no sense lol
                for onlineuser in db: username_list.append(onlineuser[socketid_db])
                emit("online", username_list, broadcast=True)


@socketio.on("admin_cmd")
def handle_admin_stuff(cmd):
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
    elif cmd == "ban":
        print("test")
        emit("ban", "true", broadcast=True)
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


@socketio.on('message_chat')
def handle_message(message):
    """New socketio implemntation for chat message handling."""
    print(message)
    if os.path.exists("backend/chat.lock"):
        pass
    else:
        result = filtering.filter_username(message)
        if result is not None:
            chat.add_message(result)
            emit("message_chat", result, broadcast=True)


# temporary, will be in diffrent namespace soon
@socketio.on('admin_message')
def handle_admin_message(message):
    """Bypass message filtering, used when chat is locked."""
    chat.force_message(message)
    emit("message_chat", message, broadcast=True, namespace="/")


#if message != "User connected to your text channel.":
#  send(message, broadcast=True)

################################################################
#      Start the webserver                                     #
################################################################

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8080)
