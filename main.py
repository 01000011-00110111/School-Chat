import bottle
import json
import chat

################################################################
#       Functions needed to allow clients to access files      #
################################################################


@bottle.route('/')
def index():
  html_file = bottle.template(
    "index.html",
    root=".",
    user_name=('Anonymous' if bottle.request.headers['X-Replit-User-Name']
               == '' else bottle.request.headers['X-Replit-User-Name']))
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


@bottle.route('/backend/ajax.js')
def ajax_file():
  ajax_js_file = bottle.static_file("backend/ajax.js", root=".")
  return ajax_js_file


@bottle.route('/backend/commands.js')
def commands_file():
  commands_js_file = bottle.static_file("backend/commands.js", root=".")
  return commands_js_file


################################################################
#             Functions handling AJAX interactions             #
################################################################


@bottle.get('/chat')
def respond_with_chat():
  messages = chat.get_chat()
  ret_val = json.dumps(messages)
  return ret_val


@bottle.post('/send')
def do_chat():
  json_receive = bottle.request.body.read().decode()
  message_dic = json.loads(json_receive)
  chat.add_message(message_dic['message'])
  response = chat.get_chat()
  ret_val = json.dumps(response)
  return ret_val


################################################################
#      Start the webserver                                     #
################################################################

bottle.run(host="0.0.0.0", port=8080)
