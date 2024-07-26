import os

from database import Permission


def chcek_if_data_is_missing():
    users = Permission.find()
    for user in users:
        if 'themeCount' not in user or user['themeCount'] is None:
            Permission.update_one({'userId': user['userId']}, {'$set': {'themeCount': 0}})


def self_destruct():
    script_path = os.path.abspath(__file__)
    try:
        os.remove(script_path)
        print(f'Script {script_path} has been deleted.')
    except Exception as e:
        print(f'Error deleting script {script_path}: {e}')