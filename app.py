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
from socketio_handler import sio
# import socketio

# Create a Sanic app and a Socket.IO server
app = Sanic("School-Chat")
sio.attach(app)
app.static('/', '../frontend')

# Example Socket.IO event
@sio.event
async def connect(sid):
    """
    This function is called when a client connects to the server.
    """
    print(f"Client connected: {sid}")
    await sio.emit("server_message", {"message": "Welcome!"})

@sio.event
async def client_message(sid, data):
    """
    This function is called when a client sends a message to the server.
    """
    print(f"Message from client {sid}: {data}")
    await sio.emit("server_message", {"message": "Echo: " + data["message"]})

@sio.event
async def disconnect(sid):
    """
    This function is called when a client disconnects from the server.
    """
    print(f"Client disconnected: {sid}")

# __all__ = ['app', 'sio']

# Start the server
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
