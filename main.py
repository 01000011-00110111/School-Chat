"""Main webserver file"""
import flask
from flask import request
from flask_socketio import SocketIO, send
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
root = logging.getLogger()
root.addHandler(default_handler)
# make this load from replit secrets later
socketio = SocketIO(app, cors_allowed_origins="*")

################################################################
#       Functions needed to allow clients to access files      #
################################################################


@app.route('/')
def index():
  if request.args.get('dev') == "true":
    html_file = flask.render_template("dev-index.html")
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
  ret_val = json.dumps(lines)
  return ret_val


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


@app.post('/send')
def do_chat():
  json_receive = request.get_json(force=True)
  if os.path.exists("backend/chat.lock"):
    pass
  else:
    chat.add_message(json_receive['message'])
    response = chat.get_chat()
    ret_val = json.dumps(response)
    return ret_val


@app.post('/force_send')
def force_chat():
  json_receive = request.get_json(force=True)
  chat.force_message(json_receive['message'])
  response = chat.get_chat()
  ret_val = json.dumps(response)
  return ret_val


@app.get('/lock')
def lock_chat():
  chat.add_message(
    "[SYSTEM]: <font color='#ff7f00'>Chat Locked by Admin.</font>")
  with open("backend/chat.lock", "w") as f:
    pass


@app.get('/unlock')
def unlock_chat():
  if os.path.exists("backend/chat.lock"):
    os.remove("backend/chat.lock")
    chat.add_message(
      "[SYSTEM]: <font color='#ff7f00'>Chat Unlocked by Admin.</font>")
  else:
    pass


@app.get('/stats')
def get_stats():
  chat.get_stats()
  return


@app.get('/reset')
def reset_Chat():
  chat.reset_chat(False, True)
  return


# socketio stuff
@socketio.on('message')
def handle_message(message):
  if message != "User connected to your text channel.":
    send(message, broadcast=True)


################################################################
#      Start the webserver                                     #
################################################################

if __name__ == "__main__":
  socketio.run(app, host="0.0.0.0", port=8080)
