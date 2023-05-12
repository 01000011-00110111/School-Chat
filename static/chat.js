// define socketio connection
const socket = io();



socket.on("message_chat", (message) => {
    renderChat(message);
});

socket.on("reload_pages", (muteUserName) => {
    let userElement = document.getElementById("username");
    let user_name = userElement["value"];

    if (muteUserName === user_name) {
        location.reload();
        // youfoundanotheregg();
    } else if (muteUserName === "everyone") {
        location.reload();
        // youfoundanotheregg();
    }
});

if (Notification.permission === "default") {
    Notification.requestPermission();
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

function openprivchat() {
// call this in online for private messaging (TM) on that
}

socket.on("ban", (mute_user_name) => {
    bancline(mute_user_name);
});

socket.on("mute", (mute_user_name) => {
    muteusr(mute_user_name);
});

socket.on("unmute", (mute_user_name) => {
    unmuteusr(mute_user_name);
});

function bancline(mute_user_name) {
    let ismutted = window.localStorage.getItem("permission")
    let userElement = document.getElementById("username");
    let user_name = userElement["value"];
    if (ismutted === 'muted' || ismutted === "true") {
        if (user_name === mute_user_name) {
            window.localStorage.setItem("permission", "banned");
            updateacc();
        }
    }
}

function muteusr(mute_user_name) {
    let ismutted =  window.localStorage.getItem("permission")
    let userElement = document.getElementById("username");
    let user_name = userElement["value"];
    if (ismutted === 'true') {
        if (user_name === mute_user_name) {
            window.localStorage.setItem("permission", "muted");
            updateacc();
        }
    } else if (ismutted === 'banned') {
        window.localStorage.setItem("permission", "banned");
    } else {
        window.localStorage.setItem("permission", "true");
    }
}

function unmuteusr(mute_user_name) {
    let ismutted = window.localStorage.getItem("permission")
    let userElement = document.getElementById("username");
    let user_name = userElement["value"];
    if (ismutted === 'muted') {
        if (user_name === mute_user_name) {
            window.localStorage.setItem("permission", "true");
            updateacc();
        }
    } else if (ismutted === 'banned') {
        window.localStorage.setItem("permission", "banned");
    } else {
        window.localStorage.setItem("permission", "true");
    }
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
    window.localStorage.setItem("Profileactive", "true")
    document.getElementById("mySidenav").style.backgroundColor = "#111";
  // document.getElementById("accountStuff").style.visibility = "hidden";
    let theme = whichEvent(window.localStorage.getItem("theme"));
    if (theme === "") {
        whichEvent();
    }
    access = window.localStorage.getItem("access");
    if (access === 'true') {
        runStartup();
        checkMsgBox();

    } else {
        // must be here, otherwise popup could be bypased
        let message_box = document.getElementById('message');
        let send = document.getElementById('send');
        let sidenav = document.getElementById('topleft');
        sidenav.disabled = true;
        send.disabled = true;
        message_box.disabled = true;
    } // else DIE
}


function runLimitedStartup() {
    runStartup();
    let message_box = document.getElementById('message');
    let send = document.getElementById('send');
    let sidenav = document.getElementById('topleft');
    sidenav.disabled = true;
    send.disabled = true;
    message_box.disabled = true;
    window.localStorage.setItem("access", "false");
}

function yesTOS() {
    access = 'true';
    window.localStorage.setItem("access", "true");
    // document.cookie = "permission=false; path=/";
    runStartup();
    checkMsgBox();
    setDarkStyle();
}

function runStartup() {
    document.getElementById("dev_chat_iframe").src = "";
    window.sessionStorage.setItem("ai", "false");
    loadChat();
    // userElement = window.localStorage.getItem("");
    document.cookie = "Notifications=true; path=/";
    socket.emit("username", "");
}

function checkMsgBox() {
    let message_box = document.getElementById('message');
    let send = document.getElementById('send');
    let sidenav = document.getElementById('topleft');
    sidenav.disabled = false;
    send.disabled = false;
    message_box.disabled = false;
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
    let user = document.getElementById("username")["value"];
    let message = document.getElementById("private_msg");
    let sender = window.sessionStorage.getItem('wisperUser');
    let userColor = document.getElementById("user_color")["value"];
    let messageColor = document.getElementById("message_color")["value"];
    let ismutted = window.localStorage.getItem("permission");

    if (ismutted === "banned" || ismutted === "muted") {
        return;
    }

    if (message === "") {
        return;
    }
    
    if (user === "cserverReal") {
        user = "cserver";
    } else if (user === "Dev EReal") {
        user = "Dev E";
    }

    // if (sender === user) {
        // return;
    // }

    let sender_f = ""
    if (sender === "cserver") {
        sender_f = "cserverReal";
    } else if (sender === "Dev E" || sender === "C7") {
        sender_f = "Dev EReal";
    } else {
        sender_f = sender;
    }
    let messageL = toHyperlink(message.value);
    let user_color_name = "<font color='" + userColor + "'>" + user + "</font>";
    let message_color_send = "<font color='" + messageColor + "'>" + messageL + "</font>";


    // insert some joke here
    message.value = "";
    socket.emit("wisper_chat", message_color_send, sender_f, user_color_name);
    let messages = "<i>You wispered to " + "<font color='#c47302'>" + sender + "</font>" + " about: </i>" + message_color_send;
    renderChat(messages);
}

function sendMessage() {
    let message = document.getElementById("message")["value"];
    let ai = window.sessionStorage.getItem("ai");
    if (ai === "true") {
        if (message === "$sudo disable ai") {
            sendMessage2();
            return;
        } else {
            sendMessageai();
        }
    } else {
        sendMessage2();
    }
}

function sendMessage2() {
    let messageElement = document.getElementById("message");
    let userElement = document.getElementById("username");
    let profileElement = document.getElementById("profile_picture");
    let roleElement = document.getElementById("role")
    let messageColorElement = document.getElementById("message_color");
    let roleColorElement = document.getElementById("role_color");
    let userColorElement = document.getElementById("user_color");
    let ismutted = window.localStorage.getItem("permission");

    let message = messageElement["value"];
    let user_name = userElement["value"];
    let profile_picture = profileElement["value"]
    let role = roleElement["value"];
    let user_color = userColorElement["value"];
    let message_color = messageColorElement["value"];
    let role_color = roleColorElement["value"];

    if (message === '$sudo enable ai') {
        document.title = "Class Chat AI";
        window.sessionStorage.setItem("ai", "true");
    } else if (message === '$sudo disable ai') {
        document.title = "OCD wleb Potato man Skill Issue!!!1!";
        window.sessionStorage.setItem("ai", "false");
    }

    if (user_color === "#000000") {
        user_color = "#ffffff";
    }

    if (message_color === "#000000") {
        message_color = "#ffffff";
    }

    if (role_color === "#000000") {
        role_color = "#ffffff";
    }

    window.localStorage.setItem("username", user_name);
    window.localStorage.setItem("profile_picture", profile_picture);

    if (message === "") {
        return;
    } else if (message === " ") {
        return;
    } else if (message === "  ") {
        return;
    }

    messageL = toHyperlink(message);

    messageElement["value"] = "";
    socket.emit('message_chat', user_name, user_color, role, role_color, messageL, message_color, profile_picture);
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
    ProfilesB();
}


function checkKey() {
    if (event.key === "Enter") {
        sendMessage();
    }
}


function youfounddaegg() {
    let i = 0
    while (i > 600) {
        setTimeout(setChristmasTheme, 1000);
        setTimeout(setDarkStyle, 1000);
        setTimeout(setLightStyle, 1000);
        setTimeout(setThanksTheme, 1000);
        setTimeout(setHollowTheme, 1000);
        setTimeout(setNewyearsTheme, 1000);
        setTimeout(setSpecalStyle, 1000);
        i++
    }
}

function youfoundanotheregg() {
    let body = document.getElementById("body");
    body.style.webkitAnimation = "rainbowb 5s infinite";
}

function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}

