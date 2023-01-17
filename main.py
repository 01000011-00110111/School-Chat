"""Main webserver file"""
import os
import logging
import json
import flask
from flask import request
from flask.logging import default_handler
from flask_socketio import SocketIO, emit
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


# serves commands to client, only gets requested once at loading
@app.get('/commands')
def command_list():
    """Return the current commands, probably will be scraped later."""
    commands = chat.get_command_list()
    ret_val = json.dumps(commands)
    return ret_val


@app.get('/cmdDef')
def command_def():
    """Return the current command definitions, probably will be scraped later."""
    commands = chat.get_command_defs()
    ret_val = json.dumps(commands)
    return ret_val

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


@app.get('/lock')
def lock_chat():
    """Lock the chat on the server side."""
    chat.add_message(
        "[SYSTEM]: <font color='#ff7f00'>Chat Locked by Admin.</font>")
    emit("message_chat",
         "[SYSTEM]: <font color='#ff7f00'>Chat Locked by Admin.</font>",
         broadcast=True,
         namespace="/")
    with open("backend/chat.lock", "w"):
        pass

    return "done"


@app.get('/unlock')
def unlock_chat():
    """Unlock the chat on the server side."""
    if os.path.exists("backend/chat.lock"):
        os.remove("backend/chat.lock")
        chat.add_message(
            "[SYSTEM]: <font color='#ff7f00'>Chat Unlocked by Admin.</font>")
        emit("message_chat",
             "[SYSTEM]: <font color='#ff7f00'>Chat Unlocked by Admin.</font>",
             broadcast=True,
             namespace="/")
    else:
        pass

    return "done"


@app.get('/stats')
def get_stats():
    """Send the server statistics in the chat."""
    result = chat.get_stats()
    emit("message_chat", result, broadcast=True, namespace="/")
    return "done"


@app.get('/reset')
def reset_chat():
    """Wipe the chat on admin request."""
    chat.reset_chat(False, True)
    emit("reset_chat", broadcast=True, namespace="/")
    return "done"


# socketio stuff
@socketio.on('connect')
def handle_connect(message):
    """Will be used later for online users."""
    print(message)
    # not working at the moment, possibly different, will check docs later


@socketio.on("admin_cmd")
def handle_admin_stuff(cmd):
    """Admin commands will be sent here."""
    if cmd == "blanks":
        chat.line_blanks()


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
