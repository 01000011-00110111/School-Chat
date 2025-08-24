"""filtering.py: Improved Filtering for usernames, permissions, and formatting.
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""

import re
from datetime import datetime
from better_profanity import profanity

# import cmds
# import log
# from user import User
# from commands.other import format_system_msg
from chat.chat import Chat
# from system import format_system_msg

def setup_filter(whitelist, blacklist, file):
    """Sets up whitelisted and blacklisted words."""
    if file:
        with open(file + '_blacklist', 'r', encoding='utf-8') as f:
            blacklist = f.read().splitlines()
        with open(file + '_whitelist', 'r', encoding='utf-8') as f:
            whitelist = f.read().splitlines()
    profanity.load_censor_words(whitelist_words=whitelist)
    profanity.add_censor_words(blacklist)

def check_permissions(user):
    """Returns the highest permission level for a user."""
    if 'Debugpass' in user.perm:
        return 'dev'
    if 'adminpass' in user.perm:
        return 'admin'
    if 'modpass' in user.perm:
        return 'mod'
    return 'user'

def check_mute(user, room):
    """Checks if the user is muted or banned."""
    return room.check_user(user) if room else False

def filter_message(message):
    """Applies profanity filtering to messages."""
    return profanity.censor(message)

def format_text(message):
    """Formats text with styling and hyperlinking."""
    message, modifications = to_hyperlink(message)
    
    patterns = [
        (re.compile(r'\*(.*?)\*', re.DOTALL), r'<b>\1</b>'),
        (re.compile(r'~(.*?)~', re.DOTALL), r'<i>\1</i>'),
        (re.compile(r'_(.*?)_', re.DOTALL), r'<u>\1</u>'),
        (re.compile(r'\[([a-zA-Z]+)\](.*?)#'), lambda m: f'<span style="color:{m.group(1)}">{m.group(2)}</span>'
         if m.group(2).strip() and m.group(0) not in modifications else m.group(0))
    ]
    
    for pattern, repl in patterns:
        message = pattern.sub(repl, message)
    
    return filter_message(message)

def to_hyperlink(text):
    """Converts URLs and emails to clickable links."""
    link_pattern = r'\b(https?|ftp|file)://[-A-Z0-9+&@#/%?=~_|!:,.;]*[-A-Z0-9+&@#/%=~_|]'
    mail_pattern = r'mailto:([^\s]+)'  # Matches mailto links
    www_pattern = r'(^|[^/])(www\.[\S]+)'  # Matches www links
    
    modifications = []
    
    for match in re.findall(mail_pattern, text):
        text = text.replace(f'mailto:{match}', f'<a href="mailto:{match}">{match}</a>')
        modifications.append(match)
    
    for match in re.findall(www_pattern, text):
        www_link = match[1]
        text = text.replace(f'www.{www_link}', f'<a target="_blank" href="http://{www_link}">www.{www_link}</a>')
        modifications.append(www_link)
    
    for match in re.findall(link_pattern, text, flags=re.I):
        text = text.replace(match, f'<a target="_blank" href="{match}">{match}</a>')
        modifications.append(match)
    
    return text, modifications

def compile_message(message, profile_picture, user):
    """Generates the structured message dictionary with updated formatting."""
    u_color = user.u_color
    m_color = user.m_color
    r_color = user.r_color
    display_name = user.display_name
    role = profanity.censor(user.role)
    # perm = check_perms(user)
    perm = 'user'
    #badges = [f"<p style='background:{badge[1]}; color: {badge[2]};' class='badge'>{badge[0]}</p>"
             # for badge in user.badges]

    profile = "<img class='user_profile_picture' src='/icons/favicon.ico'></img>"
    user_string = f"<p style='color: {u_color};'>{display_name}</p>"
    message_string = f"<p style='color: {m_color};'>{message}</p>"
    role_string = f"<p style='background:{r_color}; color: #ffffff;' class='badge'>{role}</p>"
    perm_string = (f"<p style='background:{perm}; color: #ffffff;' class='badge {perm}'>"
                   f"{perm}</p>" if perm != 'user' else None)
    date_str = datetime.now().strftime("%a %I:%M %p ")

    return {
        'profile': profile,
        'user': user_string,
        'message': message_string,
        'badges': [role_string, perm_string],# + badges,
        'date': date_str
    }


# def failed_message(reason_code, roomid):
#     """Handles failure messages based on permission checks."""
#     fail_reasons = {
#         1: "You are muted and cannot send messages.",
#         2: "You are banned from this chat room.",
#         3: "This chat room is locked.",
#         4: "You lack permissions to send messages here.",
#         5: "You do not have permission to use this command.",
#         6: "You must verify your account before using this feature.",
#         7: "Pings are not allowed.",
#         8: "No sending code in chat.",
#     }
#     fail_msg = fail_reasons.get(reason_code, "Unknown error occurred.")
#     semit("message_chat", (format_system_msg(fail_msg), roomid), namespace="/")

def run_filter_chat(user, roomid, message, suuid):
    """Filters messages before sending in a chat room."""
    room = Chat.get_chat(roomid)
    reset = False
    if suuid != user.suuid:
        return ('permission', 7, False)


    perms = check_permissions(user)
    if room.config["locked"] is True and perms not in ['dev', 'admin', 'mod']:
        return ('permission', 3, 0)

    if room.config["can_send"] == 'mod' and perms not in ['mod', 'admin', 'dev']:
        return ('permission', 4, 0)

    if "$sudo rc" in message and perms not in ['dev', 'admin', 'mod']:
        return ('permission', 5, 0)
    elif "$sudo rc" in message and perms in ['dev', 'admin', 'mod']:
        reset = True

    if re.search(r'<[^>]*>', message):
        return ('permission', 8, 0)

    # if check_mute(user, room):
    #     return ('permission', 1, 0)

    message = format_text(message)
    return ('msg', compile_message(message, None, user), 0, reset)


setup_filter("/chat/whitelist.txt", "/chat/blacklist.txt", True)