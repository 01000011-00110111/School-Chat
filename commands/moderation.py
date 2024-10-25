"""moderation.py: All moderation commands for the chat
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
from datetime import datetime, timedelta
from better_profanity import profanity
from flask_socketio import emit

import database
from chat import Chat
from commands import other
from online import get_scoketid
from user import User
from word_lists import blacklist_words
from word_lists import whitelist_words as wl

REPORTS = []


def globalock(**kwargs):
    """Locks all chatrooms, only used in emergencies."""
    # user = kwargs['user']
    roomid = kwargs['roomid']
    confirm = kwargs['commands']['v1']
    if database.check_private(roomid):
        other.respond_command((0, 'priv'), roomid)

    if confirm != "yes":
        other.respond_command((0, "not_confirmed"), roomid)
    else:
        message = other.format_system_msg("All Chatrooms locked by Admin.")
        Chat.add_message_to_all(message, "all", None)
        Chat.set_all_lock_status(True)


def lock(**kwargs):
    """locks the chat so that only devs can send"""
    user = kwargs['user']
    roomid = kwargs['roomid']
    room = kwargs['room']
    if database.check_private(roomid):
        other.respond_command((0, 'priv'), roomid)
    if other.check_if_dev(user) == 1:
        message = other.format_system_msg("Chat Locked by Admin.")
        room.add_message(message, user)
        room.set_lock_status(True)
    elif other.check_if_mod(user) == 1:
        message = other.format_system_msg("Chat Locked by Moderator.")
        room.add_message(message, user)
        room.set_lock_status(True)
    emit('chat_muted')


def unlock(**kwargs):
    """unlocks the chat so that everyone can send"""
    user = kwargs['user']
    roomid = kwargs['roomid']
    room = kwargs['room']
    if database.check_private(roomid):
        other.respond_command((0, 'priv'), roomid)
    if other.check_if_dev(user) == 1:
        message = other.format_system_msg("Chat Unlocked by Admin.")
        room.add_message(message, user)
        room.set_lock_status(False)
    elif other.check_if_mod(user) == 1:
        message = other.format_system_msg("Chat Unlocked by Moderator.")
        room.add_message(message, user)
        room.set_lock_status(False)
    emit('chat_unmuted')


def mute(**kwargs):
    """mutes the user"""
    sender = kwargs['user']
    room = kwargs['room']
    target = kwargs["commands"]["v1"]
    time = kwargs["commands"]["v2"] if kwargs["commands"]["v2"] else "5m"
    duration = int(time[:-1])
    expiration = datetime.now() + timedelta(**{time[-1] + 's': duration})
    user, delete = other.get_user(target)
    if user is None:
        room.send_message(f"{target} does not exist.")
        return
    if delete:
        User.delete_user(user.uuid)
    room.mutes.append({str(user.uuid): expiration})
    message = other.format_system_msg(f"{user.display_name}\
            was muted by {sender.display_name}.")
    room.add_message(message, user)


def unmute(**kwargs):
    """unmutes the user"""
    room = kwargs['room']
    target = kwargs["commands"]["v1"]
    user, delete = other.get_user(target)
    if user is None:
        room.send_message(f"{target} does not exist.")
        return
    room.mutes = [mute for mute in room.mutes if mute != {str(user.uuid): None}]
    if delete:
        User.delete_user(user.uuid)
    message = other.format_system_msg(f"{target} was unmuted by {kwargs['user'].display_name}.")
    room.add_message(message, user)


# def ban(**kwargs):
#     """mutes the user in all chat rooms"""
#     sender = kwargs['user']
#     target = kwargs["commands"]["v1"]
#     time = kwargs["commands"]["v2"]
#     user, delete = other.get_user(target)
#     if user is None:
#         kwargs['room'].send_message(f"{target} does not exist.")
#         return
#     expiration = None
#     if time:
#         duration = int(time[:-1])
#         expiration = datetime.now() + getattr(timedelta, time[-1])(duration)
#     for room in Chat.chats.values():
#         room.mutes.append({str(user.uuid): expiration})
#     if delete:
#         User.delete_user(user.uuid)
#     message = other.format_system_msg(
#     f"{target} was {'banned' if expiration else 'globally muted'} by {sender.display_name}."
#     )
#     kwargs['room'].add_message(message, False)


# def unban(**kwargs):
#     """unmutes the user"""
#     sender = kwargs['user']
#     target = kwargs["commands"]["v1"]
#     user, delete = other.get_user(target)
#     if User is None:
#         kwargs['room'].send_message(f"{target} does not exist.")
#         return
#     for room in Chat.chats.values():
#         del room.mutes[user.uuid]
#     if delete:
#         User.delete_user(User.uuid)

#     message = other.format_system_msg(f"{target} was unmuted by {sender.display_name}.")
#     kwargs['room'].add_message(message, False)


def add_word_to_unban_list(**kwargs):
    """Adds a word to the list of unbanned words."""
    word = kwargs["commands"]["v1"]
    room = kwargs['room']
    user = kwargs['user']
    if word not in wl:
        with open('backend/unbanned_words.txt', 'a', encoding="utf-8") as file:
            file.write(word + '\n')
        wl.append(word)
        if word in blacklist_words:
            blacklist_words.remove(word)
        message = other.format_system_msg(
            f"New unbanned word: {word} was added by an Admin.")
        room.add_message(message, user)
        profanity.load_censor_words(whitelist_words=wl)
        profanity.add_censor_words(blacklist_words)


def remove_word_from_unban_list(**kwargs):
    """Adds a word to the list of banned words."""
    word = kwargs["commands"]["v1"]
    room = kwargs['room']
    user = kwargs['user']

    if word in wl:
        wl.remove(word)
        try:
            with open("backend/unbanned_words.txt", "r", encoding="utf-8") as file:
                lines = [line.strip("\n") for line in file if line.strip("\n") != word]
            with open("backend/unbanned_words.txt", "w", encoding="utf-8") as file:
                file.write("\n".join(lines))
            with open("backend/banned_words.txt", "a", encoding="utf-8") as banned_file:
                banned_file.write(word + "\n")
            blacklist_words.append(word)

            message = other.format_system_msg(
                f"An Admin banned the word: {word}")
            room.add_message(message, user)
            profanity.load_censor_words(whitelist_words=wl)
            profanity.add_censor_words(blacklist_words)
        except FileNotFoundError:
            pass


def report_user(**kwargs):
    """Reports a user."""
    roomid = kwargs['roomid']
    user = kwargs['user']
    reported_user = kwargs["commands"]["v1"]
    reason = ' '.join(list(kwargs["commands"].values())[2:])
    REPORTS.append([reported_user, reason])
    emit("message_chat",
         (other.format_system_msg(f"You reported {reported_user} with the reason, {reason}"),
          roomid),
        to=get_scoketid(user.uuid))
    # emit('system_pings', f"The user {reported_user} was reported for the reason: {reason}",)


def list_reports(**kwargs):
    """List all reported users."""
    room = kwargs['room']
    user = kwargs['user']
    reports_list = "<br>".join(
        [f'{report[0]} was reported with the reason, {report[1]}' for report in REPORTS])
    room.add_message(other.format_system_msg(('<br>'+reports_list)), user)
