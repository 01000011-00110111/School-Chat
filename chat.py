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
from main import dbm

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


def get_line_count(file, roomid) -> List:
    """Return the line count in the logfile."""
    if file == "main":
        room = dbm.rooms.find_one({"roomid": roomid})
        lines = len(room["messages"])
        return lines
    elif file == "backup":
        with open(LOGFILE_B, "r", encoding="utf8") as f_in:
            lines_b = len(f_in.readlines())
            return lines_b


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


# this needs to move to cmds.py
def get_stats(roomid) -> str:
    """Return full stats list to chat."""
    lines = get_line_count('main', roomid)
    lines_b = get_line_count('backup', roomid)
    # other stats on the repl
    p_in = psutil.Process()
    with p_in.oneshot():
        uptime = timedelta(seconds=time() - p_in.create_time())
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        thread_count = p_in.num_threads()
        # mem_virt = p_in.virtual_memory()[3]/1000000000
        # mem = p_in.memory_full_info()

    begin_f = "[SYSTEM]: <font color='#ff7f00'>Server Stats:</font>"
    lines_f = f"Temp logfile: {lines} lines.\nBackup logfile: {lines_b} lines."
    uptime_f = f"Uptime: {days}d, {hours}h, {minutes}m, {seconds}s."
    system_s = f"Threads: {thread_count}"
    # <br>Memory in use (webserver): {mem_virt}
    longstats = f"{begin_f}<br>{lines_f}<br>{uptime_f}<br>{system_s}<br>"
    add_message(longstats, roomid, 'true')
    return longstats


def add_message(message_text: str, roomid, permission) -> None:
    """Handler for messages so they get logged."""
    room = dbm.rooms.find_one({"roomid": roomid})
    lines = len(room["messages"]) if roomid != "all" else 1
    if (((lines >= 500 and roomid != "ilQvQwgOhm9kNAOrRqbr") 
        or (roomid == "ilQvQwgOhm9kNAOrRqbr" and lines >= 1000)) 
        and permission != 'true'):
        reset_chat(message_text, False, roomid)
    else:
        (send_message_DB(message_text,
                         roomid), log.backup_log(message_text, roomid))
    return ('room', 1)


def reset_chat(_: str, admin: bool, roomid) -> str:
    """Admin function for reseting chat. Also used by the GC."""
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
        "Chat reset by this chat rooms Owner or Mod."
    }

    system_answer = format_system_msg(system_response.get(id))
    return system_answer


def send_message_DB(message_text: str, roomid) -> None:
    """addes messages to the chat room in the database"""
    if roomid == "all":
        dbm.rooms.update_many({}, {'$push': {'messages': message_text}})
    else:
        dbm.rooms.update_one({"roomid": roomid},
                             {'$push': {
                                 'messages': message_text
                             }})


def set_message_DB(roomid, is_admin: bool):
    """clears the database"""
    if is_admin is True:
        message_text = system_response(1)
    elif is_admin is False:
        message_text = system_response(4)
    else:
        message_text = system_response(2)
    dbm.rooms.update_one({"roomid": roomid},
                         {'$set': {
                             "messages": [message_text]
                         }})