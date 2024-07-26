from flask import Blueprint

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
            app.socketio.on_namespace(module.socketio)
        if hasattr(module, 'bp'):
            app.register_blueprint(module.bp)
    
    app.register_blueprint(bp)
