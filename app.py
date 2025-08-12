"""app.py: Main webserver file for school-chat, a chat server
    Copyright (C) 2023, 2024  cserver45, cseven

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
from sanic import Sanic
from sanic_cors import CORS
# import socketio
import socketio_confg
# ruff-ignore: F401
from chat import message, rooms, chat # noqa: F401 F811
from user import login, signup, settings # noqa: F401
from online import online # noqa: F401
from private import private, rooms, message # noqa: F401 F811
sio = socketio_confg.sio

app = Sanic("School-Chats")
CORS(app, resources={r"/*": {"origins": "*"}}, automatic_options=True)
@app.before_server_start
async def start_tasks(app, loop):
    sio.start_background_task(online.heartbeat_loop)
sio.attach(app)

@app.before_server_stop
async def final_backup(app, _):
    """Final backup before server stop."""
    for roomid in chat.Chat.chats:
        await chat.Chat.get_chat(roomid).backup(True)
    print("Final backup completed.")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
