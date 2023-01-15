"""Main webserver file"""
import flask
from flask import request
from flask_socketio import SocketIO, emit
import json
import chat
import filtering
import os
import logging
from flask.logging import default_handler

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
  else:
    html_file = flask.render_template("index.html")
    return html_file


@app.route('/changelog')
def changelog():
  html_file = flask.render_template('update-log.html')
  return html_file


################################################################
#             Functions handling AJAX interactions             #
################################################################


@app.get('/chat')
def respond_with_chat():
  messages = chat.get_chat()
  ret_val = json.dumps(messages)
  return ret_val


# send total lines in chat
@app.get('/chat_count')
def chat_list():
  lines = chat.get_line_count()
  emit("message_chat",
       f"[SYSTEM]: <font color='#ff7f00'>Line count is {lines}</font>",
       broadcast=True,
       namespace="/")
  return "done"


# serves commands to client, only gets requested once at loading
@app.get('/commands')
def command_list():
  commands = chat.get_command_list()
  ret_val = json.dumps(commands)
  return ret_val


@app.get('/cmdDef')
def command_def():
  commands = chat.get_command_defs()
  ret_val = json.dumps(commands)
  return ret_val


"""@app.post('/send')
def do_chat():
  json_receive = request.get_json(force=True)
  if os.path.exists("backend/chat.lock"):
    pass
  else:
    result = filtering.filter_username(json_receive['message'])
    if result is not None:
      chat.add_message(result)
    # handle_message(result)
    response = chat.get_chat()
    ret_val = json.dumps(response)
    return ret_val"""
# now implmented in socketio


@app.post('/force_send')
def force_chat():
  # probably going to leave this as a html request, but still send to all (add send tag)
  json_receive = request.get_json(force=True)
  chat.force_message(json_receive['message'])
  emit("message_chat", json_receive['message'], broadcast=True, namespace="/")
  return "done"


@app.get('/lock')
def lock_chat():
  chat.add_message(
    "[SYSTEM]: <font color='#ff7f00'>Chat Locked by Admin.</font>")
  emit("message_chat",
       "[SYSTEM]: <font color='#ff7f00'>Chat Locked by Admin.</font>",
       broadcast=True,
       namespace="/")
  with open("backend/chat.lock", "w") as f:
    pass

  return "done"


@app.get('/unlock')
def unlock_chat():
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
  result = chat.get_stats()
  emit("message_chat", result, broadcast=True, namespace="/")
  return "done"


@app.get('/reset')
def reset_Chat():
  chat.reset_chat(False, True)
  emit("reset_chat", broadcast=True, namespace="/")
  return "done"


# socketio stuff
@socketio.on('connect')
def handle_connect(message):
  print(message)
  # not working at the moment, possibly different, will check docs later


@socketio.on("admin_cmd")
def handle_admin_stuff(cmd):
  if cmd == "blanks":
    chat.line_blanks()


@socketio.on('message_chat')
def handle_message(message):
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
  chat.force_message(message)
  emit("message_chat", message, broadcast=True, namespace="/")


#if message != "User connected to your text channel.":
#  send(message, broadcast=True)

################################################################
#      Start the webserver                                     #
################################################################

if __name__ == "__main__":
  socketio.run(app, host="0.0.0.0", port=8080)
