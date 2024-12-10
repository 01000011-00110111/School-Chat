"""private.py: Backend functions for the private messaging system.
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
from datetime import datetime
import private.database as database


class Private:
    """The Private chat class."""
    chats = {}  # Dictionary to store existing chats
    chats_userlist = {} #or do i make it

    def __init__(self, private, vid, userlist):
        """Initialize the chat."""
        lst = private["userIds"]
        self.userlist = lst
        self.active = {lst[0]: False, lst[1]: False}
        self.vid = vid
        self.messages = database.get_private_messages(userlist)
        self.unread = private['unread']
        self.backup_values = [
            [0, 0], # 1st is total and 2nd is total sense last message
            datetime.now()
        ]
        self.sids = []
