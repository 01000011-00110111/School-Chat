"""All debug/devolpent commands for checking status or for testing the server
    Copyright (C) 2023  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
import platform
import sys
from time import time
from typing import List

# from cmds import other.respond_command, check_if_dev
import psutil
from flask_socketio import emit

import database
import log
from commands import other
from user import User

LOGFILE_B = "backend/Chat-backup.txt"


def get_line_count(file, vid) -> List:
    """Return the line count in the logfile."""
    lines = 0
    if file == "main":
        room = database.find_room({'roomid': vid}, 'msg')
        room = database.find_private(vid) if room is None else room
        lines = len(room["messages"])
    if file == "backup":
        with open(LOGFILE_B, "r", encoding="utf8") as f_in:
            lines = len(f_in.readlines())
    return lines


def get_stats(roomid, version, room) -> str:
    """Return extended stats list to chat."""
    # System stats
    p_in = psutil.Process()
    with p_in.oneshot():
        uptime_seconds = time() - p_in.create_time()
        days, seconds = divmod(int(uptime_seconds), 86400)
        hours, minutes = divmod(seconds, 3600)
        minutes, seconds = divmod(minutes, 60)

        mem_info = p_in.memory_full_info()
        mem_virt = mem_info.vms / (1024 ** 3)
        mem_res = mem_info.rss / (1024 ** 3)

    # Define full and partial helper functions
    def full():
        return (
            "[SYSTEM]: <font color='#ff7f00'>Server Stats:</font><br>"
            f"Temp logfile: {get_line_count('main', roomid)} lines.<br>"
            f"Backup logfile: {get_line_count('backup', None)} lines.<br>"
            f"Uptime: {days} day(s), {hours} hour(s), {minutes} minute(s), {seconds} seconds.<br>"
            f"CPU Usage: {psutil.cpu_percent(interval=1)}%<br>"
            f"CPU Cores: {psutil.cpu_count(logical=False)} (Physical), \
                {psutil.cpu_count(logical=True)} (Logical)<br>"
            f"Disk Usage: Total: {psutil.disk_usage('/').total / (1024 ** 3):.2f}\
                GB, Used: {psutil.disk_usage('/').used / (1024 ** 3):.2f} GB<br>"
            f"Virtual Memory: {mem_virt:.2f} GB<br>"
            f"Resident Memory: {mem_res:.2f} GB<br>"
            f"Network Usage: Sent: {psutil.net_io_counters().bytes_sent / (1024 ** 2):.2f} MB, \
                Received: {psutil.net_io_counters().bytes_recv / (1024 ** 2):.2f} MB<br>"
            f"Operating System: {platform.system()} {platform.version()},\
                Platform: {platform.platform()}<br>"
            f"Python Version: {sys.version}"
        )

    def partial():
        return (
            "[SYSTEM]: <font color='#ff7f00'>Partial Server Stats:</font><br>"
            f"Temp logfile: {get_line_count('main', roomid)} lines.<br>"
            f"Backup logfile: {get_line_count('backup', None)} lines.<br>"
            f"Uptime: {days} day(s), {hours} hour(s), {minutes} minute(s), {seconds} seconds.<br>"
            f"CPU Usage: {psutil.cpu_percent(interval=1)}%<br>"
            f"CPU Cores: {psutil.cpu_count(logical=False)} (Physical), \
                {psutil.cpu_count(logical=True)} (Logical)<br>"
            f"Virtual Memory: {mem_virt:.2f} GB<br>"
            f"Resident Memory: {mem_res:.2f} GB<br>"
        )

    # Displaying formatted stats
    stats_text = partial() if version == 'partial' else full()
    room.add_message(stats_text, 'true')

    return stats_text



def status(**kwargs):
    """Send stats into the chat."""
    roomid = kwargs['roomid']
    room = kwargs['room']
    emit("message_chat", (get_stats(roomid, 'full', room), roomid), broadcast=True)


def pstats(**kwargs):
    """Send stats into the chat."""
    roomid = kwargs['roomid']
    room = kwargs['room']
    emit("message_chat", (get_stats(roomid, 'partial', room), roomid), broadcast=True)


def line_count(**kwargs):
    """Respond with the current line count for the room (TBD)"""
    roomid = kwargs['roomid']
    room = kwargs['room']
    lines = get_line_count("main", roomid)
    msg = other.format_system_msg(f"Line count is {lines}\n")
    room.add_message(msg, 'true')


def ping(**kwargs):
    """Send the RTT of a message, used for debugging."""
    roomid = kwargs['roomid']
    start = time() * 1000.0
    emit("pingTime", (start, roomid), namespace="/")


def send_cmd_logs(**kwargs):
    """Send the last 10 lines in command_log.txt"""
    # user = kwargs['user']
    roomid = kwargs['roomid']
    room = kwargs['room']
    msg = log.get_cmd_logs()
    if database.check_private(roomid):
        room.add_private_message(msg, None)
    else:
        room.add_message(msg, 'false')


def clear_all_mutes(**kwargs):
    """Clears all mutes from every user."""
    # user = kwargs['user']
    # roomid = kwargs['roomid']
    room = kwargs['room']
    for user in User.Users.values():
        user.mutes = []
    message = other.format_system_msg("All mutes cleared by a Dev.")
    room.add_message(message, None)
