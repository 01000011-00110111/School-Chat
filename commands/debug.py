from datetime import datetime, timedelta
from flask_socketio import emit
import chat
import database
import log
import rooms


def status(**kwargs):
    """Send stats into the chat."""
    roomid = kwargs['roomid']
    emit("message_chat", (chat.get_stats(roomid, 'full'), roomid), broadcast=True)
    

def pstats(**kwargs):
    """Send stats into the chat."""
    roomid = kwargs['roomid']
    emit("message_chat", (chat.get_stats(roomid, 'partial'), roomid), broadcast=True)
    

def line_count(**kwargs):
    """Respond with the current line count for the room (TBD)"""
    roomid = kwargs['roomid']
    lines = chat.get_line_count("main", roomid)
    msg = f"[SYSTEM]: <font color='#ff7f00'>Line count is {lines}</font>\n"
    chat.add_message(msg, roomid, 'true')
    emit("message_chat", (msg, roomid), broadcast=True, namespace="/")