// Copyright (C) 2023  cserver45, cseven
// License info can be viewed in main.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat

socket.on("login_att", (state) => {
    if (state === 'true') {
        socket.emit('get_prefs', document.getElementById("user")["value"]);
    }
});

socket.on("return_prefs", (Obj) => {
    if ('failed' in Obj) {
        console.log('We need a failed to grab function')
    }
    window.localStorage.setItem("username", Obj["displayName"]);
    window.localStorage.setItem("pfp", Obj["profile"]);
    socket.emit("username_msg", Obj["displayName"]);
    whichEvent(Obj["theme"]);
    let pfp = document.getElementById("pfpmenu");
    let picture = window.localStorage.getItem("pfp");
    if (picture === '') {
        pfp.src = 'static/favicon.ico';
    } else {
        pfp.src = picture;
    }
});
