// Copyright (C) 2023  cserver45, cseven
// License info can be viewed in main.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat

socket.on("message_chat", (message) => {
    renderChat((message));
});

socket.on("troll", (message, ID) => {
    renderChat(message, ID);
    var audio = new Audio('static/airhorn_default.wav');
    audio.play();
});

socket.on("pingTime", (time, ID) => {
    socket.emit('pingtest', time, ID);
});

socket.on("force_room_update", (_statement) => {
    userid = getCookie("Userid")
    socket.emit("get_rooms", userid);
});

socket.on("reset_chat", (who, ID) => {
    if (ID === window.sessionStorage.getItem('ID')) {
        let chatDiv = document.getElementById("chat");
        if (who === "admin") {
            chatDiv.innerHTML = "[SYSTEM]: <font color='#ff7f00'>Chat reset by an admin.</font><br>";
        } else if (who === 'owner/mod') {
            chatDiv.innerHTML = "[SYSTEM]: <font color='#ff7f00'>Chat reset by this chat rooms Owner or Mod.</font><br>"
        } else if (who === "priv") {
            chatDiv.innerHTML = "[SYSTEM]: <font color='#ff7f00'>Chat reset by a private chat user.</font><br>";
        } else if (who === "auto") {
            chatDiv.innerHTML = "[SYSTEM]: <font color='#ff7f00'>Chat reset by automatic wipe system.</font><br>";
        }
    }
});

  

function runStartup() {
    window.sessionStorage.setItem("ID", 'ilQvQwgOhm9kNAOrRqbr');
    changeRoom('ilQvQwgOhm9kNAOrRqbr')
    userid = getCookie("Userid")
    document.getElementById("pfpmenu").src = getCookie("Profile");
    socket.emit("get_full_list");
    socket.emit("get_rooms", userid);
    setTheme(getCookie('Theme'))
}

socket.on("roomsList", (result, permission) => {
    let newline = "<br>"
    let rooms = "";
    let RoomDiv = document.getElementById("ChatRoomls");
    for (room of result) {
        if (permission != 'locked') {
        rooms = rooms + `<hr id="room_bar"><a id="room_names" onclick=changeRoom("${room.vid}")>/` + room.name + '</a><hr id="room_bar">';
        } else {
            rooms = '<hr id="room_bar">verify to have access to chat rooms<hr id="room_bar">'
            changeRoom('zxMhhAPfWOxuZylxwkES')
          }
    }
    RoomDiv["innerHTML"] = rooms;
    // for (room of result) {CheckIfExist(result);}
});

function CheckIfExist(_params) {
    if (window.sessionStorage.getItem("ID") != room.vid) {
        changeRoom('ilQvQwgOhm9kNAOrRqbr')
    } else {return}
}

socket.on("room_data", (data) => {
    // console.log(data)
    window.sessionStorage.setItem("ID", data['roomid']);
    window.sessionStorage.setItem("private", 'false')
    let newline = "<br>";
    let chatDiv = document.getElementById("chat");
    // update the url when the room is changed.
    let room_cat = window.location.href.split("/")[3];
    window.history.replaceState({"pageTitle": `${data['name']} - Chat`}, "", `/${room_cat}/${data['name']}`);
    roomname = document.getElementById("RoomDisplay").innerHTML = '/'+data['name'];
    document.title = `/${data['name']} - Chat`;
    let chat = ""; 
    for (let messageObj of data['msg']) {
        chat = chat + messageObj + newline;
    }

    chatDiv["innerHTML"] = chat;
    window.scrollTo(0, chatDiv.scrollHeight);
});

socket.on("private_data", (data) => {
    // console.log(data)
    window.sessionStorage.setItem("ID", data['pmid'])
    window.sessionStorage.setItem("private", 'true');
    let newline = "<br>";
    let chatDiv = document.getElementById("chat");
    // update the url when the room is changed.
    let room_cat = window.location.href.split("/")[3];
    window.history.replaceState({"pageTitle": `Private Chat`}, "", `/${room_cat}/Private/${data['name']}`);
    roomname = document.getElementById("RoomDisplay").innerHTML = `Private Chat: ${data['name']}`;
    document.title = `/Private - ${data['name']}`;
    let chat = ""; 
    for (let messageObj of data['message']) {
        chat = chat + messageObj + newline;
    }

    chatDiv["innerHTML"] = chat;
    window.scrollTo(0, chatDiv.scrollHeight);
});

function changeRoom(room) {
    window.sessionStorage.setItem("ID", room);
    closeNav();
    socket.emit('room_connect', room, getCookie("Userid"))
}


function openuserinfo(user) {
    socket.emit('private_connect', getCookie('Userid'), user, window.sessionStorage.getItem('ID'))
}

// function BTMLog() {
//   if (Math.floor(window.scrollY) === window.scrollMaxY) {
//     console.log("cheese");
//     setTimeout(ToBtm, 10000)
//   } 
// }

// function ToBtm() {
//   window.scrollTo(0, chatDiv.scrollHeight);
// }

function getMessage() {
    let messageElement = document.getElementById("message");
    let message = messageElement["value"];
    messageElement["value"] = "";
    let hidden = false
    var admin = document.getElementById('send_as_admin');
    if (admin) {
        if (admin.checked) {
            hidden = true;
            message = '$sudo admin ' + message;
        }
    }
    sendMessage(message, hidden);
}

function sendMessage(message, hidden) {
    let user = getCookie('Username')
    let userid = getCookie('Userid')
    if (message === "") {
        return;
    }
    // later i'll implement hiding the cmd
    let chatDiv = document.getElementById("chat");
    // this is needed, because this goes over socketio, not a normal http request
    private = window.sessionStorage.getItem('private')
    ID = window.sessionStorage.getItem("ID")
    socket.emit('message_chat', user, message, ID, userid, private, hidden);

    window.scrollTo(0, chatDiv.scrollHeight);
}


// setInterval(BTMLog, 3000)

function renderChat(messages) {
    // console.log(messages)
    let newline = "<br>";
    let chatDiv = document.getElementById("chat");
    chatDiv["innerHTML"] = chatDiv["innerHTML"] + messages + newline;
}


function checkKey() {
    if (event.key === "Enter") {
        getMessage();
    }
}