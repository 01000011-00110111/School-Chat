from flask import request
from flask_socketio import emit
from app import socketio

import app.database as database

socketids = {}
users_list = {}


@socketio.on("status_change")
def handle_connect(data):
    """Will be used later for online users."""
    socketid = request.sid
    # user = User.get_user_by_id(request.cookies.get('Userid'))
    update_userlist(socketid, data, request.cookies.get("Userid"))
    # if user is not None:
    #     user.unique_online_list(userid, isVisible, location, sid)


@socketio.on("get_full_list")
def handle_full_list_request():
    socketid = request.sid
    emit("update_list_full", (list(users_list.values())), namespace="/", to=socketid)


@socketio.on("connect")
def emit_on_startup():
    socketid = request.sid
    uuid = request.cookies.get("Userid")
    if uuid in socketids:
        socketids[uuid] = socketid
    if uuid is not None:
        update_userlist(socketid, {"status": "active"}, uuid)


@socketio.on("disconnect")
def handle_disconnect():
    """Remove the user from the online user db on disconnect."""
    socketid = request.sid
    userid = request.cookies.get("Userid")

    active_privates = [
        private
        for private in Private.chats.values()
        if (userid in private.userlist and private.active.get(userid, False))
        or socketid in private.sids
    ]

    for private in active_privates:
        private.active[userid] = False
        if socketid in private.sids:
            private.sids.remove(socketid)

    active_chats = [chat for chat in Chat.chats.values() if socketid in chat.sids]

    for chat in active_chats:
        chat.sids.remove(socketid)

    try:
        user = User.get_user_by_id(userid)
        if user is not None and user.status != "offline-locked":
            user.status = "offline"
        database.set_offline(userid)
        # emit('update_list', (list(users_list.values())), brodcast=True)
        if userid is not None:
            update_userlist(socketid, {"status": "offline"}, userid)
        # del socketids[request.cookies.get("Userid")]
    except TypeError:
        pass


def get_scoketid(uuid):
    return  socketids[uuid]

def update_userlist(_, data, uuid):
    for key, value in data.items():
        users_list[uuid][key] = value
    # send_users_list = users_list[uuid]
    # send_users_list.pop('unread', None)

    emit('update_list', users_list[uuid], namespace='/', broadcast=True)
    #later ill advabce ui to be able to send to only one user
    return users_list[uuid]


def add_unread(recipient, sender):
    displayName = users_list[recipient]['username']
    users_list.setdefault(sender, {'unread': {}}).setdefault('unread', {}).setdefault(displayName, 0)
    users_list[sender]['unread'][displayName] += 1
    # print(users_list[recipient], '\n', recipient)
    if 'offline' not in users_list[recipient]['status']:
        emit('update_list', users_list[sender], namespace='/', to=socketids[recipient])


def clear_unread(recipient, sender):
    displayName = users_list[sender]['username']
    users_list.setdefault(recipient, {'unread': {}}).setdefault('unread', {}).setdefault(displayName, 0)
    users_list[recipient]['unread'][displayName] = 0
    # print(users_list[recipient], '\n', recipient)
    if 'offline' not in users_list[sender]['status']:
        emit('update_list', users_list[recipient], namespace='/', to=socketids[sender])


def get_all_offline():
    offline = []
    for user in users_list:
        if user['status'] in ['offline','offline-locked']:
            offline.append(user['username'])
    return offline

for user in database.get_all_offline():
    # print(user)
    perm = 'dev' if user['perm'][0] == 'Debugpass' else 'admin' if\
        user['perm'][0] == 'adminpass' else 'mod'\
            if user['perm'][0] == 'modpass' else None
    
    status = 'offline' if user['status'] != 'offlne-locked' else 'offline-locked'
            
    users_list[user['userid']] = {'username': user['displayName'],
                                  'status': status, 'perm': perm, 'unread': {}}