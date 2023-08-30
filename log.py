"""All of the backend logging functions.
    Copyright (C) 2023  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
from collections import deque


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
    with open("backend/chat-rooms_log.txt", "r") as f:
        cmds_log = deque(f, 10)
    cmd_log_txt = ""
    for cmd in cmds_log:
        cmd_log_txt += f"{cmd}<br>"
    return f"[SYSTEM]: <font color='#ff7f00'>Last 10 Room Log Entries:<br>{cmd_log_txt}</font>\n"


def get_cmd_logs() -> str:
    """Return a sendable str with the last 10 Command Log Entries."""
    with open("backend/command_log.txt", "r") as f:
        cmds_log = deque(f, 10)
    cmd_log_txt = ""
    for cmd in cmds_log:
        cmd_log_txt += f"{cmd}<br>"
    return f"[SYSTEM]: <font color='#ff7f00'>Last 10 Command Log Entries:<br>{cmd_log_txt}</font>\n"