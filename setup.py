"""setup.py: Inital setup functions on first run.
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
import configparser
import os

from database import Access, Messages, Private, Customization
from commands.other import format_system_msg

config = configparser.ConfigParser()
config.read("config/keys.conf")


def chcek_if_data_is_missing():
    """checks if a certain value is there."""
    if config['main']['version'] != 'v1.5-beta.1':
        costom = Customization.find()
        for custom in costom:
            if 'badges' not in custom or custom['badges'] is None:
                Customization.update_one({'userId': custom['userId']}, {'$set': {'badges': []}})
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
        config['main']['version'] = 'v1.5-beta.1'




def self_destruct():
    """Deletes this file"""
    script_path = os.path.abspath(__file__)
    try:
        if config['backend']['ENV'] != 'development':
            os.remove(script_path)
        print(f'Script {script_path} has been deleted.')
    except TypeError as e:
        print(f'Error deleting script {script_path}: {e}')
