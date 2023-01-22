"""Handle chat messages."""
from time import time
from datetime import timedelta, datetime
import psutil
from flask_socketio import emit

LOGFILE = "backend/chat.txt"
LOGFILE_B = "backend/Chat-backup.txt"


# Returns a list of dictionaries. Each dictionary in the list
# is a message that has been sent in our chat server
def get_chat():
    """Return list of chat messages."""
    ret_val = []
    with open(LOGFILE, "r", encoding="utf8") as f_in:
        for line in f_in:
            line = line.rstrip("\n\r")
            rec = {"message": line}
            ret_val.append(rec)
    return ret_val


def get_line_count():
    """Return the line count in the logfiles."""
    ret_val = []
    with open(LOGFILE, "r", encoding="utf8") as f_in:
        lines = len(f_in.readlines())
    with open(LOGFILE, "a", encoding="utf8") as f_in:
        f_in.write(
            f"[SYSTEM]: <font color='#ff7f00'>Line count is {lines}</font>\n")
        ret_val = lines
    return ret_val


def line_blanks():
    """Send 100 blank lines in chat for testing purposes."""
    add_message(
        '[SYSTEM]: <font color="#ff7f00">nothing to see here \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n nothing to see here\n</font>'
    )
    emit(
        "message_chat",
        '[SYSTEM]: <font color="#ff7f00">nothing to see here <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>nothing to see here<br></font>'
    )


def get_stats():
    """Return full stats list to chat."""

    # get line count
    with open(LOGFILE, "r", encoding="utf8") as f_in:
        lines = len(f_in.readlines())
    with open(LOGFILE_B, "r", encoding="utf8") as f_in:
        lines_b = len(f_in.readlines())

    # other stats on the repl
    p_in = psutil.Process()
    with p_in.oneshot():
        uptime = timedelta(seconds=time() - p_in.create_time())
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        pname = p_in.name()
        thread_count = p_in.num_threads()
        mem = p_in.memory_full_info()

    begin_f = "[SYSTEM]: <font color='#ff7f00'>Server Stats:</font>"
    lines_f = f"Temp logfile: {lines} lines.\nBackup logfile: {lines_b} lines."
    uptime_f = f"Uptime: {days} day(s), {hours} hour(s), {minutes} minute(s), {seconds} seconds."
    cpu_info = f"Threads: {thread_count}"
    longstats = f"{begin_f}<br>{lines_f}<br>{uptime_f}<br>{cpu_info}<br>"
    with open(LOGFILE, "a", encoding="utf8") as f_in:
        f_in.write(longstats)
    return longstats


# Adds the message text to our file containing all the messages
def add_message(message_text):
    """Handler for messages so they get logged."""
    with open(LOGFILE, "r", encoding="utf8") as f_in:
        lines = len(f_in.readlines())
    if lines >= 500:
        reset_chat(message_text, False)
    else:
        with open(LOGFILE, "a", encoding="utf8") as f_in:
            f_in.write(message_text + "\n")
    with open(LOGFILE_B, "a", encoding="utf8") as f_out:
        date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S: ")
        f_out.write(date + message_text + "\n")


def reset_chat(message, admin):
    """Admin function for reseting chat. Also used by the GC."""
    if admin is True:
        with open(LOGFILE, "w", encoding="utf8") as f_out:
            f_out.write(
                "[SYSTEM]: <font color='#ff7f00'>Chat reset by a admin.</font>\n"
            )
            emit("reset_chat", "admin", broadcast=True, namespace="/")
        return "[SYSTEM]: <font color='#ff7f00'>Chat reset by a admin.</font>\n"
    # if that is not true, run as the GC
    with open(LOGFILE, "w", encoding="utf8") as f_out:
        f_out.write(
            "[SYSTEM]: <font color='#ff7f00'>Chat reset by automatic wipe system.</font>\n"
            + message + "\n")
        emit("reset_chat", "auto", broadcast=True, namespace="/")
    return "[SYSTEM]: <font color='#ff7f00'>Chat reset by automatic wipe system.</font>\n" + message + "\n"


# force the message text to our file containing all the messages
def force_message(message_text):
    """Force send a message to everyone even when chat is locked."""
    with open(LOGFILE, "a", encoding="utf8") as f_in:
        f_in.write(message_text + "\n")
    with open(LOGFILE_B, "a", encoding="utf8") as f_out:
        f_out.write(message_text + "\n")
