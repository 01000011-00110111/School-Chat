"""filtering.py: Filtering for usernames, and general formatting.
    Copyright (C) 2023, 2024  cserver45, cseven
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
profanity.add_censor_words(word_lists.blacklist_words)


def run_filter_chat(user, room, message, roomid, userid):
    """Its simple now, but when chat rooms come this will be more convoluted."""
    locked = room.config.locked
    perms = check_perms(user)
    can_send = room.config.can_send
    user_muted = check_mute(user, roomid)
    limit = user.send_limit()

    # we must check if the current user is acutally them, good idea for this to be first
    if userid != user.uuid:
        # idea lock account if they fail 3 times using the normal lock
        # or a lock version that doesnt let you login at all
        # without dev help of email fix
        return ('permission', 12, user_muted)

    # userobj = User.get_user_by_id(userid)

    if user_muted:
        return ('permission', 1)

    if bool(re.search(r'[<>]', message)) is True and perms != 'dev':
        # cmds.warn_user(user)
        return ('permission', 10, 0)

    # if perms != "dev":
    message = format_text(message)
    role = profanity.censor(user.role)
    # else:
        # role = user.role

    profile_picture = '/static/favicon.ico' if user.profile == "" else user.profile
    if "@" in message and not locked:
        find_pings(message, user.display_name, user, roomid, room)

    final_str = compile_message(message, profile_picture, user, role)

    # check if locked or allowed to send
    if locked and perms not in ["dev", 'admin', "mod"]:
        return ("permission", 3, 0)

    if can_send == "everyone":
        return_str = ('msg', final_str, 0)
    elif can_send == 'mod':
        return_str = ('msg', final_str, 0)
    else:
        return_str = ('permission', 5, 0)

    #check for spam then update message count and prev user
    if not limit:
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

    # if perms != "dev":
    message = format_text(message)
    role = profanity.censor(user.role)
    # else:
        # role = user.role

    profile_picture = '/static/favicon.ico' if user.profile == "" else user.profile


    final_str = ('msg' ,compile_message(message,
                                        profile_picture, user, role), 0)

    limit = user.send_limit()
    if not limit:
        return ('permission', 8, 0)

    return final_str

def check_mute(user, roomid):
    """Checks if the user is muted or banned."""
    return user.get_perm(roomid)


def check_perms(user):
    """Checks if the user has specal perms else return as a user"""
    return 'dev' if 'Debugpass' in user.perm else 'mod' if 'modpass' in user.perm else\
        'user'


def to_hyperlink(text: str) -> tuple[str, list[str]]:
    """Auto hyperlinks any links we find as common and returns the hyperlinked parts."""
    link_pattern = \
    r"(\b(https?|ftp|sftp|file|http):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])"
    mails = re.findall(r"mailto:(.+?)([\s]|$)", text)
    www_links = re.findall(r"(^|[^\/])(www\.[\S]+)", text)
    links = re.findall(link_pattern, text, flags=re.I)

    # Track modifications
    modifications = []

    # Process mailto links
    for mail in mails:
        mail_address = mail[0]
        original_text = f'mailto:{mail_address}'
        replacement_text = f'<a href="mailto:{mail_address}">{mail_address}</a>'
        if original_text in text:
            text = text.replace(original_text, replacement_text)
            modifications.append(replacement_text)

    # Process www links
    for url in www_links:
        www_link = url[1]
        original_text = f'www.{www_link}'
        replacement_text = f'<a target="_blank" href="http://{www_link}">{original_text}</a>'
        if original_text in text:
            text = text.replace(original_text, replacement_text)
            modifications.append(replacement_text)

    # Process http/https/ftp/sftp/file links
    for link in links:
        link_url = link[0]
        replacement_text = f'<a target="_blank" href="{link_url}">{link_url}</a>'
        if link_url in text:
            text = text.replace(link_url, replacement_text)
            modifications.append(replacement_text)

    return text, modifications



def filter_message(message):
    """No one likes profanity, especially flagging systems."""
    return profanity.censor(message)


def format_text(message):  # this system needs notes do not remove
    """Adds the message styling the user requested."""
    bold_pattern = re.compile(r'\*(.*?)\*', re.DOTALL)
    italic_pattern = re.compile(r'/(.*?)/', re.DOTALL)
    underline_pattern = re.compile(r'_(.*?)_', re.DOTALL)
    color_pattern = re.compile(r'\[([a-zA-Z]+)\](.*?)#')

    message, modifications = to_hyperlink(message)

    if '*' in message:
        message = bold_pattern.sub(lambda m: f'<b>{m.group(1)}</b>'\
                                   if m.group(1).strip() else m.group(0), message)

    if '/' in message:
        message = italic_pattern.sub(lambda m: f'<i>{m.group(1)}</i>'\
            if m.group(1).strip() else m.group(0), message)

    if '_' in message:
        message = underline_pattern.sub(lambda m: f'<u>{m.group(1)}</u>'\
            if m.group(1).strip() else m.group(0), message)

    def replace(match):
        color, text = match.groups()
        formatted_text = f'<span style="color: {color}">{text}</span>'
        if text.strip() and formatted_text not in modifications:
            return formatted_text
        return match.group(0)

    if '[' in message:
        message = color_pattern.sub(replace, message)

    return filter_message(message)



def find_pings(message, disp_name, user, roomid, _room):
    """Gotta catch 'em all! (checks for pings in the users message)"""
    if user.locked == 'locked':
        failed_message(('permission', 11, 'locked'), roomid)
        return
    users_pinged = []
    pings = re.findall(r'@([^\s@"]+|"[^"]*")', message)
    pings = [ping.strip('"') for ping in pings]
    # room = database.find_room({'roomid': roomid}, 'vid')

    for ping in pings:
        other_user = User.get_userid(ping) if ping != 'everyone' else None
        sid = get_scoketid(other_user) if ping != 'everyone' else None
        users_pinged.append(other_user)
        if ping == 'everyone':
            emit("ping", {"from": disp_name}, namespace='/', broadcast=True)
        if sid is not None:
            emit("ping", {"from": disp_name}, namespace='/', to=sid)


