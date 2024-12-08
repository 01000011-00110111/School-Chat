"""socketio_handler.py: Filtering for usernames, and general formatting.
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in app.py or the LICENSE file.
"""
import socketio
# from app import sio

sio = socketio.AsyncServer(async_mode="sanic", allow_origins="*", cross_origin_allowed_origins="*", access_control_allow_Origin="*")

# @sio.event
# async def connect(sid):
#     """
#     This function is called when a client connects to the server.
#     """
#     print(f"Client connected: {sid}")
#     await sio.emit("server_message", {"message": "Welcome!"})

# @sio.event
# async def client_message(sid, data):
#     """
#     This function is called when a client sends a message to the server.
#     """
#     print(f"Message from client {sid}: {data}")
#     await sio.emit("server_message", {"message": "Echo: " + data["message"]})

# @sio.event
# async def disconnect(sid):
#     """
#     This function is called when a client disconnects from the server.
#     """
#     print(f"Client disconnected: {sid}")
