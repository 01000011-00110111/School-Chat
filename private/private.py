"""private.py: Backend functions for the private messaging system.
    Copyright (C) 2023-2025  cserver45, cseven, CastyiGlitchxz
    License info can be viewed in app.py or the LICENSE file.
"""
# import asyncio
from datetime import datetime
from system import format_system_msg
from socketio_confg import sio
# pylint: disable=W0406
from private import database
# import private.database as database

# pmids = database.get_pmids()

class Private:
    """The Private chat class."""
    chats = {}  # Dictionary to store existing chats

    def __init__(self, private, pmid):
        """Initialize the chat."""
        

    # async def send_message(self, message):
    #     """Send a message to the chat."""
    #     self.messages.append(message)
    #     # self.config["last_message"] = datetime.now()
    #     lines = len(self.messages)# if not private else 1

    #     if lines >= 350:# and permission != 'true'):
    #         self.reset_chat()
    #     else:
    #         self.messages.append(message)

    #     for _, sid in self.sids.items():
    #         await sio.emit("message", {"message": message}, to=sid)

    # async def reset_chat(self):
    #     """Reset the chat."""
    #     self.messages.clear()
    #     msg = format_system_msg('Message limit reached chat cleared.')
    #     self.messages.append(msg)
    #     for _, sid in self.sids.items():
    #         await sio.emit("reset_chat", msg, to=sid)