def find_cmds(message, user, roomid, room):
    """ $sudo commands, 
        will push every cmd found to cmds.py along with the user,
        so we can check if they can do said command.
    """
    command_split = message.split("$sudo")
    command_split.pop(0)
    origin_room = None

    if origin_room is None:
        origin_room = roomid
    # this check is needed, due to the finding of commands
    # being after chat lock check in run_filter
    # leading to users being able to send comamnds, even when chat is locked
    # we should be the only ones that can do that (devs)
    for cmd in command_split:
        date_str = datetime.now().strftime("[ %a %I:%M %p] ")
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
    profile = f"<img class='message_pfp' src='{profile_picture}'></img>"
    user_string = f"<p style='color:{user.u_color}'>{user.display_name}</p>"
    message_string = f"<p color='{user.m_color}'>{message}</p>"
    role_string = f"<p style='background: {user.r_color}; color: #ffffff;' class='badge'> {role}</p>"
    date_str = datetime.now().strftime("%a %I:%M %p ")
    # message_string_h = to_hyperlink(message_string)

    message = f"<div class='message'> <div class='message_image_content'>{profile}</div> <div class='message_content'><div class='user_info_div'>{user_string}<p>*</p> <p>{date_str}</p> {role_string}</div> <div class='user_message_div'>{message_string}</div> </div></div>"
    return message


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
        """You are not allowed to send more than 15 messages in a row.
        You have been muted for 5 minutes(Warning)""",
        (9):
        "You must verify your account before you can use this command.",
        (10):
        "You are not allowed to send code in the chat. (Warning)",
        (11):
        "You are not allowed to ping other users. (Warning)",
        (12):
        "Are you trying to do some funny business? (You failed lol)",
    }

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
    return None


def is_warned_expired(warned_str):
    """Check if the time a user has been warned has expired."""
    parts = warned_str.split(' ')
    if len(parts) == 2:
        expiration_time_str = ''.join(parts[1:])
        expiration_time = datetime.strptime(expiration_time_str,
                                            "%Y-%m-%d %H:%M:%S")
        current_time = datetime.now()
        return current_time >= expiration_time
    return None
