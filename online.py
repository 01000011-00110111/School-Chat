"""Handles the userlist of the chat."""
from flask_socketio import emit

import database

socketids = {}
users_list = {}


def get_scoketid(uuid):
    """Gets the user's socketid."""
    return socketids[uuid]


def update_userlist(_, data, uuid):
    """Updates a user in the users list."""
    for key, value in data.items():
        users_list[uuid][key] = value

    emit("update_list", users_list[uuid], namespace="/", broadcast=True)
    # later ill advance the code to be able to send to only one user and not just everyone online
    return users_list[uuid]


def add_unread(recipient, sender):
    """Updates the unread list of a user."""
    display_name = users_list[recipient]["username"]
    users_list.setdefault(sender, {"unread": {}}).setdefault("unread", {}).setdefault(
        display_name, 0
    )
    users_list[sender]["unread"][display_name] += 1
    # print(users_list[recipient], '\n', recipient)
    if "offline" not in users_list[recipient]["status"]:
        emit("update_list", users_list[sender], namespace="/", to=socketids[recipient])


def clear_unread(recipient, sender):
    "Resets a user's unread count."
    display_name = users_list[sender]["username"]
    users_list.setdefault(recipient, {"unread": {}}).setdefault(
        "unread", {}
    ).setdefault(display_name, 0)
    users_list[recipient]["unread"][display_name] = 0
    # print(users_list[recipient], '\n', recipient)
    if "offline" not in users_list[sender]["status"]:
        emit("update_list", users_list[recipient], namespace="/", to=socketids[sender])


def get_all_offline():
    """gets all offline users"""
    offline = []
    for u in users_list:
        if u["status"] in ["offline", "offline-locked"]:
            offline.append(u["username"])
    return offline


for user in database.get_all_offline():
    perm = (
        "dev"
        if user["perm"][0] == "Debugpass"
        else "admin"
        if user["perm"][0] == "adminpass"
        else "mod"
        if user["perm"][0] == "modpass"
        else None
    )

    STATUS = "offline" if user["status"] != "offlne-locked" else "offline-locked"

    users_list[user["userid"]] = {
        "username": user["displayName"],
        "status": STATUS,
        "perm": perm,
        "unread": {},
    }
