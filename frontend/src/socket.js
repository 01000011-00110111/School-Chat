// Copyright (C) 2023, 2024  cserver45, cseven
// License info can be viewed in app.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat
import { io } from "socket.io-client";

const socket = io("http://127.0.0.1:8000", {
    withCredentials: true
});

export default socket;