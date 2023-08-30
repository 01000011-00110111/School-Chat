// Copyright (C) 2023  cserver45, cseven
// License info can be viewed in main.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat

socket.on("message_chat", (message, roomid) => {
    renderChat((message), roomid);
});

socket.on("troll", (message, roomid) => {
    renderChat(message, roomid);
    var audio = new Audio('static/airhorn_default.wav');
    audio.play();
});

socket.on("pingTime", (time, roomid) => {
    socket.emit('pingtest', time, roomid);
});


socket.on("force_username", (statement) => {
    socket.emit("username", window.localStorage.getItem("username"), 'chat');
});

socket.on("ping", ({ who, from, pfp, message, name, roomid}) => {
    let user_name = window.localStorage.getItem("username");
    room = window.sessionStorage.getItem("roomid");
    console.log(who, from, message);
    if (user_name === who && roomid === room) {
        new Notification("You where pinged by:", { body: from + ` in ${name}: ` + message, icon: '/static/favicon.ico'});
    } else if (who === "everyone") {// add a check to see if the user has access and if so then ping them    
        new Notification("You where pinged by:", { body: from + ` in ${name}: ` + message, icon: '/static/favicon.ico'});
    }
});

socket.on("reset_chat", (who, roomid) => {
    if (roomid === window.sessionStorage.getItem('roomid')) {
        let chatDiv = document.getElementById("chat");
        if (who === "admin") {
            chatDiv.innerHTML = "[SYSTEM]: <font color='#ff7f00'>Chat reset by an admin.</font><br>";
        } else if (who === 'owner/mod') {
            chatDiv.innerHTML = "[SYSTEM]: <font color='#ff7f00'>Chat reset by this chat rooms Owner or Mod.</font><br>"
        } else if (who === "auto") {
            chatDiv.innerHTML = "[SYSTEM]: <font color='#ff7f00'>Chat reset by automatic wipe system.</font><br>";
        }
    }
});

function runStartup() {
    setDarkStyle();
    window.sessionStorage.setItem("roomid", 'ilQvQwgOhm9kNAOrRqbr');
    socket.emit('get_prefs', document.getElementById("user")["value"]);
    socket.emit('get_perms');
    username = window.localStorage.getItem("username");
    let user = document.getElementById("user")["value"];
    socket.emit("username", username, 'chat');
    socket.emit("get_rooms", user);
    changeRoom('ilQvQwgOhm9kNAOrRqbr')
}

socket.on("roomsList", (result) => {
    for (room of result) {CheckIfExist(result);}
    let newline = "<br>"
    let rooms = "";
    let RoomDiv = document.getElementById("ChatRoomls");
    for (room of result) {
        rooms = rooms + "<a onclick=changeRoom('" + room.id + "')>/" + room.name + '</a>';
    }
    RoomDiv["innerHTML"] = rooms;
});

function CheckIfExist(params) {
    if (window.sessionStorage.getItem("roomid") != room.id) {
        changeRoom('ilQvQwgOhm9kNAOrRqbr')
    } else {return}
}

socket.on("room_data", (data) => {
    window.sessionStorage.setItem("roomid", data['roomid']);
    let newline = "<br>";
    let chatDiv = document.getElementById("chat");
    // why oh why does chrome say no to this.
    //window.history.pushState({"pageTitle": `${data['name']} - Chat`},"", `dev.school-chat.us/chat${data['name']}`);
    let chat = ""; 
    for (let messageObj of data['messages']) {
        chat = chat + messageObj + newline;
    }

    chatDiv["innerHTML"] = chat;
    window.scrollTo(0, chatDiv.scrollHeight);
});

function changeRoom(room) {
    window.sessionStorage.setItem("roomid", room);
    socket.emit('room_connect', room)
}

function toHyperlink(str) {
    var pattern1 = /(\b(https?|ftp|sftp|file|http):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig;
    var str1 = str.replace(pattern1, "<a href='$1'>$1</a>");
    var pattern2 = /(^|[^\/])(www\.[\S]+(\b|$))/gim;
    var str2 = str1.replace(pattern2, '$1<a target="_blank" href="http://$2">$2</a>');
    var pattern3 = /mailto:([^\?]*)/gm;
    var str3 = str2.replace(pattern3, "<a href='mailto:$1'>$1</a>");

    return str3;
}

function sendMessage() {
    let messageElement = document.getElementById("message");
    let user = document.getElementById("user")["value"]
    let message = messageElement["value"];
    if (message === "") {
        return;
    }

    let chatDiv = document.getElementById("chat");
    messageL = toHyperlink(message);
    messageElement["value"] = "";
    socket.emit('message_chat', user, messageL, window.sessionStorage.getItem("roomid"));
    window.scrollTo(0, chatDiv.scrollHeight);
}

function renderChat(messages, roomid) {
    let newline = "<br>";
    let chatDiv = document.getElementById("chat");
    if (roomid === window.sessionStorage.getItem('roomid') || roomid === "all") {
        chatDiv["innerHTML"] = chatDiv["innerHTML"] + messages + newline;
    }
}


function checkKey() {
    if (event.key === "Enter") {
        sendMessage();
    }
}