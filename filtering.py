"""Filter usernames and make the chat more xss safe.
    Copyright (C) 2023  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
import re
from datetime import datetime

from better_profanity import profanity
from flask_socketio import emit

import cmds
import log

# import rooms
import word_lists
from online import get_scoketid
from user import User

# old imports, do we still need the markdown package due to us having our own markdown
# from markdown import markdown
# import chat

# get our custom whitelist words (that shouldnot be banned in the first place)
profanity.load_censor_words(whitelist_words=word_lists.whitelist_words)
profanity.add_censor_words(word_lists.censored)


def run_filter_chat(user, room, message, roomid, userid):
    """Its simple now, but when chat rooms come this will be more convoluted."""
    locked = room.locked
    perms = check_perms(user)
    can_send = room.canSend
    user_muted = check_mute(user, roomid)
    limit = user.send_limit()

    # we must check if the current user is acutally them, good idea for this to be first
    if userid != user.uuid:
        # idea lock account if they fail 3 times useing the normal lock
        # or a lock version that doesnt let you login at all
        # without dev help of email fix
        return ('permission', 12, user_muted)

    # userobj = User.get_user_by_id(userid)

    if user_muted:
        return ('permission', 1)

    if bool(re.search(r'[<>]', message)) is True and perms != 'dev':
        # cmds.warn_user(user)
        return ('permission', 10, 0)

    if perms != "dev":
        message = filter_message(message)
        role = profanity.censor(user.role)
    else:
        role = user.role

    profile_picture = '/static/favicon.ico' if user.profile == "" else user.profile
    if "@" in message and not locked:
        if user.locked != 'locked':
            find_pings(message, user.displayName, profile_picture, roomid, room)
        else:
            # cmds.warn_user(user)
            failed_message(('permission', 11, 'locked'), roomid)

    final_str = compile_message(format_text(message), profile_picture, user, role)

    # check if locked or allowed to send
    if locked and perms not in ["dev", 'admin', "mod"]:
        return ("permission", 3, 0)

    if can_send == "everyone":
        return_str = ('msg', final_str, 0)
    elif can_send == 'mod':
        return_str = ('msg', final_str, 0) if perms == 'mod' else ('permission', 5, 0)
    else:
        return_str = ('permission', 5, 0)

    #check for spam then update message count and prev user
    if not limit: #and perms != "dev":
        # cmds.warn_user(user)
        return ('permission', 8, 0)


    if perms in ["dev", "mod"]:
        return_str = ('msg', final_str, 0)

    return return_str

def run_filter_private(user, message, userid):
    """Its simple now, but when chat rooms come this will be more convoluted."""
    perms = check_perms(user)
    user_muted = check_mute(user, None)

    # we must check if the current user is acutally them, good idea for this to be first
    if userid != user.uuid:
        # idea lock account if they fail 3 times useing the normal lock
        # or a lock version that doesnt let you login at all
        # without dev help of email fix
        return ('permission', 12, user_muted)

    # userobj = User.get_user_by_id(userid)

    if user_muted:
        return ('permission', 1)

    if bool(re.search(r'[<>]', message)) is True and perms != 'dev':
        # cmds.warn_user(user)
        return ('permission', 10, 0)

    if perms != "dev":
        message = filter_message(message)
        role = profanity.censor(user.role)
    else:
        role = user.role

    profile_picture = '/static/favicon.ico' if user.profile == "" else user.profile


    final_str = ('msg' ,compile_message(format_text(message),
                                        profile_picture, user, role), 0)

    limit = user.send_limit()
    if not limit: #and perms != "dev":
        # cmds.warn_user(user)
        return ('permission', 8, 0)

    return final_str

def check_mute(user, roomid):
    """Checks if the user is muted or banned."""
    return user.get_perm(roomid)


def check_perms(user):
    """Checks if the user has specal perms else return as a user"""
    return 'dev' if 'Debugpass' in user.perm else 'mod' if 'modpass' in user.perm else\
        'user'


def to_hyperlink(text: str) -> str:
    """Auto hyperlinks any links we find as common."""
    mails = re.findall(r"mailto:(.+?)[\s?]", text, flags=re.M)
    links2 = re.findall(r"(^|[^\/])(www\.[\S]+(\b|$))", text, flags=re.M | re.I)
    pattern = \
        r"(\b(https?|ftp|sftp|file|http):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])"
    links1 = re.findall(
    pattern, text, flags=re.I)

    # Iterate over the results and replace the strings
    for link in mails:
        text = text.replace(f'mailto:{link}', f'<a href="mailto:{link}">{link}</a>')
    for link in links1:
        text = text.replace(link[0], f'<a href="{link[0]}">{link[0]}</a>')
    for link in links2:
        text = text.replace(link[1],
                            f'<a target="_blank" href="{link[1]}">{link[1]}</a>')
    return text


def filter_message(message):
    """No one likes profanity, especially flagging systems."""
    return profanity.censor(message)


def format_text(message):#this system needs notes do not remove
    """Adds the message styling the user requested."""
    bold_pattern = re.compile(r'\*(.*?)\*', re.DOTALL)
    italic_pattern = re.compile(r'/(.*?)/', re.DOTALL)
    underline_pattern = re.compile(r'_(.*?)_', re.DOTALL)
    color_pattern = re.compile(r'\[([a-zA-Z]+)\](.*?)#')

    # Check and apply bold formatting: *text*
    if '*' in message:
        message = bold_pattern.sub(r'<b>\1</b>', message)

    # Check and apply italic formatting: <i>text</i>
    if '/' in message and '__' not in message:
        message = italic_pattern.sub(r'<i>\1</i>', message)

    # Check and apply underline formatting: __text__
    if '_' in message and '__' not in message:
        message = underline_pattern.sub(r'<u>\1</u>', message)

    # Check and apply color formatting: [color]text
    def replace(match):
        color, text = match.groups()
        return f'<span style="color: {color}">{text}</span>'

    if '[' in message:
        message = color_pattern.sub(replace, message)

    return message


def find_pings(message, disp_name, _profile_picture, _roomid, _room):
    """Gotta catch 'em all! (checks for pings in the users message)"""
    pings = re.findall(r'@(\w+|"[^"]+")', message)
    pings = [ping.strip('"') for ping in pings]
    # room = database.find_room({'roomid': roomid}, 'vid')

    for ping in pings:
        # message = message.replace(f"[{ping}", '')
        # print(ping)
        sid = get_scoketid(User.get_userid(ping)) if ping != 'everyone' else None
        emit("ping", {
            "from": disp_name,
            # "pfp": profile_picture,
        },
        namespace="/",
        to=sid if ping != 'everyone' else None,
        broadcast=ping == 'everyone')
        break  # ez one per message fix lol


