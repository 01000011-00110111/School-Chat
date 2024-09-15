"""setup.py: Inital setup functions on first run.
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
import configparser
import os

from database import Access, Messages, Private
from commands.other import format_system_msg


def chcek_if_data_is_missing():
    """checks if a certain value is there."""
    # users = Permission.find()
    # for user in users:
    #     if 'themeCount' not in user or user['themeCount'] is None:
    #         Permission.update_one({'userId': user['userId']}, {'$set': {'themeCount': 0}})
    rooms = Access.find()
    for room in rooms:
        if 'user_data' not in room or room['user_data'] is None:
            Access.update_one({'roomid': room['roomid']}, {'$set': {'user_data': {}}})
        if 'muted' not in room or room['muted'] is None:
            Access.update_one({'roomid': room['roomid']}, {'$set': {'muted': {}}})
        if 'banned' not in room or room['banned'] is None:
            Access.update_one({'roomid': room['roomid']}, {'$set': {'banned': {}}})

    messages = Messages.find()
    for message in messages:
        Messages.update_one({'roomid': message['roomid']}, {'$set': {'messages': \
        [format_system_msg("Chat has been reset due to new message format.")]}})
    private = Private.find()
    for pm in private:
        Private.update_one({'pmid': pm['pmid']}, {'$set': {'messages': \
        [format_system_msg("Chat has been reset due to new message format.")]}})




def self_destruct():
    """Deletes this file"""
    script_path = os.path.abspath(__file__)
    try:
        config = configparser.ConfigParser()
        config.read("config/keys.conf")
        if config['backend']['ENV'] != 'development':
            os.remove(script_path)
        print(f'Script {script_path} has been deleted.')
    except TypeError as e:
        print(f'Error deleting script {script_path}: {e}')