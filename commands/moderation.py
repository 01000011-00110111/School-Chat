from datetime import datetime, timedelta
from flask_socketio import emit
from chat import Chat
# from cmds import  other.respond_command, other.check_if_dev, other.format_system_msg, other.check_if_mod
import database
from commands import other
from user import User, inactive_users


def globalock(**kwargs):
    """Locks all chatrooms, only used in emergencies."""
    # user = kwargs['user']
    roomid = kwargs['roomid']
    confirm = kwargs['commands']['v1']
    other.respond_command((0, 'priv'), roomid) if database.check_private(roomid) \
    else None

    if confirm != "yes":
        other.respond_command((0, "not_confirmed"), roomid)
    else:
        message = other.format_system_msg("All Chatrooms locked by Admin.")
        Chat.add_message_to_all(message, "all", None)
        Chat.set_all_lock_status(True)
        emit("message_chat", (message, "all"), broadcast=True)


def lock(**kwargs):
    """locks the chat so that only devs can send"""
    user = kwargs['user']
    roomid = kwargs['roomid']
    room = kwargs['room']
    other.respond_command((0, 'priv'), roomid) if database.check_private(roomid) \
    else None
    if other.check_if_dev(user) == 1:
        message = other.format_system_msg("Chat Locked by Admin.")
        room.add_message(message, None)
        room.set_lock_status(True)
        emit("message_chat", (message, roomid), broadcast=True)
    elif other.check_if_mod(user) == 1:
        message = other.format_system_msg("Chat Locked by Moderator.")
        room.add_message(message, None)
        room.set_lock_status(True)
        emit("message_chat", (message, roomid), broadcast=True)


def unlock(**kwargs):
    """unlocks the chat so that everyone can send"""
    user = kwargs['user']
    roomid = kwargs['roomid']
    room = kwargs['room']
    other.respond_command((0, 'priv'), roomid) if database.check_private(roomid) \
    else None
    if other.check_if_dev(user) == 1:
        message = other.format_system_msg("Chat Unlocked by Admin.")
        room.add_message(message, None)
        room.set_lock_status(False)
        emit("message_chat", (message, roomid), broadcast=True)
    elif other.check_if_mod(user) == 1:
        message = other.format_system_msg("Chat Unlocked by Moderator.")
        room.add_message(message, None)
        room.set_lock_status(False)
        emit("message_chat", (message, roomid), broadcast=True)

def mute(**kwargs):
    """mutes the user"""
    # user = kwargs['user']
    roomid = kwargs['roomid']
    room = kwargs['room']
    target = kwargs["commands"]["v1"]#' '.join(list(kwargs["commands"].values())[1:])
    time = kwargs["commands"]["v2"] if kwargs["commands"]["v2"] else "5m"
    for users in User.Users:
        if users.displayName == target:
            user = users
    duration = int(time[:-1])
    if time[-1] == 'm':
        expiration_time = datetime.now() + timedelta(minutes=duration)
    elif time[-1] == 'h':
        expiration_time = datetime.now() + timedelta(hours=duration)
    elif time[-1] == 'd':
        expiration_time = datetime.now() + timedelta(days=duration)
    muted = {str(roomid): expiration_time}
    if user not in inactive_users[2]:  # add check later
        user.mutes.append(muted)
    else:
        database.mute_user(inactive_users[user][1], muted)
    message = other.format_system_msg("User Muted by Admin.")
    room.add_message(message, None)
    emit("message_chat", (message, roomid), broadcast=True)


def ban(**kwargs):
    """mutes the user in all chat rooms"""
    # user = kwargs['user']
    roomid = kwargs['roomid']
    room = kwargs['room']
    target = kwargs["commands"]["v1"]#' '.join(list(kwargs["commands"].values())[1:])
    time = kwargs["commands"]["v2"] if kwargs["commands"]["v2"] else "5m"
    duration = int(time[:-1])
    if time[-1] == 'm':
        expiration_time = datetime.now() + timedelta(minutes=duration)
    elif time[-1] == 'h':
        expiration_time = datetime.now() + timedelta(hours=duration)
    elif time[-1] == 'd':
        expiration_time = datetime.now() + timedelta(days=duration)
    for users in User.Users:
        if users.displayName == target:
            user = users
    # if True:  # add check later
    muted = {'all': expiration_time}
    if user not in inactive_users[2]:  # add check later
        user.mutes.append(muted)
    else:
        database.mute_user(inactive_users[user][1], muted)
    message = other.format_system_msg("User Banned by Admin.")
    room.add_message(message, None)
    emit("message_chat", (message, roomid), broadcast=True)

def unmute(**kwargs):
    """unmutes the user"""
    # user = kwargs['user']
    roomid = kwargs['roomid']
    room = kwargs['room']
    target = kwargs["commands"]["v1"]#' '.join(list(kwargs["commands"].values())[1:])
    # time = kwargs["commands"]["v2"]
    for users in User.Users:
        if users.displayName == target:
            user = users
    user.mutes = [mute for mute in user.mutes if str(roomid) not in mute.keys()]
    message = other.format_system_msg("User Unmuted by Admin.")
    room.add_message(message, None)
    emit("message_chat", (message, roomid), broadcast=True)


        
def add_word_to_unban_list(**kwargs):
     word = kwargs["commands"]["v1"]
     room = kwargs['room']
     roomid = kwargs['roomid']
     with open('unbanned_words.txt', 'a') as file:
         file.write(word + '\n')
     message = other.format_system_msg(f"New unbanned word: {word} was added by an Admin.")
     room.add_message(message, None)
     emit("message_chat", (message, roomid), broadcast=True)

def remove_word_from_unban_list(**kwargs):
    word = kwargs["commands"]["v1"]
    room = kwargs['room']
    roomid = kwargs['roomid']
    try:
        with open("unbanned_words.txt", "r") as file:
            lines = file.readlines()
        with open("unbanned_words.txt", "w") as file:
            for line in lines:
                if line.strip("\n") != word:
                    file.write(line)
        message = other.format_system_msg(f"An Admin banned the word: {word} was added by an Admin.")
        room.add_message(message, None)
        emit("message_chat", (message, roomid), broadcast=True)
    except FileNotFoundError:
        pass
