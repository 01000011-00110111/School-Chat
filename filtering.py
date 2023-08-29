"""Filter usernames and make the chat more xss safe.
    Copyright (C) 2023  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
import re
from datetime import datetime, timezone, timedelta
from better_profanity import profanity
from flask_socketio import emit
# from markdown import markdown
import chat
import profanity_words
import cmds
import log
import rooms

# get our custom whitelist words (that shouldnot be banned in the first place)
profanity.load_censor_words(whitelist_words=profanity_words.whitelist_words)
profanity.add_censor_words(profanity_words.censored)
preuser = 'system'
message_count = 0


def run_filter(user, room, message, roomid):
    """Its simple now, but when chat rooms come this will be more convoluted."""
    global preuser
    global message_count
    locked = check_lock(room)
    perms = check_perms(user)
    can_send = check_allowed_sending(user, room)
    user_muted = check_mute(user)

    if user_muted not in [0, 3] and perms != 'dev':
        return ('permission', user_muted)

    if bool(re.search(r'[<>]', message)) is True:
        cmds.warn_user(user)
        return ('permission', 10, user_muted)
        

    if perms != "dev":
        message = filter_message(message)
        role = profanity.censor(user['role'])
    else:
        role = user['role']

    if user['profile'] == "":
        profile_picture = 'static/favicon.ico'
    else:
        profile_picture = user['profile']

    if "[" in message:
        find_pings(message, user['displayName'], profile_picture, roomid)

    # print (preuser)
    # messageM = markdown(message)
    final_str = compile_message(message, profile_picture, user, role, preuser,
                                message_count)
    # print (message_count, preuser)

    #check if locked or allowed to send
    if locked == 'true' and perms not in ["dev", "mod"]:
        return ("permission", 3, user_muted)

    if can_send == "everyone":
        return_str = ('msg', final_str, user_muted)
    elif can_send == 'mod':
        if perms == 'mod':
            return_str = ('msg', final_str, user_muted)
        else:
            return_str = ('permission', 5, user_muted)
    else:
        return_str = ('permission', 5, user_muted)

    #check for spam then update message count and prev user
    if message_count == 15 and preuser == user["username"] and perms != "dev":
        cmds.warn_user(user)
        return ('permission', 8, user_muted)

    if preuser != user["username"]:
        message_count = 0

    preuser = user["username"]
    message_count += 1

    if perms in ["dev", "mod"]:
        chat.add_message(final_str, roomid, 'true')
        emit("message_chat", (final_str, roomid),
             broadcast=True,
             namespace="/")
        if "$sudo" in message:
            find_cmds(message, user, roomid)
            # if 'system' in message:
            #     return_str = ('command', 1, final_str)
        return ('dev/mod', 0, user_muted)

    return return_str


def check_mute(user):
    """checks if the user is muted or banned."""
    permission = user["permission"].split(' ')
    if permission[0] == "muted":
        return 1
    elif user["permission"] == "banned":
        return 2
    elif permission[0] == "locked":
        return 3
    return 0


def check_lock(room):
    """For now, its just as simple as this, but when rooms come it will be more complicated."""
    return (room["locked"])


def check_allowed_sending(user, room):
    """this is a check to se if the database allowes you to send"""
    return (room["canSend"])


def check_perms(user):
    """checks if the user has specal perms else return as a user"""
    if user['SPermission'] == 'Debugpass':
        perms = 'dev'
    elif user['SPermission'] == 'modpass':
        perms = 'mod'
    else:
        perms = 'user'
    return perms


def to_hyperlink(text):
    """Taken from the js file, we don't need to have the client process it really."""
    mails = re.findall(r"mailto:([^\?]*)", text)
    links2 = re.findall(r"(^|[^\/])(www\.[\S]+(\b|$))", text)
    #print(f"{mails}\n\n\n{links2}")


def filter_message(message):
    """No one likes profanity, especially flagging systems."""
    return profanity.censor(message)


def find_pings(message, dispName, profile_picture, roomid):
    """Gotta catch 'em all! (checks for pings in the users message)"""
    pings = re.findall(r'(?<=\[).+?(?=\])', message)
    room = rooms.get_chat_room(roomid)
    for ping in pings:
        message = message.replace(f"[{ping}]", '')
        emit("ping", {
            "who": ping,
            "from": dispName,
            "pfp": profile_picture,
            "message": message,
            "name": room["roomName"],
            "roomid": room["roomid"]
        },
             namespace="/",
             broadcast=True)


