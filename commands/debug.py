from time import time
from flask_socketio import emit
from typing import List
import chat
import psutil
import database
import sys
import platform

LOGFILE_B = "backend/Chat-backup.txt"

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
    chat.add_message( \
        partial_stats_text if version == 'partial' else full_stats_text, roomid, 'true')
    return partial_stats_text if version == 'partial' else full_stats_text


def status(**kwargs):
    """Send stats into the chat."""
    roomid = kwargs['roomid']
    emit("message_chat", (get_stats(roomid, 'full'), roomid), broadcast=True)
    

def pstats(**kwargs):
    """Send stats into the chat."""
    roomid = kwargs['roomid']
    emit("message_chat", (get_stats(roomid, 'partial'), roomid), broadcast=True)
    

def line_count(**kwargs):
    """Respond with the current line count for the room (TBD)"""
    roomid = kwargs['roomid']
    lines = get_line_count("main", roomid)
    msg = f"[SYSTEM]: <font color='#ff7f00'>Line count is {lines}</font>\n"
    chat.add_message(msg, roomid, 'true')
    emit("message_chat", (msg, roomid), broadcast=True, namespace="/")

def ping(**kwargs):
    """EEEEEEEEEEEEEEEE"""
    roomid = kwargs['roomid']
    start = time.time() * 1000.0
    emit("pingTime", (start, roomid), namespace="/")
