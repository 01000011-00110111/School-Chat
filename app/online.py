"""online.py: Handles the userlist of the chat
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
import time
from flask import current_app, request
from flask_socketio import emit

from app import socketio
from app import database
from app.user import User
# from app.chat import Chat

socketids = {}
users_list = {}
user_connections = {}
user_last_heartbeat = {}

HEARTBEAT_TIMEOUT = 40

@socketio.on("status_change")
def handle_connect(data):
    """Will be used later for online users."""
    socketid = request.sid
    update_userlist(socketid, data, request.cookies.get("Userid"))


@socketio.on("get_full_list")
def handle_full_list_request():
    """updates the full list of users in the online list"""
    socketid = request.sid
    emit("update_list_full", (list(users_list.values())), namespace="/", to=socketid)


def get_scoketid(uuid):
    """Gets the user's socketid."""
    return socketids[uuid]


def update_userlist(_, data, uuid):
    """Updates a user in the users list."""
    for key, value in data.items():
        if key == 'status' and users_list[uuid]['status'] == 'offline-locked':
            continue
        users_list[uuid][key] = value

    emit("update_list", users_list[uuid], namespace="/", broadcast=True)
    # later ill improve the code to be able to send to only one user and not just everyone online
    return users_list[uuid]


def update_display(data, uuid):
    """Updates a user in the users list."""
    # user_old = users_list[uuid]
    for key, value in data.items():
        if key == 'status' and users_list[uuid]['status'] == 'offline-locked':
            continue
        users_list[uuid][key] = value

    # emit("updated_display", (users_list[uuid], user_old), namespace="/", broadcast=True)
    emit("update_list_full", (list(users_list.values())), namespace="/", broadcast=True)
    return users_list[uuid]


def add_unread(recipient, sender):
    """Updates the unread list of a user."""
    display_name = users_list[recipient]["username"]
    users_list.setdefault(sender, {"unread": {}}).setdefault("unread", {}).setdefault(
        display_name, 0
    )
    users_list[sender]["unread"][display_name] += 1
    if "offline" not in users_list[recipient]["status"]:
        emit("update_list", users_list[sender], namespace="/", to=socketids[recipient])


def clear_unread(recipient, sender):
    """Resets a user's unread count."""
    display_name = users_list[sender]["username"]
    users_list.setdefault(recipient, {"unread": {}}).setdefault(
        "unread", {}
    ).setdefault(display_name, 0)
    users_list[recipient]["unread"][display_name] = 0
    if "offline" not in users_list[sender]["status"]:
        emit("update_list", users_list[recipient], namespace="/", to=socketids[sender])


def check_user_heartbeat(userid, disconnect_callback):
    """Check if the user's heartbeat is overdue and disconnect if necessary."""
    if userid in user_last_heartbeat:
        last_heartbeat = user_last_heartbeat[userid]
        if time.time() - last_heartbeat > HEARTBEAT_TIMEOUT:
            handle_forced_disconnect(userid, disconnect_callback)


def handle_forced_disconnect(userid, disconnect_callback):
    """Mark the user as offline if no heartbeat is received in time."""
    if userid in user_connections:
        for socketid in list(user_connections[userid]):
            disconnect_callback(socketid, userid)
        del user_connections[userid]

    try:
        with current_app.app_context():
            try:
                u = User.get_user_by_id(userid)
                if u and u.status != "offline-locked":
                    u.status = "offline"
                database.set_offline(userid)
                update_userlist(None, {"status": "offline"}, userid)
            except TypeError as e:
                print(f"Error in forced disconnect: {e}")
    except RuntimeError as e:
        print(f"Runtime error in forced disconnect: {e}")




def get_all_offline():
    """gets all offline users"""
    offline = []
    for _, values in users_list.items():
        if 'offline' in values["status"]:
            offline.append(values["username"])
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