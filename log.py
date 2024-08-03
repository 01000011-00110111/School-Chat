"""All of the backend logging functions.
    Copyright (C) 2023  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
from collections import deque
from datetime import datetime

import database


def format_system_msg(msg):
    """Format a message [SYSTEM] would send."""
    return f'[SYSTEM]: <font color="#ff7f00">{msg}</font>'

def log_accounts(message):
    """Log when something happens to an account."""
    with open('backend/accounts.txt', 'a', encoding="utf8") as file:
        file.write(message + '\n')

def log_commands(message) -> None:
    """Log when a command is issued."""
    with open('backend/command_log.txt', 'a', encoding="utf8") as file:
        file.write(message + '\n')


def log_mutes(message) -> None:
    """Log when a unmuted user is issued."""
    with open('backend/permission.txt', 'a', encoding="utf8") as file:
        file.write(message + '\n')


def get_room_logs() -> str:
    """Return a sendable str with the last 10 Room Log Entries."""
    with open("backend/chat-rooms_log.txt", "r", encoding="utf-8") as f:
        cmds_log = deque(f, 10)
    cmd_log_txt = ""
    cmd_log_txt = "<br>".join(f"{cmd}" for cmd in cmds_log)
    return format_system_msg(f"Last 10 Room Log Entries:<br>{cmd_log_txt}\n")


def get_cmd_logs() -> str:
    """Return a sendable str with the last 10 Command Log Entries."""
    with open("backend/command_log.txt", "r", encoding="utf-8") as f:
        cmds_log = deque(f, 10)
    cmd_log_txt = ""
    cmd_log_txt = "<br>".join(f"{cmd}" for cmd in cmds_log)
    return format_system_msg(f"Last 10 Command Log Entries:<br>{cmd_log_txt}\n")

def backup_log(message_text: str, roomid: str, private: bool) -> None:
    """adds the newest message from any chat rooom in the backup file"""
    with open("backend/Chat-backup.txt", "a", encoding="utf8") as f_out:
        date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S: ")
        room = database.find_room({"roomid": roomid}, 'vid')
        if private:
            name = "Private Room"
        else:
            name = room["roomName"] if roomid != "all" else "All rooms"
        f_out.write(
            f"[{date}], [{name}, Roomid: ({roomid})] The message said: {message_text}\n"
        )
