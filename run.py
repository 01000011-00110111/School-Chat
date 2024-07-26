from app import create_app, socketio

app = create_app()

if __name__ == "__main__":
    print("Copyright (C) 2023  cserver45, cseven")
    print("License info can be viewed in main.py or the LICENSE file.")
    socketio.run(app, host="0.0.0.0", port=5000)
