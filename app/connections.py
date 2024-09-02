import time
from threading import Timer
from flask import request

from app import socketio, database
from app.private import Private
from app.chat import Chat
from app.user import User
from app.online import socketids, update_userlist, user_connections, user_last_heartbeat, HEARTBEAT_TIMEOUT, check_user_heartbeat

@socketio.on("connect")
def emit_on_startup():
    """Handle a new connection."""
    socketid = request.sid
    userid = request.cookies.get("Userid")

    if userid is not None:
        if userid not in user_connections:
            user_connections[userid] = set()
        user_connections[userid].add(socketid)
        user_last_heartbeat[userid] = time.time()

        socketids[userid] = socketid
        update_userlist(socketid, {"status": "active"}, userid)

        Timer(HEARTBEAT_TIMEOUT + 5, check_user_heartbeat,
              args=[userid, handle_disconnect]).start()


@socketio.on("disconnect")
def handle_disconnect(socketid=None, userid=None):
    """Handle user disconnection."""
    if not socketid:
        socketid = request.sid
    if not userid:
        userid = request.cookies.get("Userid")

    if userid is None:
        return

    if userid in user_connections:
        user_connections[userid].discard(socketid)
        if not user_connections[userid]:
            del user_connections[userid]

    active_privates = [
        private
        for private in Private.chats.values()
        if userid in private.userlist and private.active.get(userid, False)
        or socketid in private.sids
    ]

    for private in active_privates:
        if userid in private.active:
            private.active[userid] = False
        if socketid in private.sids:
            private.sids.remove(socketid)

    active_chats = [chat for chat in Chat.chats.values() if socketid in chat.sids]

    for chat in active_chats:
        chat.sids.remove(socketid)

    if not user_connections.get(userid):
        try:
            user = User.get_user_by_id(userid)
            if user and user.status != "offline-locked":
                user.status = "offline"
            database.set_offline(userid)
            update_userlist(socketid, {"status": "offline"}, userid)
        except TypeError as e:
            print(f"Error setting user offline: {e}")


@socketio.on("heartbeat")
def handle_heartbeat(status, roomid):
    """Handle heartbeat from the client."""
    socketid = request.sid
    userid = request.cookies.get("Userid")

    if userid is not None:
        user_last_heartbeat[userid] = time.time()

        if userid in user_connections:
            update_userlist(socketid, {"status": status}, userid)
            room = Chat.create_or_get_chat(roomid)
            if socketid not in room.sids:
                socketids[userid] = socketid
                room.sids.append(socketid)
