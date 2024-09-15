// Copyright (C) 2023, 2024  cserver45, cseven
// License info can be viewed in main.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat

// define socketio connection
const socket = io();

// it returns from the dead!
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

socket.on("ping", ({from}) => {
    new Notification(`${from} pinged you`, { icon: 'static/favicon.ico' });
});

socket.on("system_pings", (message) => {
    new Notification(message, { icon: 'static/favicon.ico' });
});

setInterval(() => {
    RID = window.sessionStorage.getItem("ID")
    private = window.sessionStorage.getItem("private")
    let status = ''
    if (document.hidden) {
        status = 'idle';
    } else {
        status = 'active';
    }
    socket.emit('heartbeat', status, RID, private);
}, 25000);