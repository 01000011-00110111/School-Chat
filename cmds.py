"""All commands ran by devs, mods, users, etc.
    Copyright (C) 2023  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
from datetime import datetime, timedelta

from flask_socketio import emit

from commands import debug, moderation, online, other, room
# from main import scheduler

# consts
troll_str = """
                [SYSTEM]: <font color='#ff7f00'>YOUVE BEEN TROLOLOLOLLED</font>
                <img src='static/troll-face.jpeg'>
            """
            

def find_command(**kwargs):
    """Send whatever sudo command is issued to its respective function."""
    vid = kwargs['roomid']
    dev_commands = {
        'status': debug.status,
        'pstats': debug.pstats,
        'lines': debug.line_count,
        'rc': room.reset_chat_user,
        'clear_mutes': debug.clear_all_mutes,
    }
    admin_commands = {
        'cmd_logs': debug.send_cmd_logs,
        'globalock': moderation.globalock,
        'admin': other.send_admin,
        'ban': moderation.ban,
        'unban': moderation.unban,
        'word_ban': moderation.remove_word_from_unban_list,
        "word_unban": moderation.add_word_to_unban_list,
        # 'globalunlock': moderation.globalunlock,
    }
    mod_commands = {
        'lock': moderation.lock,
        'unlock': moderation.unlock,
        'reset': room.reset_chat_user,
        'mute': moderation.mute,
        'unmute': moderation.unmute,
    }
    basic_commands = {
        'help': other.help,
        'song': other.song,
        # 'refresh': online.refresh_online,
        # 'offline': online.appear_offline,
        # 'online': online.appear_online,
        'ping': debug.ping,
        'ecount': other.E_count_bacup,
        'create': room.create_room,
        # 'popular': other.most_used_room,
    }
    command = kwargs['commands']['v0']
    perm = permission(kwargs['user'])
    if command in dev_commands:
        # print('dev')
        dev_commands[command](**kwargs) if perm in ['dev'] else \
            other.respond_command((0, 'dev'), vid)
    if command in admin_commands:
        # print('admin')
        admin_commands[command](**kwargs) if perm in ['dev', 'admin'] else \
            other.respond_command((0, 'admin'), vid)
    if command in mod_commands:
        mod_commands[command](**kwargs) if perm in ['dev', 'admin', 'mod'] else \
            other.respond_command((0, 'mod'), vid)
    if command in basic_commands:
        try:
            basic_commands[command](**kwargs)
        except Exception:
            other.respond_command((0, None), vid)
    # try:
    #     response_strings[(kwargs['commands']['v0'], permission(kwargs['user']))] \
    #         (**kwargs)
    # except KeyError:
    #     other.respond_command(("result", 1, None), kwargs['roomid'])#, None)
    # key = (kwargs['commands']['v0'], permission(kwargs['user']))
    # if key in response_strings and callable(response_strings[key]):
    #     response_strings[key](**kwargs)
    # else:
    #     print("Invalid action or permission level")

def permission(user):
    """get the users permission"""
    return 'dev' if 'Debugpass' in user.perm else 'admin' \
        if 'adminpass' in user.perm else 'mod' \
        if 'modpass' in user.perm else None
    # in the 1.4 update ill add room mods back modpass


def warn_user(user):
    """adds a new warning to the user"""
    # warn_count = user.warned.split(' ')
    current_time = datetime.now()
    expiration_time = current_time + timedelta(days=30)
    date = expiration_time.strftime("%Y-%m-%d %H:%M:%S")
    warn_updated = int(warn_count[0]) + 1
    dbm.Accounts.update_one(
        {"username": user.username},
        {'$set': {
            'warned': f"{str(warn_updated)} {date}"
        }})
