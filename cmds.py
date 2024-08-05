"""cmds.py: All commands ran by devs, mods, users, etc.
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
# from datetime import datetime, timedelta

# from flask_socketio import emit

from commands import debug, moderation, other, online_commands, room

# from main import scheduler

# consts
TROLL_STR = """
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
        'report_list': moderation.list_reports,
    }
    basic_commands = {
        'help': other.help_command,
        'song': other.song,
        'offline': online_commands.appear_offline,
        'online': online_commands.appear_online,
        'ping': debug.ping,
        'ecount': other.e_count_backup,
        'create': room.create_room,
        'report': moderation.report_user,
        # 'popular': other.most_used_room,
    }
    command = kwargs['commands']['v0']
    perm = permission(kwargs['user'])
    if command in dev_commands:
        if perm in ['dev']:
            dev_commands[command](**kwargs)
        else:
            other.respond_command((0, 'dev'), vid)

    if command in admin_commands:
        if perm in ['dev', 'admin']:
            admin_commands[command](**kwargs)
        else:
            other.respond_command((0, 'admin'), vid)
    if command in mod_commands:
        if perm in ['dev', 'admin', 'mod']:
            mod_commands[command](**kwargs)
        else:
            other.respond_command((0, 'mod'), vid)
    if command in basic_commands:
        try:
            basic_commands[command](**kwargs)
        except EnvironmentError:
            other.respond_command((0, None), vid)


def permission(user):
    """get the users permission"""
    return 'dev' if 'Debugpass' in user.perm else 'admin' \
        if 'adminpass' in user.perm else 'mod' \
        if 'modpass' in user.perm else None
    # in the 1.5 update ill add room mods back modpass
