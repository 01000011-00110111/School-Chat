"""helpers.py: functions that need to be imported in multiple places."""
import time

from flask_socketio import emit

import chat


def end_ping(start, ID):
    """The end of the ping comamnd."""
    end = time.time() * 1000.0
    difference = end - start
    msg = '[SYSTEM]: <font color="#ff7f00">Ping Time: ' + str(
        int(difference)) + 'ms RTT</font>'
    chat.add_message(msg, ID, 'true')
    emit("message_chat", (msg, ID), broadcast=True, namespace="/")