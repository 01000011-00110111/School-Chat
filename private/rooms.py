"""chat/rooms.py: Backend functions for message handling.
    Copyright (C) 2023-2025  cserver45, cseven, CastyiGlitchxz
    License info can be viewed in app.py or the LICENSE file.
"""
# from datetime import datetime
from private.private import Private
from chat.chat import Chat
# import chat.database as chatdb
from user.user import User
from user.login import check_suuid
from socketio_confg import sio
