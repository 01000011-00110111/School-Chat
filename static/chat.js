// define socketio connection
const socket = io();

socket.on("ping_test", (Obj) => {
    pingHandle(Obj);
});

socket.on("message_chat", (message, roomid) => {
    renderChat((message), roomid);
});

socket.on("troll", (message, roomid) => {
    renderChat(message, roomid);
    var audio = new Audio('static/airhorn_default.wav');
    audio.play();
});

function pingHandle(Obj=null) {
    user = document.getElementById("user")["value"];
    if (Obj === null) {
        let start = Date.now();
        socket.emit('pingtest', start);
    } else {
        let end = Date.now();
        let diff = end - Obj['start']
        socket.emit('admin_message', '[SYSTEM]: <font color="#ff7f00">Ping Time: ' + diff + 'ms RTT</font>', user);
    }
}

socket.on("ping", ({ who, from, pfp, message }) => {
    let userElement = document.getElementById("username");
    let user_name = userElement.value;

        if (user_name === who) {
            new Notification("You have been pinged by:", { body: from + ": " + message, icon: '/static/favicon.ico'});
        } else if (who === "everyone") {
            new Notification("You have been pinged by:", { body: from + ": " + message, icon: '/static/favicon.ico'});
        }
});

socket.on("reset_chat", (who, roomid) => {
    if (roomid === window.sessionStorage.getItem('roomid')) {
        let chatDiv = document.getElementById("chat");
        if (who === "admin") {
            chatDiv.innerHTML = "[SYSTEM]: <font color='#ff7f00'>Chat reset by a admin.</font><br>";
        } else if (who === "auto") {
            chatDiv.innerHTML = "[SYSTEM]: <font color='#ff7f00'>Chat reset by automatic wipe system.</font><br>";
        }
    }
});

socket.on("force_username", (statement) => {
    socket.emit("username", window.localStorage.getItem("username"));
});

socket.on("online", (db) => {
    let newline = "<br>"
    let online = "";
    let onlinels = '';
    let onlineDiv = document.getElementById("online_users");
    // let onlinelsDiv = document.getElementById("onlinels");
    let online_count = db.length;
    for (onlineUser of db) {
        online = online + onlineUser + newline;
        onlinels = onlinels + "<a onclick=changeWisperUser('" + onlineUser + "')>" + onlineUser + '</a>';
    }
    let final_online = "<font size=5%>Online: " + online_count + "</font><br><br>" + online;
    // onlinelsDiv["innerHTML"] = onlinels;
    onlineDiv["innerHTML"] = final_online;
});

function runCheckStartup() {
    setDarkStyle();
}

function runStartup() {
    setDarkStyle();
    window.sessionStorage.setItem("roomid", 'ilQvQwgOhm9kNAOrRqbr');
    socket.emit('get_prefs', document.getElementById("user")["value"]);
    socket.emit('get_perms');
    username = window.localStorage.getItem("username");
    let user = document.getElementById("user")["value"];
    socket.emit("username", username);
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
    }
}

socket.on("room_data", (data) => {
    window.sessionStorage.setItem("roomid", data['roomid']);
    let newline = "<br>";
    let chatDiv = document.getElementById("chat");
    let chat = ""; 
    for (let messageObj of data['messages']) {
        chat = chat + messageObj + newline;
    }

    chatDiv["innerHTML"] = chat;
    window.scrollTo(0, chatDiv.scrollHeight);
});

function changeRoom(room) {
    socket.emit('room_connect', room)
}

function toHyperlink(str) {
    var pattern1 = /(\b(https?|ftp|sftp|file|http):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig;
    var str1 = str.replace(pattern1, "<a href='$1'>$1</a>");
    // make it show without the https://
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
    console.log(roomid)
    if (roomid === window.sessionStorage.getItem('roomid')) {
        chatDiv["innerHTML"] = chatDiv["innerHTML"] + messages + newline;
    }
}


function checkKey() {
    if (event.key === "Enter") {
        sendMessage();
    }
}