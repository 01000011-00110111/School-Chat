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
# import word_lists
from online import get_scoketid
from user import User
from commands.other import format_system_msg

# old imports, do we still need the markdown package due to us having our own markdown
# from markdown import markdown
# import chat

# get our custom whitelist words (that shouldnot be banned in the first place)
def setup_filter(wl, bl):
    """sets up the whitelisted and blacklisted words."""
    profanity.load_censor_words(whitelist_words=wl)
    profanity.add_censor_words(bl)
    return


def run_filter_chat(user, room, message, roomid, userid):
    #pylint: disable=E1121
    """Its simple now, but when chat rooms come this will be more convoluted."""
    limit = user.send_limit(room)
    perms = check_perms(user)
    if userid != user.uuid:
        # idea lock account if they fail 3 times using the normal lock
        # or a lock version that doesnt let you login at all
        # without dev help of email fix
        return ('permission', 12, False)


    if room.config.locked and perms not in ["dev", 'admin', "mod"]:
        return ("permission", 3, 0)

    if room.config.can_send == 'mod' and perms not in ["mod", "admin", "dev"]:
        return ('permission', 5, 0)

    if bool(re.search(r'[<>]', message)) and perms != 'dev':
        # cmds.warn_user(user)
        return ('permission', 10, 0)

    if check_mute(user, room):
        if not limit:
            return ('permission', 8, 0)
        return ('permission', 1)

    message = format_text(message)

    profile_picture = '/static/favicon.ico' if user.profile == "" else user.profile
    if "@" in message and not room.config.locked:
        find_pings(message, user.display_name, user, roomid, room)

    final_str = compile_message(message, profile_picture, user)

    return ('msg', final_str, 0)


def run_filter_private(user, message, userid):
    #pylint: disable=E1121
    """Its simple now, but when chat rooms come this will be more convoluted."""
    perms = check_perms(user)
    user_muted = False# check_mute(user, None)

    if userid != user.uuid:
        return ('permission', 12, user_muted)

    if user_muted:
        return ('permission', 1, False)

    if "<>" in message and perms != 'dev':
        return ('permission', 10, False)

    message = format_text(message)

    profile_picture = '/static/favicon.ico' if user.profile == "" else user.profile

    final_str = ('msg', compile_message(message,
                                        profile_picture, user), 0)

    # limit = user.send_limit(room)
    # if not limit:
    #     return ('permission', 8, 0) BROKEN

    return final_str

def check_mute(user, room):
    """Checks if the user is muted or banned."""
    return room.check_user(user)


def check_perms(user):
    """Checks if the user has specal perms else return as a user"""
    return 'dev' if 'Debugpass' in user.perm else 'admin' if 'adminpass'\
          in user.perm else 'mod' if 'modpass' in user.perm else\
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


def format_text(message):
    """Adds the message styling the user requested."""
    message, modifications = to_hyperlink(message)

    patterns = [
        (re.compile(r'\*(.*?)\*', re.DOTALL), r'<b>\1</b>'),
        (re.compile(r'~(.*?)~', re.DOTALL), r'<i>\1</i>'),
        (re.compile(r'_(.*?)_', re.DOTALL), r'<u>\1</u>'),
        (re.compile(r'\[([a-zA-Z]+)\](.*?)#'), lambda m: f'<span style="color:\
        {m.group(1)}">{m.group(2)}</span>' if m.group(2).strip() and\
            m.group(0) not in modifications else m.group(0))
    ]

    for pattern, repl in patterns:
        message = pattern.sub(repl, message)

    return filter_message(message)



def find_pings(message, disp_name, user, roomid, _room):
    """Gotta catch 'em all! (checks for pings in the users message)"""
    if user.locked == 'locked':
        failed_message(('permission', 11, 'locked'), roomid)
        return

    pings = re.findall(r'@([^\s@"]+|"[^"]*")', message)
    pings = [ping.strip('"') for ping in pings]

    users_pinged = [User.get_userid(ping) for ping in pings if ping != 'everyone']
    sids = [get_scoketid(usr) for usr in users_pinged if usr is not None]

    if 'everyone' in pings:
        emit("ping", {"from": disp_name}, namespace='/', broadcast=True)

    if sids:
        emit("ping", {"from": disp_name}, namespace='/', to=sids)


