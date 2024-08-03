"""Setup file (might rework).
    Copyright (C) 2023  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
import os

from database import Permission


def chcek_if_data_is_missing():
    """checks if a certain value is there."""
    users = Permission.find()
    for user in users:
        if 'themeCount' not in user or user['themeCount'] is None:
            Permission.update_one({'userId': user['userId']}, {'$set': {'themeCount': 0}})


def self_destruct():
    """Deletes this file"""
    script_path = os.path.abspath(__file__)
    try:
        os.remove(script_path)
        print(f'Script {script_path} has been deleted.')
    except TypeError as e:
        print(f'Error deleting script {script_path}: {e}')
