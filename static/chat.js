// define socketio connection
const socket = io();

socket.on("ping_test", (Obj) => {
    pingHandle(Obj);
});

socket.on("message_chat", (message) => {
    renderChat(message);
});

if (Notification.permission === "default") {
    Notification.requestPermission();
}

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

function NotificationsB() {
    Notifications = getCookie("Notifications");
    let notifB = document.getElementById("notif");

  if (Notifications === "true") {
      document.cookie = "Notifications=false; path=/";
      notifB.value = "Enable notifications";
      notifB.style.backgroundColor = "green";
  } else {
      document.cookie = "Notifications=true; path=/";
      notifB.value = "Disable notifications";
      notifB.style.backgroundColor = "red";

  }
}

socket.on("ping", ({ who, from, pfp, message }) => {
    let userElement = document.getElementById("username");
    let user_name = userElement.value;
    nonotif = getCookie("Notifications");

    if ((nonotif === "true") && (Notification.permission === "granted")) {
        if (user_name === who) {
            new Notification("You have been pinged by:", { body: from + ": " + message, icon: '/static/favicon.ico'});
        } else if (who === user_name) {
            return;
        } else if (who === "cseven" && user_name === "csevenReal") {
            new Notification("You have been pinged by:", { body: from + ": " + message, icon: '/static/favicon.ico'});
        } else if (who === "cserver" && user_name === "cserverReal") {
            new Notification("You have been pinged by:", { body: from + ": " + message, icon: '/static/favicon.ico'});
        } else if (who === "everyone") {
            new Notification("You have been pinged by:", { body: from + ": " + message, icon: '/static/favicon.ico'});
        }
    }
});

socket.on("reset_chat", (who) => {
    let chatDiv = document.getElementById("chat");
    if (who === "admin") {
        chatDiv.innerHTML = "[SYSTEM]: <font color='#ff7f00'>Chat reset by a admin.</font><br>";
    } else if (who === "auto") {
        chatDiv.innerHTML = "[SYSTEM]: <font color='#ff7f00'>Chat reset by automatic wipe system.</font><br>";
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
    let onlinelsDiv = document.getElementById("onlinels");
    let online_count = db.length;
    for (onlineUser of db) {
        if (onlineUser === "cserverReal") {
            onlineUser = "cserver";
        } else if (onlineUser === null) {
            onlineUser = "Anonymous";
        } else if (onlineUser === "") {
            onlineUser = "Anonymous";
        } else if (onlineUser === "csevenReal") {
            onlineUser = "cseven";
        }
        online = online + onlineUser + newline;
        onlinels = onlinels + "<a onclick=changeWisperUser('" + onlineUser + "')>" + onlineUser + '</a>';
    }
    let final_online = "<font size=5%>Online: " + online_count + "</font><br><br>" + online;
    onlinelsDiv["innerHTML"] = onlinels;
    onlineDiv["innerHTML"] = final_online;
});

function changeWisperUser(username) {
    window.sessionStorage.setItem('wisperUser', username);
    document.getElementById('onelinelsbtn').value = username + " selected.";
}

function loadChat() {
    ajaxGetRequest("/chat_logs", loadChatStartup);
}

function getCookie(name) {
    name = name + "=";
    var cookies = document.cookie.split(';');
    for(var i = 0; i <cookies.length; i++) {
        var cookie = cookies[i];
        while (cookie.charAt(0)==' ') {
            cookie = cookie.substring(1);
        }
        if (cookie.indexOf(name) == 0) {
            return cookie.substring(name.length,cookie.length);
        }
    }
    return "";
}

function runCheckStartup() {
    setDarkStyle();
    loadChat();
}

function runStartup() {
    loadChat();
    document.cookie = "Notifications=true; path=/";
    username =  window.localStorage.getItem("username")
    socket.emit("username", username);
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

function wisperMessage() {
    let sender = document.getElementById("user")["value"];
    let message = document.getElementById("private_msg");
    let recipient = window.sessionStorage.getItem('wisperUser');

    let messageL = toHyperlink(message.value);
    message.value = "";
    socket.emit("wisper_chat", messageL, recipient, sender);
}



function sendMessage() {
    let messageElement = document.getElementById("message");
    let user = document.getElementById("user")["value"]
    let message = messageElement["value"];
    if (message === "") {
        return;
    }
    
    messageL = toHyperlink(message);
    messageElement["value"] = "";
    socket.emit('message_chat', user, messageL);
    window.scrollTo(0, document.body.scrollHeight);
}

function loadChatStartup(jsonString) {
    let newline = "<br>";
    let chatDiv = document.getElementById("chat");
    let chat = "";
    let messages = JSON.parse(jsonString);
    for (let messageObj of messages) {
        chat = chat + messageObj["message"] + newline;
    }

    chatDiv["innerHTML"] = chat;
    window.scrollTo(0, document.body.scrollHeight);
}

function renderChat(messages) {
    let newline = "<br>";
    let chatDiv = document.getElementById("chat");
    if (Notification.permission === 'granted' && !document.hidden) {
    }

    chatDiv["innerHTML"] = chatDiv["innerHTML"] + messages + newline;
}


function checkKey() {
    if (event.key === "Enter") {
        sendMessage();
    }
}