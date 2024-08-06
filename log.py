"""log.py: All of the backend logging functions.
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
import os
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

class FileHandler:
    """Class for the backup file."""
    user_position = {}

    def __init__(self, chunk_size):
        self.file_path = 'backend/Chat-backup.txt'
        self.chunk_size = chunk_size
        self.current_position = os.path.getsize('backend/Chat-backup.txt')

    @classmethod
    def generate_handler(cls, uuid):
        """Creates the handler and stores it in the user_position dictionary."""
        cls.user_position[uuid] = FileHandler(500)
        return cls.user_position[uuid]

    @classmethod
    def get_handler(cls, uuid):
        """Gets the handler from the user_position dictionary."""
        backup = cls.user_position.get(uuid, None)
        if backup is None:
            backup = cls.generate_handler(uuid)
        return backup

    def read_chunk(self):
        """Reads a chunk of lines from the file starting at a given position."""
        with open(self.file_path, 'r', encoding='utf-8') as file:
            file.seek(self.current_position)
            lines = [file.readline().strip() for _ in range(self.chunk_size) if file.readline()]
            new_position = file.tell()
        self.current_position = new_position
        return lines

    def read_chunk_reverse(self):
        """Reads a chunk of lines in reverse starting at a given position."""
        lines = []
        with open(self.file_path, 'rb') as file:
            file.seek(0, os.SEEK_END)
            # end_position = file.tell()
            while self.current_position > 0 and len(lines) < self.chunk_size:
                self.current_position -= 1
                file.seek(self.current_position)
                if file.read(1) == b'\n':
                    line = file.readline().decode().strip()
                    if line:
                        lines.insert(0, line)
            if self.current_position == 0:
                file.seek(0)
                line = file.readline().decode().strip()
                if line:
                    lines.insert(0, line)
        return lines

    def reset_position(self):
        """Resets the user's position."""
        self.current_position = os.path.getsize(self.file_path)
        return self.current_position
    