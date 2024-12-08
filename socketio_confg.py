"""socketio_handler.py: Filtering for usernames, and general formatting.
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in app.py or the LICENSE file.
"""
import socketio
sio = socketio.AsyncServer(async_mode="sanic", cors_allowed_origins='*')