def find_cmds(message, user, roomid):
    """$sudo commands, will push every cmd found to cmds.py along with the user, so we can check if they can do said command."""
    command_split = message.split("$sudo")
    command_split.pop(0)
    command_string = command_split[0]
    perms = check_perms(user)
    origin_room = None
    match = re.findall(r"\(|\)", command_string)

    if perms == 'dev' and roomid == 'jN7Ht3giH9EDBvpvnqRB' and match != []:
        match_msg = re.findall(r"\((.*?)\)", command_string)
        find_roomid = re.sub(r"\([^()]+\)", "", command_string).strip()
        room_check = rooms.check_roomids(find_roomid)
        if room_check is False:
            failed_message(('permission', 7), roomid, user)
            return
        if len(match) == 2:
            origin_room = roomid
            roomid = find_roomid
            command_split = [match_msg[0]]

    if origin_room is None: origin_room = roomid
    # this check is needed, because the finding of commands is after chat lock check in run_filter
    # leading to users being able to send comamnds, even when chat is locked
    # we should be the only ones that can do that (devs)
    # for cmd in command_split:
    date_str = datetime.now(timezone(#that removes the multi command feture hope it dont break
        timedelta(hours=-4))).strftime("[%a %H:%M] ")
    Lmessage = date_str + user['username'] + ":" + command_split
    log.log_commands(Lmessage)

    command = command_split.split()
    commands = {}

    for index, command in enumerate(command):
        var_name = "v%d" % index
        commands[var_name] = command
    if 'v0' in commands:
        cmds.find_command(commands=commands,
                          user=user,
                          roomid=roomid,
                          origin_room=origin_room)


def compile_message(message, profile_picture, user, role, preuser,
                    message_count):
    """Taken from old methold of making messages"""
    to_hyperlink(message)
    profile = f"<img class='pfp' src='{profile_picture}'></img>"
    user_string = f"<font color='{user['userColor']}'>{user['displayName']}</font>"
    message_string = f"<font color='{user['messageColor']}'>{message}</font>"
    role_string = do_dev_easter_egg(role, user)
    date_str = datetime.now(timezone(
        timedelta(hours=-4))).strftime("[%a %I:%M %p] ")

    # should we change it to a f string
    # if user["username"] == preuser:
    #     message = message_string
    # else:
    message = date_str + profile + " " + user_string + " (" + role_string + ")" + " - " + message_string
    return message


def do_dev_easter_egg(role, user):
    """Because we want RAINBOW changing role names."""
    role_color = user['roleColor']
    if role_color == "#00ff00":
        role_string = "<font class='Dev_colors-loop'>" + role + "</font>"
    elif role_color == "rainbow":
        role_string = "<font class='rainbow-text-loop'>" + role + "</font>"
    else:
        role_string = "<font color='" + role_color + "'>" + role + "</font>"
    return role_string


def failed_message(result, roomid, user):
    """Tell the client that your message could not be sent for whatever the reason was."""
    fail_strings = {
        (1):
        "[SYSTEM]: <font color='#ff7f00'>You can't send messages because you are muted.</font>",
        (2):
        "[SYSTEM]: <font color='#ff7f00'>You can't send messages because you have been banned.</font>",
        (3):
        "[SYSTEM]: <font color='#ff7f00'>You can't send messages because this chat room has been locked.</font>",
        (4):
        "[SYSTEM]: <font color='#ff7f00'>You can't send messages because you have been banned from this chat room.</font>",
        (5):
        "[SYSTEM]: <font color='#ff7f00'>You can't send messages because you do not have enough permission to use this chat room.</font>",
        (6):
        "[SYSTEM]: <font color='#ff7f00'>You can't send messages in this chat room because this chat room no longer exists,  select a chat room that does exist.</font>",
        (7):
        "[SYSTEM]: <font color='#ff7f00'>this chat room id does not exist.</font>",
        (8):
        "[SYSTEM]: <font color='#ff7f00'>You are not allowed to send more than 15 messages in a row. (You have been warned)</font>",
        (9):
        "[SYSTEM]: <font color='#ff7f00'>You must verify your account before you can use commands.</font>",
        (10):
        "[SYSTEM]: <font color='#ff7f00'>You are not allowed to send code in the chat. (You have been warned)</font>"
    }
    if result[0] == "dev":
        if result[1] == 6: fail_str = fail_strings.get((result[1]), "")
        else: return
    # if result[0] == "return": emit("message_chat", ('', roomid), namespace="/") what is this

    fail_str = fail_strings.get((result[1]), "")  # result[2]), "")
    emit("message_chat", (fail_str, roomid), namespace="/")


def is_user_expired(permission_str):
    """checks if the user's time maches the time (idk you explain it better to me please)"""
    parts = permission_str.split(' ')
    if len(parts) == 3 and parts[0] == 'muted':
        expiration_time_str = ' '.join(parts[1:])
        expiration_time = datetime.strptime(expiration_time_str,
                                            "%Y-%m-%d %H:%M:%S")
        current_time = datetime.now()
        return current_time >= expiration_time


def is_warned_expired(warned_str):
    """checks if the user's time maches the time (idk you explain it better to me please)"""
    parts = warned_str.split(' ')
    if len(parts) == 2:
        expiration_time_str = ''.join(parts[1:])
        expiration_time = datetime.strptime(expiration_time_str,
                                            "%Y-%m-%d %H:%M:%S")
        current_time = datetime.now()
        return current_time >= expiration_time