def find_cmds(message, user, roomid, room):
    """ $sudo commands, 
        will push every cmd found to cmds.py along with the user,
        so we can check if they can do said command.
    """
    command_split = message.split("$sudo")
    command_split.pop(0)
    # command_string = command_split[0]
    # perms = check_perms(user)
    origin_room = None
    # match = re.findall(r"\(|\)", command_string)

    # if perms == 'dev' and roomid == 'jN7Ht3giH9EDBvpvnqRB' and match != []:
    #     match_msg = re.findall(r"\((.*?)\)", command_string)
    #     find_roomid = re.sub(r"\([^()]+\)", "", command_string).strip()
    #     room_check = rooms.check_roomids(find_roomid)
    #     if room_check is False:
    #         failed_message(('permission', 7), roomid)
    #         return
    #     if len(match) == 2:
    #         origin_room = roomid
    #         roomid = find_roomid
    #         command_split = [match_msg[0]]

    if origin_room is None:
        origin_room = roomid
    # this check is needed, due to the finding of commands
    # being after chat lock check in run_filter
    # leading to users being able to send comamnds, even when chat is locked
    # we should be the only ones that can do that (devs)
    for cmd in command_split:
        date_str = datetime.now().strftime("[%a %H:%M] ")
        l_message = date_str + user.username + ":" + cmd
        log.log_commands(l_message)

        command = cmd.split()
        commands = {}

        for index, comm in enumerate(command):
            var_name = ("v" + "%d") % index
            commands[var_name] = comm
        if 'v0' in commands:
            cmds.find_command(commands=commands,
                              user=user,
                              roomid=roomid,
                              origin_room=origin_room,
                              room=room)
            break  # that will work ez one per message fix lol


