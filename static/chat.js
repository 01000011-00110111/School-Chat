// Copyright (C) 2023  cserver45, cseven
// License info can be viewed in main.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat

socket.on("message_chat", (message, ID) => {
    renderChat((message), ID);
});

socket.on("troll", (message, ID) => {
    renderChat(message, ID);
    var audio = new Audio('static/airhorn_default.wav');
    audio.play();
});

socket.on("pingTime", (time, ID) => {
    socket.emit('pingtest', time, ID);
});


socket.on("force_username", () => {
    socket.emit("username", getCookie("Userid"), 'chat');
});

socket.on("force_room_update", (_statement) => {
    userid = getCookie("Userid")
    socket.emit("get_rooms", userid);
});

socket.on("ping", ({ who, from, pfp, message, name, ID}) => {
    let user_name = getCookie("DisplayName");
    // room = window.sessionStorage.getItem("ID");
    // console.log(who, from, message);
    if (user_name === who) {
        new Notification("You where pinged by:", { body: from + ` in ${name}: ` + message, icon: '/static/favicon.ico'});
    } else if (who === "everyone") {// add a check to see if the user has access and if so then ping them    
        new Notification("You where pinged by:", { body: from + ` in ${name}: ` + message, icon: '/static/favicon.ico'});
    }
});

socket.on("reset_chat", (who, ID) => {
    if (ID === window.sessionStorage.getItem('ID')) {
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
    window.sessionStorage.setItem("ID", 'ilQvQwgOhm9kNAOrRqbr');
    changeRoom('ilQvQwgOhm9kNAOrRqbr')
    userid = getCookie("Userid")
    document.getElementById("pfpmenu").src = getCookie("Profile");
    socket.emit("username", userid, 'chat');
    socket.emit("get_rooms", userid);
    setTheme(getCookie('Theme'))
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
    if (window.sessionStorage.getItem("ID") != room.id) {
        changeRoom('ilQvQwgOhm9kNAOrRqbr')
    } else {return}
}

socket.on("room_data", (data) => {
    // console.log(data)
    window.sessionStorage.setItem("ID", data['ID']);
    window.sessionStorage.setItem("private", 'false')
    let newline = "<br>";
    let chatDiv = document.getElementById("chat");
    // update the url when the room is changed.
    window.history.replaceState({"pageTitle": `${data['name']} - Chat`}, "", `/chat/${data['name']}`);
    roomname = document.getElementById("RoomDisplay").innerHTML = '/'+data['name'];
    document.title = `/${data['name']} - Chat`
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
    // window.history.replaceState({"pageTitle": `${data['name']} - Chat`}, "", `/chat/${data['name']}`);
    // roomname = document.getElementById("RoomDisplay").innerHTML = '/'+data['name'];
    window.history.replaceState({"pageTitle": `Private Chat`}, "", `/chat/${data['name']}`);
    roomname = document.getElementById("RoomDisplay").innerHTML = 'Private Chat';
    document.title = `/Private`
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
    socket.emit('room_connect', room)
}

function openuserinfo(user) {
    socket.emit('private_connect', getCookie('Userid'), user)
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

// function BTMLog() {
//   if (Math.floor(window.scrollY) === window.scrollMaxY) {
//     console.log("cheese");
//     setTimeout(ToBtm, 10000)
//   } 
// }

// function ToBtm() {
//   window.scrollTo(0, chatDiv.scrollHeight);
// }

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
    private = window.sessionStorage.getItem('private')
    ID = window.sessionStorage.getItem("ID")
    socket.emit('message_chat', user, messageL, ID, userid, private);
    window.scrollTo(0, chatDiv.scrollHeight);
}


setInterval(BTMLog, 3000)

function renderChat(messages, ID) {
    // console.log(messages)
    let newline = "<br>";
    let chatDiv = document.getElementById("chat");
    if (ID === window.sessionStorage.getItem('ID') || ID === "all") {
        chatDiv["innerHTML"] = chatDiv["innerHTML"] + messages + newline;
    }
}


function checkKey() {
    if (event.key === "Enter") {
        sendMessage();
    }
}