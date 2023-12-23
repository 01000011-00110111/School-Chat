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


socket.on("force_username", (_statement, ignore_user) => {
    if (getCookie('Userid') != ignore_user){
        socket.emit("username", getCookie("Username"), 'chat');
    } else {socket.emit("username", 'pass', 'chat');}
});

socket.on("force_room_update", (_statement) => {
    userid = getCookie("Userid")
    socket.emit("get_rooms", userid);
});

socket.on("ping", ({ who, from, pfp, message, name, roomid}) => {
    let user_name = getCookie("Username");
    // room = window.sessionStorage.getItem("roomid");
    console.log(who, from, message);
    if (user_name === who) {
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
    window.sessionStorage.setItem("roomid", 'ilQvQwgOhm9kNAOrRqbr');
    username = getCookie("Username");
    userid = getCookie("Userid")
    socket.emit("username", username, 'chat');
    socket.emit("get_rooms", userid);
    setTheme(getCookie('Theme'))
    // changeRoom('ilQvQwgOhm9kNAOrRqbr')
}

socket.on("roomsList", (result, permission) => {
    let newline = "<br>"
    let rooms = "";
    let RoomDiv = document.getElementById("ChatRoomls");
    for (room of result) {
        if (permission != 'locked') {
        rooms = rooms + `<hr id="room_bar"><a id="room_names" onclick=changeRoom("${room.id}")>/` + room.name + '</a><hr id="room_bar">';
        } else {
            rooms = '<hr id="room_bar">verify to have access to chat rooms<hr id="room_bar">'
            changeRoom('zxMhhAPfWOxuZylxwkES')
          }
    }
    RoomDiv["innerHTML"] = rooms;
    for (room of result) {CheckIfExist(result);}
});

function CheckIfExist(_params) {
    if (window.sessionStorage.getItem("roomid") != room.id) {
        changeRoom('ilQvQwgOhm9kNAOrRqbr')
    } else {return}
}

socket.on("room_data", (data) => {
    window.sessionStorage.setItem("roomid", data['roomid']);
    let newline = "<br>";
    let chatDiv = document.getElementById("chat");
    // update the url when the room is changed.
    window.history.replaceState({"pageTitle": `${data['name']} - Chat`}, "", `/chat/${data['roomName']}`);
    document.title = `/${data['roomName']} - Chat`
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

function BTMLog() {
  if (Math.floor(window.scrollY) === window.scrollMaxY) {
    console.log("cheese");
    setTimeout(ToBtm, 10000)
  } 
}

function ToBtm() {
  window.scrollTo(0, chatDiv.scrollHeight);
}

function sendMessage() {
    let messageElement = document.getElementById("message");
    let user = getCookie('Username')
    let userid = getCookie('Userid')
    let message = messageElement["value"];
    if (message === "") {
        return;
    }

    let chatDiv = document.getElementById("chat");
    messageL = toHyperlink(message);
    messageElement["value"] = "";
    // this is needed, because this goes over socketio, not a normal http request
    socket.emit('message_chat', user, messageL, window.sessionStorage.getItem("roomid"), userid);
    window.scrollTo(0, chatDiv.scrollHeight);
}


setInterval(BTMLog, 3000)

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