def compile_message(message, profile_picture, user, role):
    """Taken from old methold of making messages"""
    to_hyperlink(message)
    profile = f"<img class='pfp' src='{profile_picture}'></img>"
    user_string = f"<font color='{user.Ucolor}'>{user.displayName}</font>"
    message_string = f"<font color='{user.Mcolor}'>{message}</font>"
    role_string = do_dev_easter_egg(role, user)
    date_str = datetime.now().strftime("[%a %I:%M %p] ")
    message_string_h = to_hyperlink(message_string)

    message = f"{date_str}{profile} {user_string} ({role_string}) - {message_string_h}"
    return message


def do_dev_easter_egg(role, user):
    """Because we want RAINBOW changing role names."""
    role_color = user.Rcolor
    if role_color == "#00ff00":
        role_string = "<font class='Dev_colors-loop'>" + role + "</font>"
    elif role_color == "rainbow":
        role_string = "<font class='rainbow-text-loop'>" + role + "</font>"
    else:
        role_string = "<font color='" + role_color + "'>" + role + "</font>"
    return role_string


def failed_message(result, roomid):
    """Find the response the client needs for why their message can't be sent."""
    # maybe later we can move these to a file?
    # also why do we use a tuple here for these entries?
    # they could just be ints and it work still
    fail_strings = {
        (1):
        "You can't send messages here because you are muted.",
        (2):
        "You can't send messages here because you have been banned.",
        (3):
        "You can't send messages here because this chat room has been locked.",
        (4):
        "You can't send messages here because you have been banned from this chat room",
        (5):
        "You can't send messages here due to lack of permissions for this chat room.",
        (6):
        "This chat room no longer exists, select a chat room that does exist.",
        (7):
        "This chat room vid does not exist.",
        (8):
        "You are not allowed to send more than 15 messages in a row.\
        You have been muted for 5 minutes(Warning)",
        (9):
        "You must verify your account before you can use this command.",
        (10):
        "You are not allowed to send code in the chat. (Warning)",
        (11):
        "You are not allowed to ping other users. (Warning)",
        (12):
        "Are you trying to do some funny business? (You failed lol)",
    }
    # if result[0] == "dev/mod":
    #     if result[1] == 6: fail_str = fail_strings.get((result[1]), "")
    #     else: return
    # if result[0] == "return": emit("message_chat", ('', roomid), namespace="/")
    # ^^^^ what is this? no clue

    fail_str = fail_strings.get((result[1]), "")  # result[2]), "")
    # I love fstrings
    final_str = f"[SYSTEM]: <font color='#ff7f00'>{fail_str}</font>"
    emit("message_chat", (final_str, roomid), namespace="/")


def is_user_expired(permission_str):
    """Checks if the time of a user being muted has expired."""
    parts = permission_str.split(' ')
    if len(parts) == 3 and parts[0] == 'muted':
        expiration_time_str = ' '.join(parts[1:])
        expiration_time = datetime.strptime(expiration_time_str,
                                            "%Y-%m-%d %H:%M:%S")
        current_time = datetime.now()
        return current_time >= expiration_time


def is_warned_expired(warned_str):
    """Check if the time a user has been warned has expired."""
    parts = warned_str.split(' ')
    if len(parts) == 2:
        expiration_time_str = ''.join(parts[1:])
        expiration_time = datetime.strptime(expiration_time_str,
                                            "%Y-%m-%d %H:%M:%S")
        current_time = datetime.now()
        return current_time >= expiration_time
