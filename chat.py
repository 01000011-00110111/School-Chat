"""Handle chat messages.
    Copyright (C) 2023  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
from datetime import timedelta
from time import time
from typing import List
import psutil
import sys
import platform
from flask_socketio import emit
import cmds
import log
import database

LOGFILE_B = "backend/Chat-backup.txt"


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
        room = database.find_room({'roomid': roomid}, 'msg')
        lines = len(room["messages"])
        return lines
    elif file == "backup":
        with open(LOGFILE_B, "r", encoding="utf8") as f_in:
            lines_b = len(f_in.readlines())
            return lines_b


# this seriously needs to be moved to cmds.py
def line_blanks(**kwargs) -> None:
    """Send 100 blank lines in chat for testing purposes."""
    user = kwargs['user']
    roomid = kwargs['roomid']
    if cmds.check_if_dev(user) == 1:
        message_text = system_response(("message", 3), roomid)
        add_message(message_text, roomid, 'true')
        emit("message_chat", (
            '[SYSTEM]: <font color="#ff7f00">nothing to see here <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>nothing to see here<br></font>',
            roomid))
    else:
        cmds.respond_command(("reason", 2, "not_dev"), roomid, None)


def get_stats(roomid, version) -> str:
    """Return extended stats list to chat."""
    lines_main = get_line_count('main', roomid)
    lines_backup = get_line_count('backup', roomid)

    # System stats
    p_in = psutil.Process()
    with p_in.oneshot():
        uptime_seconds = time() - p_in.create_time()
        days, seconds = divmod(int(uptime_seconds), 86400)
        hours, minutes = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        # thread_count = p_in.num_threads()
        mem_info = p_in.memory_full_info()
        mem_virt = mem_info.vms / (1024 ** 3)
        mem_res = mem_info.rss / (1024 ** 3)
        
    
    # CPU stats
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_cores = psutil.cpu_count(logical=False)  # physical cores
    cpu_threads = psutil.cpu_count(logical=True) # logical cores (including hyperthreading)

    # Python version
    python_version = sys.version

    # disk usage
    disk_usage = psutil.disk_usage('/')
    
    # nework usage
    net_io = psutil.net_io_counters()


    # Formatting stats for display
    full_stats_text = (
        "[SYSTEM]: <font color='#ff7f00'>Server Stats:</font><br>"
        f"Temp logfile: {lines_main} lines.<br>"
        f"Backup logfile: {lines_backup} lines.<br>"
        f"Uptime: {days} day(s), {hours} hour(s), {minutes} minute(s),\
            {seconds} seconds.<br>"
        f"CPU Usage: {cpu_percent}%<br>"
        f"CPU Cores: {cpu_cores} (Physical), {cpu_threads} (Logical)<br>"
        # f"Threads: {thread_count}<br>"
        f"Disk Usage: Total: {disk_usage.total / (1024 ** 3):.2f} GB, Used:\
            {disk_usage.used / (1024 ** 3):.2f} GB<br>"
        f"Virtual Memory: {mem_virt:.2f} GB<br>"
        f"Resident Memory: {mem_res:.2f} GB<br>"
        f"Network Usage: Sent: {net_io.bytes_sent / (1024 ** 2):.2f} MB, Received:\
            {net_io.bytes_recv / (1024 ** 2):.2f} MB<br>"
        f"Operating System: {platform.system()} {platform.version()}, Platform: \
            {platform.platform()}<br>"
        f"Python Version: {python_version}"
    )
    
    partial_stats_text = (
        "[SYSTEM]: <font color='#ff7f00'>Partial Server Stats:</font><br>"
        f"Temp logfile: {lines_main} lines.<br>"
        f"Backup logfile: {lines_backup} lines.<br>"
        f"Uptime: {days} day(s), {hours} hour(s), {minutes} minute(s),\
            {seconds} seconds.<br>"
        f"CPU Usage: {cpu_percent}%<br>"
        f"CPU Cores: {cpu_cores} (Physical), {cpu_threads} (Logical)<br>"
        f"Virtual Memory: {mem_virt:.2f} GB<br>"
        f"Resident Memory: {mem_res:.2f} GB<br>"
    )

    # Displaying formatted stats
    add_message( \
        partial_stats_text if version == 'partial' else full_stats_text, roomid, 'true')
    return partial_stats_text if version == 'partial' else full_stats_text





def add_message(message_text: str, roomid, permission) -> None:
    """Handler for messages so they get logged."""
    room = database.find_room({'roomid': roomid}, 'msg')
    lines = len(room["messages"]) if roomid != "all" else 1
    if lines >= 500 and permission != 'true' and roomid != "ilQvQwgOhm9kNAOrRqbr":
        reset_chat(message_text, False, roomid)
    elif roomid == "ilQvQwgOhm9kNAOrRqbr" and lines >= 1000 and permission != 'true':
        reset_chat(message_text, False, roomid)
    else:
        (database.send_message_single(message_text,
                         roomid) if roomid != 'all' else database.send_message_all(message_text, roomid), log.backup_log(message_text, roomid))
    return ('room', 1)


def reset_chat(message: str, admin: bool, roomid) -> str:
    """Admin function for reseting chat. Also used by the GC."""
    set_message_DB(roomid, admin)
    if admin == False:
        emit("reset_chat", ("owner/mod", roomid),
             broadcast=True,
             namespace="/")
    elif admin == True:
        emit("reset_chat", ("admin", roomid), broadcast=True, namespace="/")
    else:
        emit("reset_chat", ("auto", roomid), broadcast=True, namespace="/")
    return ('good', 0)


def system_response(message, id):
    """stores all messages for system"""
    system_response = {
        1:
        "[SYSTEM]: <font color='#ff7f00'>Chat reset by an admin.</font>",
        2:
        "[SYSTEM]: <font color='#ff7f00'>Chat reset by automatic wipe system.</font>",
        3:
        '[SYSTEM]: <font color="#ff7f00">nothing to see here \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n nothing to see here\n</font>',
        4:
        "[SYSTEM]: <font color='#ff7f00'>Chat reset by this chat rooms Owner or Mod.</font>"
    }

    system_answer = system_response.get(id)
    return system_answer


def set_message_DB(roomid, is_admin: bool):
    """clears the database"""
    if is_admin == True:
        message_text = system_response("message", 1)
    elif is_admin == False:
        message_text = system_response("message", 4)
    else:
        message_text = system_response("message", 2)
    database.clear_chat_room(roomid, message_text)