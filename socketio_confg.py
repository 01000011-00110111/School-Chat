"""socketio_handler.py: Filtering for usernames, and general formatting.
    Copyright (C) 2023-2025  cserver45, cseven, CastyiGlitchxz
    License info can be viewed in app.py or the LICENSE file.
"""
import socketio

sio = socketio.AsyncServer(async_mode="sanic", cors_allowed_origins='*')
