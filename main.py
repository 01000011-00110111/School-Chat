import bottle
import json
import chat
import os

################################################################
#       Functions needed to allow clients to access files      #
################################################################


@bottle.route('/')
def index():
  if bottle.request.params.get('dev') == "true":
    html_file = bottle.template("dev-index.html", root=".")
    return html_file
  else:
    html_file = bottle.template("index.html", root=".")
    return html_file

@bottle.route('/static/style.css')
def css_style():
  css_file = bottle.static_file("static/style.css", root=".")
  return css_file


@bottle.route('/static/CSS/Event-CSS/<filepath:path>')
def server_static(filepath):
  return bottle.static_file(filepath, root='./static/')


@bottle.route('/static/favicon.ico')
def favicon():
  favicon = bottle.static_file("images/favicon.ico", root=".")
  return favicon


@bottle.route('/backend/chat.js')
def chat_file():
  chat_js_file = bottle.static_file("backend/chat.js", root=".")
  return chat_js_file

@bottle.route('/backend/styles.js')
def styles_js_file():
  styles_js_file = bottle.static_file("backend/styles.js", root=".")
  return styles_js_file

@bottle.route('/backend/ajax.js')
def ajax_file():
  ajax_js_file = bottle.static_file("backend/ajax.js", root=".")
  return ajax_js_file


@bottle.route('/backend/commands.js')
def commands_file():
  commands_js_file = bottle.static_file("backend/commands.js", root=".")
  return commands_js_file

@bottle.route('/backend/dev-menu.js')
def dev_menu_file():
  dev_menu_js_file = bottle.static_file("backend/dev-menu.js", root=".")
  return dev_menu_js_file


################################################################
#             Functions handling AJAX interactions             #
################################################################


@bottle.get('/chat')
def respond_with_chat():
  messages = chat.get_chat()
  ret_val = json.dumps(messages)
  return ret_val

# send total lines in chat
@bottle.get('/chat_count')
def chat_list():
  lines = chat.get_line_count()
  ret_val = json.dumps(lines)
  return ret_val

# serves commands to client, only gets requested once at loading
@bottle.get('/commands')
def command_list():
  commands = chat.get_command_list()
  ret_val = json.dumps(commands)
  return ret_val

@bottle.get('/cmdDef')
def command_def():
  commands = chat.get_command_defs()
  ret_val = json.dumps(commands)
  return ret_val

@bottle.post('/send')
def do_chat():
  json_receive = bottle.request.body.read().decode()
  message_dic = json.loads(json_receive)
  if os.path.exists("backend/chat.lock"):
    pass
  else:
    chat.add_message(message_dic['message'])
  response = chat.get_chat()
  ret_val = json.dumps(response)
  return ret_val

@bottle.post('/force_send')
def force_chat():
  json_receive = bottle.request.body.read().decode()
  message_dic = json.loads(json_receive)
  chat.force_message(message_dic['message'])
  response = chat.get_chat()
  ret_val = json.dumps(response)
  return ret_val

@bottle.get('/lock')
def lock_chat():
  chat.add_message("[SYSTEM]: <font color='#ff7f00'>Chat Locked by Admin.</font>")
  with open("backend/chat.lock", "w") as f:
    pass

@bottle.get('/unlock')
def unlock_chat():
  if os.path.exists("backend/chat.lock"):
    os.remove("backend/chat.lock")
    chat.add_message("[SYSTEM]: <font color='#ff7f00'>Chat Unlocked by Admin.</font>")
  else:
    pass

@bottle.get('/stats')
def get_stats():
  chat.get_stats()
  return

################################################################
#      Start the webserver                                     #
################################################################

bottle.run(host="0.0.0.0", port=8080)
