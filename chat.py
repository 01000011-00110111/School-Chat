"""Handle chat messages.
    Copyright (C) 2023  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
from datetime import timedelta
from time import time
from typing import List

import psutil
from flask_socketio import emit
import cmds
import log
import database

LOGFILE_B = "backend/Chat-backup.txt"

def format_system_msg(msg):
    """Format a message [SYSTEM] would send."""
    return f'[SYSTEM]: <font color="#ff7f00">{msg}</font>'

# Returns a list of dictionaries. Each dictionary in the list
# is a message that has been sent in our chat server
def get_chat(file: str) -> List:
    """Return list of chat messages."""
    ret_val = []
    with open(f"backend/{file}.txt", "r", encoding="utf8") as f_in:
        for line in f_in:
            line = line.rstrip("\n\r")
            rec = {"message": line}
            ret_val.append(rec)
    return ret_val

# this seriously needs to be moved to cmds.py
# or just remove in general
def line_blanks(**kwargs) -> None:
    """Send 100 blank lines in chat for testing purposes."""
    user = kwargs['user']
    roomid = kwargs['roomid']
    if cmds.check_if_dev(user) == 1:
        message_text = system_response(("message", 3), roomid)
        add_message(message_text, roomid, 'true')
        emit("message_chat", (
            format_system_msg('nothing to see here <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>nothing to see here'),
            roomid))
    else:
        cmds.respond_command(("reason", 2, "not_dev"), roomid, None)


def add_message(message_text: str, roomid, permission) -> None:
    """Handler for messages so they get logged."""
    room = database.find_room({'roomid': roomid}, 'msg')
    private = room is None
    room = database.find_private(roomid) if private else room
    lines = len(room["messages"]) if roomid != "all" else 1
    if (((lines >= 500 and roomid != "ilQvQwgOhm9kNAOrRqbr")
        or (roomid == "ilQvQwgOhm9kNAOrRqbr" and lines >= 1000)
        or (lines >= 250 and private))
        and permission != 'true'):
        reset_chat(message_text, False, roomid)
    else:
        (database.send_message_single(message_text,
                         roomid) if roomid != 'all' else database.send_message_all(message_text, roomid), log.backup_log(message_text, roomid, private))
    return ('room', 1)


def add_private_message(message_text: str, pmid) -> None:
    """Handler for messages so they get logged."""
    # lines = len(room["messages"]) if roomid != "all" else 1
    # if (lines >= 250):
    #     reset_chat(message_text, False, roomid)
    # else:
    database.send_private_message(message_text,
                        pmid) #if roomid != 'all' else database.send_message_all(message_text, roomid), log.backup_log(message_text, roomid))
    return ('room', 1)


def reset_chat(_: str, admin: bool, roomid) -> str:
    """Admin function for reseting chat. Also used by the GC."""
    if database.check_private(roomid):
        set_priv_message_DB(roomid, admin),
        emit("reset_chat", ("priv", roomid), broadcast=True, namespace="/")
        return ('good', 0)
    else:
        set_message_DB(roomid, admin)
        
    
    if admin is False:
        emit("reset_chat", ("owner/mod", roomid),
             broadcast=True,
             namespace="/")
    elif admin is True:
        emit("reset_chat", ("admin", roomid), broadcast=True, namespace="/")

    else:
        emit("reset_chat", ("auto", roomid), broadcast=True, namespace="/")
    return ('good', 0)


def system_response(id):
    """Stores all messages for system"""
    system_response = {
        1:
        "Chat reset by an admin.",
        2:
        "Chat reset by automatic wipe system.",
        3:
        'nothing to see here \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n nothing to see here',
        4:
        "Chat reset by this chat rooms Owner or Mod.",
        5:
        "Chat reset by a priavte chat user."
    }

    system_answer = format_system_msg(system_response.get(id))
    return system_answer


def set_message_DB(roomid, is_admin: bool):
    """clears the database"""
    if is_admin is True:
        message_text = system_response(1)
    elif is_admin is False:
        message_text = system_response(4)
    else:
        message_text = system_response("message", 2)
    database.clear_chat_room(roomid, message_text)
    

def set_priv_message_DB(pmid, user):
    """clears the database"""
    message_text = system_response(5) if user else system_response(2)
    database.clear_priv_chat(pmid, message_text)