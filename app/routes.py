from flask import Blueprint
from app import socketio

bp = Blueprint('main', __name__)

def register_routes(app):
    from app import (
        accounting,
        appConfig,
        chat,
        cmds,
        database,
        filtering,
        log,
        online,
        private,
        rooms,
        uploading,
        user,
        word_lists,
    )

    modules = [
        accounting, appConfig, chat, cmds, database, filtering, log, online,
        private, rooms, uploading, user, word_lists
    ]

    for module in modules:
        if hasattr(module, 'socketio'):
            socketio.on_namespace(module.socketio)
        if hasattr(module, 'bp'):
            app.register_blueprint(module.bp)
    
    app.register_blueprint(bp)
    

@socketio.on("message_chat")
def handle_message(_, message, vid, userid, private, hidden):
    from app import chat, private as private_chat
    if private == "false":
        chat.handle_chat_message(message, vid, userid, hidden)
    else:
        private_chat.handle_private_message(message, vid, userid)
