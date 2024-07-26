import os
import logging
from flask import Flask
from flask_socketio import SocketIO
from flask_apscheduler import APScheduler
from flask_login import LoginManager
import app.database as database

scheduler = APScheduler()
socketio = SocketIO()
login_manager = LoginManager()

def setup_func():
    """Sets up the server"""
    if not os.path.exists('static/profiles'):
        os.makedirs('static/profiles')
    for filename in [
        'backend/accounts.txt',
        'backend/Chat-backup.txt',
        'backend/command_log.txt',
        'backend/permission.txt',
        'backend/chat-rooms_log.txt',
        'backend/webserver.log',
        'backend/unbanned_words.txt',
        'backend/banned_words.txt'
    ]:
        if not os.path.exists(filename):
            with open(filename, 'w'):
                pass
    database.setup_chatrooms()

setup_func()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(9001)  # ITS OVER 9000!!!!!!

    # Logging setup
    logging.basicConfig(filename="backend/webserver.log", filemode='a', level=logging.ERROR)
    logging.getLogger().setLevel(logging.ERROR)

    # Initialize extensions
    socketio.init_app(app)
    scheduler.init_app(app)
    scheduler.api_enabled = True
    login_manager.init_app(app)
    login_manager.login_view = 'login_page'
    database.clear_online()

    # Register Blueprints (routes)
    from app import routes
    routes.register_routes(app)
    
    return app

# Import models and commands to attach to the app
# from app import accounting, filtering, log, uploading, word_lists, appConfig, chat, online, private, rooms, user
