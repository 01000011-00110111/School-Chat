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
from chat import message
sio = socketio_confg.sio

app = Sanic("School-Chats")
CORS(app, resources={r"/*": {"origins": "*"}}, automatic_options=True)
sio.attach(app)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