function devopenNav() {
    document.getElementById("DevStuff").style.width = "550px";
    document.getElementById("DevStuff").style.paddingLeft = "5%";
}

function devcloseNav() {
    document.getElementById("DevStuff").style.width = "0";
    document.getElementById("DevStuff").style.paddingLeft = "0";
}

function opendevchat() {
    document.getElementById("dev_chat").style.width = "1250px";
    document.getElementById("dev_chat").style.paddingLeft = "5%";
    document.getElementById("dev_chat_iframe").src = "https://dev.school-chat.us/chat";
}

function closedevchat() {
    document.getElementById("dev_chat").style.width = "0";
    document.getElementById("dev_chat").style.paddingLeft = "0";
    document.getElementById("dev_chat_iframe").src = "";
}

function EditopenNav() {
    document.getElementById("EditorStuff").style.width = "550px";
    document.getElementById("EditorStuff").style.paddingLeft = "5%";
}

function EditcloseNav() {
    document.getElementById("EditorStuff").style.width = "0";
    document.getElementById("EditorStuff").style.paddingLeft = "0";
}

function JOTDopenNav() {
    document.getElementById("JOTDStuff").style.width = "550px";
    document.getElementById("JOTDStuff").style.paddingLeft = "5%";
}

function JOTDcloseNav() {
    document.getElementById("JOTDStuff").style.width = "0";
    document.getElementById("JOTDStuff").style.paddingLeft = "0";
}

function ModopenNav() {
    document.getElementById("ModStuff").style.width = "550px";
    document.getElementById("ModStuff").style.paddingLeft = "5%";
}

function ModcloseNav() {
    document.getElementById("ModStuff").style.width = "0";
    document.getElementById("ModStuff").style.paddingLeft = "0";
}

function dropdownTheme() {
    document.getElementById("myDropdown").classList.toggle("show");
}

window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    } else if (!event.target.matches('.mySidenav')) {
        // what is this
    }
}

function Onlinewprls() {
  document.getElementById("onlinels").classList.toggle("show");
}

window.onclick = function(event) {
  if (!event.target.matches('.onelinelsbtn')) {
    var dropdowns = document.getElementsByClassName("droptheme");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
} 

function DropdownTXTtheme() {
    document.getElementById("DropdownTXT").classList.toggle("showTXT");
}
