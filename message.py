from socketio_confg import sio

@sio.on("connect")
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    await sio.emit("server_message", {"message": "Welcome!"})

@sio.on("client_message")
async def client_message(sid, data):
    """
    This function is called when a client sends a message to the server.
    """
    print(f"Message from client {sid}: {data}")
    await sio.emit("server_message", {"message": "Echo: " + data["message"]})