def find_cmds(message, user, roomid, room):
    """ $sudo commands, 
        will push every cmd found to cmds.py along with the user,
        so we can check if they can do said command.
    """
    command_split = message.split("$sudo")
    if len(command_split) > 1:
        command = command_split[1].split()
        commands = {f"v{i}": cmd for i, cmd in enumerate(command)}

        date_str = datetime.now().strftime("[ %a %I:%M %p] ")
        l_message = date_str + user.username + ":" + command_split[1]
        log.log_commands(l_message)

        cmds.find_command(commands=commands,
                          user=user,
                          roomid=roomid,
                          origin_room=roomid,
                          room=room)


def compile_message(message, profile_picture, user):
    """Taken from old methold of making messages"""
    u_color = user.u_color
    m_color = user.m_color
    r_color = user.r_color
    display_name = user.display_name
    role = profanity.censor(user.role)
    perm = check_perms(user)
    badges = [f"<p style='background:{badge[1]}; color: {badge[2]};' class='badge'>{badge[0]}</p>"
              for badge in user.badges]

    return {
        'profile': f"<img class='message_pfp' src='{profile_picture}'></img>",
        'user': f"<p style='color:{u_color}'>{display_name}</p>",
        'message': f"<p style='color:{m_color}'>{message}</p>",
        'badges': [f"<p style='background:{r_color}; color: #ffffff;' class='badge'>{role}</p>",
                   f"<p style='background:{perm}; color: #ffffff;' class='badge {perm}'>\
      {perm}</p>" if perm != 'user' else None] + badges,
        'date': datetime.now().strftime("%a %b %d %I:%M %p")
    }


def failed_message(result, roomid):
    """Find the response the client needs for why their message can't be sent."""
    fail_strings = {
    0: "need to figure out how to solve this. I don't think anyone can see this message. -cseven",
    1: "You can't send messages here because you are muted. Next time don't get muted.",
    2: "You can't send messages here because you have been banned. what a loser.",
    3: "You can't send messages here because this chat room has been locked.",
    4: "You can't send messages here because you have been banned from this chat room. Say sorry.",
    5: """You can't send messages here due to lack of permissions for this chat room.
            Just ask for permission whats the worst that can happen.""",
    6: """This chat room no longer exists, select a chat room that does exist,
        or just sit alone with youself""",
    7: "This chat room does not exist. Make so it then",
    8: """You are not allowed to send more than 15 messages in a row.
    You have been muted for 5 minutes(Warning) Good job now you have to wait!""",
    9: "You must verify your account before you can use this command.",
    10: "You are not allowed to send code in the chat. (Warning)",
    11: "You are not allowed to ping other users. (Warning)",
    12: "Are you trying to do some funny business? (You failed lol)",
    }

    fail_str = fail_strings.get(result[1], "")
    final_str = format_system_msg(fail_str)
    emit("message_chat", (final_str, roomid), namespace="/")


# def is_user_expired(permission_str):
#     """Checks if the time of a user being muted has expired."""
#     parts = permission_str.split(' ')
#     if len(parts) == 3 and parts[0] == 'muted':
#         expiration_time_str = ' '.join(parts[1:])
#         expiration_time = datetime.strptime(expiration_time_str,
#                                             "%Y-%m-%d %H:%M:%S")
#         current_time = datetime.now()
#         return current_time >= expiration_time
#     return None


# def is_warned_expired(warned_str):
#     """Check if the time a user has been warned has expired."""
#     parts = warned_str.split(' ')
#     if len(parts) == 2:
#         expiration_time_str = ''.join(parts[1:])
#         expiration_time = datetime.strptime(expiration_time_str,
#                                             "%Y-%m-%d %H:%M:%S")
#         current_time = datetime.now()
#         return current_time >= expiration_time
#     return None
