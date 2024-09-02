from flask import Flask
from flask_socketio import SocketIO
# from flask_login import LoginManager


socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize SocketIO with the Flask app
    socketio.init_app(app)

    with app.app_context():
        # Import routes and socket events
        from app import login, chat, user, connections, log
        user.login_manager.init_app(app)

        # Register routes
        app.register_blueprint(login.login_bp)
        app.register_blueprint(chat.chat_bp)
        app.register_blueprint(log.log_bp)

    return app
