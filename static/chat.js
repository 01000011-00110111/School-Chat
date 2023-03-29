// define socketio connection
const socket = io();


// add messages as they are recieved
socket.on("message_chat", (message) => {
    renderChat(message);
});

socket.on("reload_pages", (muteUserName) => {
    // something something anoy everyone
    let userElement = document.getElementById("username");
    let user_name = userElement["value"];

    if (muteUserName === user_name) {
        location.reload();
    } else if (muteUserName === "everyone") {
        location.reload();
    }
});


// new notification thing
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

socket.on("ping", ({ who, from }) => {
    let userElement = document.getElementById("username");
    let user_name = userElement.value;
    nonotif = getCookie("Notifications");

    if ((nonotif === "true") && (Notification.permission === "granted")) {
        if (user_name === who) {
            new Notification("You have been pinged by:", { body: from, icon: "/static/troll-face.jpeg"});
        } else if (who === "Dev E" && user_name === "Dev EReal") {
            new Notification("You have been pinged by:", { body: "Dev E", icon: "/static/troll-face.jpeg"});
        } else if (who === "cserver" && user_name === "cserverReal") {
            new Notification("You have been pinged by:", { body: "cserver", icon: "/static/troll-face.jpeg"});
        } else if ((who === "Owen" || who === "owen") && user_name === "¿Owen?") {
            new Notification("You have been pinged by:", { body: from, icon: "/static/troll-face.jpeg"});
        } else if (who === "everyone") {
            new Notification("You have been pinged by:", { body: from, icon: "/static/troll-face.jpeg"});
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

socket.on("cookieEater", (statement) => {
    deleteAllCookies();
    let userElement = document.getElementById("username");
    let user_color = document.getElementById("user_color");
    let message_color = document.getElementById("message_color");
    let role_color = document.getElementById("role_color");
    let roleElement = document.getElementById("role");
    user_color["value"] = "#000000";
    message_color["value"] = "#000000";
    role_color["value"] = "#000000";
    roleElement["value"] = "";
    userElement["value"] = "";
});

socket.on("online", (db) => {
    let newline = "<br>"
    let online = "";
    let onlineDiv = document.getElementById("online_users");
    let online_count = db.length
    for (onlineUser of db) {
        if (onlineUser === "cserverReal") {
            onlineUser = "cserver";
        } else if (onlineUser === null) {
            onlineUser = "Anonymous";
        } else if (onlineUser === "") {
            onlineUser = "Anonymous";
        } else if (onlineUser === "Dev EReal") {
            onlineUser = "C7";
        }
        online = online + onlineUser + newline;
    }
    let final_online = "<font size=5%>Online: " + online_count + "</font><br><br>" + online
    onlineDiv["innerHTML"] = final_online;
});

socket.on("ban", (muteUserName) => {
    bancline(muteUserName);
});

socket.on("mute", (muteUserName) => {
    muteusr(muteUserName);
});

socket.on("unmute", (muteUserName) => {
    unmuteusr(muteUserName);
});

function bancline(muteUserName) {
    let permissionElement = document.getElementById("permission");
    let userElement = document.getElementById("username");
    let user_name = userElement["value"];
    let ismutted = permissionElement["value"];
    if (ismutted === 'muted' || ismutted === "true") {
        if (user_name === muteUserName) {
            document.getElementById("permission")["value"] = "banned";
            window.localStorage.setItem("permission", "banned");
        }
    }
}

function muteusr(muteUserName) {
    let permissionElement = document.getElementById("permission");
    let userElement = document.getElementById("username");
    let user_name = userElement["value"];
    let ismutted = permissionElement["value"];
    if (ismutted === 'true') {
        if (user_name === muteUserName) {
            document.getElementById("permission")["value"] = "muted";
            window.localStorage.setItem("permission", "muted");
        }
    } else if (ismutted === 'banned') {
        document.getElementById("permission")["value"] = "banned";
        window.localStorage.setItem("permission", "banned");
    } else {
        document.getElementById("permission")["value"] = "true";
        window.localStorage.setItem("permission", "true");
    }
}

function unmuteusr(muteUserName) {
    let permissionElement = document.getElementById("permission");
    let userElement = document.getElementById("username");
    let user_name = userElement["value"];
    let ismutted = permissionElement["value"];
    if (ismutted === 'muted') {
        if (user_name === muteUserName) {
            document.getElementById("permission")["value"] = "true";
            window.localStorage.setItem("permission", "true");
        }
    } else if (ismutted === 'banned') {
        document.getElementById("permission")["value"] = "banned";
        window.localStorage.setItem("permission", "banned");
    } else {
        document.getElementById("permission")["value"] = "true";
        window.localStorage.setItem("permission", "true");
    }
}

// This function requests the server send it a full chat log
function loadChat() {
    ajaxGetRequest("/chat_logs", loadChatStartup);
}

function deleteAllCookies() {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i];
        const eqPos = cookie.indexOf("=");
        const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
        document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT";
    }
}

// get specific cookie value
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

// the startup for cookies after the first time
function runCheckStartup() {
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


// what happens if you don't agree to the rules
function runLimitedStartup() {
    runStartup();
    // lock the abbility to type in chat
    let message_box = document.getElementById('message');
    let send = document.getElementById('send');
    let sidenav = document.getElementById('topleft');
    sidenav.disabled = true;
    send.disabled = true;
    message_box.disabled = true;
    // let access = 'false'
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

// stuff to run at startup and what happens when you do agree to the rules
function runStartup() {
    // load previous chat messages
    loadChat();
    // add the username currently in a cookie unless there is none
    // userElement = window.localStorage.getItem("");
    document.cookie = "Notifications=true; path=/";
    socket.emit("username", "");
}

function checkMsgBox() {
    // make sure message box is fine after accepting terms
    // makes sure that message box and send button are not disabled
    let message_box = document.getElementById('message');
    let send = document.getElementById('send');
    let sidenav = document.getElementById('topleft');
    sidenav.disabled = false;
    send.disabled = false;
    message_box.disabled = false;
}

function runCheckReset(message) {
    console.log(message)
    if (message === "[SYSTEM]: <font color='#ff7f00'>Chat reset by a admin.</font>") {
        let chatDiv = document.getElementById("chat");
        console.log("here")
        chatDiv["innerHTML"] = "[SYSTEM]: <font color='#ff7f00'>Chat reset by a admin.</font><br>"
        console.log(message)
        return "true";
    }
}

function toHyperlink(str) {
    // thank you stackoverflow for giving me this stupid regex script
    var pattern1 = /(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig;
    var str1 = str.replace(pattern1, "<a href='$1'>$1</a>");

    var pattern2 = /(^|[^\/])(www\.[\S]+(\b|$))/gim;
    var str2 = str1.replace(pattern2, '$1<a target="_blank" href="http://$2">$2</a>');

    return str2;
}

/*function reban() {
    let userElement = document.getElementById("user");
    let profileElement = document.getElementById("profile_picture");
    let roleElement = document.getElementById("role")
    let messageColorElement = document.getElementById("message_color");
    let roleColorElement = document.getElementById("role_color");
    let userColorElement = document.getElementById("user_color");
    let user_name = userElement["value"];
    let message = "I " + user_name + " have been banned as I cheated to get unbanned or unmutted."
    let profile_picture = profileElement["value"]
    let role = roleElement["value"]
    let user_color = userColorElement["value"];
    let message_color = messageColorElement["value"];
    let role_color = roleColorElement["value"];
    let user_color_name = "<font color='" + user_color + "'>" + user_name + "</font>";
    let message_color_send = "<font color='" + message_color + "'>" + message + "</font>";
    let role_color_send = "<font color='" + role_color + "'>" + role + "</font>";
    let profile_img = "<img style='max-height:25px; max-width:25px; overflow: hidden' src='" + profile_picture + "'></img>";
    if (role === "") {
        let toSend = profile_img + user_color_name.toString() + " - " + message_color_send
        socket.emit('message_chat', toSend);
        return;
    } else {
        let toSend = profile_img + user_color_name.toString() + " (" + role_color_send + ")" + " - " + message_color_send
        socket.emit('message_chat', toSend);
        return;
    }
}*/


function wisperMessage() {
    let user = document.getElementById("username")["value"];
    let message = document.getElementById("private_msg");
    let sender = document.getElementById("private_user")["value"];
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

    let sender_f = ""
    if (sender === "cserver") {
        sender_f = "cserverReal";
    } else if (sender === "Dev E") {
        sender_f = "Dev EReal";
    } else if (sender === "Owen") {
        sender_f = "¿Owen?";
    } else {
        sender_f = sender;
    }
    let messageL = toHyperlink(message.value);
    let user_color_name = "<font color='" + userColor + "'>" + user + "</font>";
    let message_color_send = "<font color='" + messageColor + "'>" + messageL + "</font>";


    // insert some joke here
    message.value = ""; // 
    socket.emit("wisper_chat", message_color_send, sender_f, user_color_name);
    let messages = "<i>You wispered to " + "<font color='#c47302'>" + sender + "</font>" + " about: </i>" + message_color_send;
    renderChat(messages);
}

// This function sends the server the new message and receives
// the full chat log in response
function sendMessage() {
    // Get an object representing the text box (where we get the user and msg to get sent)
    let messageElement = document.getElementById("message");
    let userElement = document.getElementById("username");
    let profileElement = document.getElementById("profile_picture");
    let roleElement = document.getElementById("role")
    let messageColorElement = document.getElementById("message_color");
    let roleColorElement = document.getElementById("role_color");
    let userColorElement = document.getElementById("user_color");
    let ismutted = window.localStorage.getItem("permission");

    // Save the message text
    let message = messageElement["value"];
    let user_name = userElement["value"];
    let profile_picture = profileElement["value"]
    let role = roleElement["value"];
    let user_color = userColorElement["value"];
    let message_color = messageColorElement["value"];
    let role_color = roleColorElement["value"];

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


    let profile_img = "<img style='max-height:25px; max-width:25px; overflow: hidden' src='" + profile_picture + "'></img>";

    if (ismutted === 'muted') {
        return;
    } else if (ismutted === 'banned') {
        return;
    } /*else if (ismutted === "") {
        socket.emit('ban_cmd', user_name)
        return;
    }*/

    if (message === "") {
        return;
    } else if (message === " ") {
        return;
    } else if (message === "  ") {
        return;
    }

    // maybe add links as links in html? idk might work (regex crap again)
    messageL = toHyperlink(message);

    // Let the user "see" the message was sent by clearing the textbox
    messageElement["value"] = "";
    socket.emit('message_chat', user_name, user_color, role, role_color, messageL, message_color, profile_img);
    window.scrollTo(0, document.body.scrollHeight);
}

// ran at startup so you get previous messages
function loadChatStartup(jsonString) {
    let newline = "<br>";
    // Get an object representing the div displaying the chat
    let chatDiv = document.getElementById("chat");
    let chat = "";
    let messages = JSON.parse(jsonString);
    // Loop through each message in the data sent from the server
    for (let messageObj of messages) {
        // Update our accumulator with the message's text
        chat = chat + messageObj["message"] + newline;
    }

    chatDiv["innerHTML"] = chat;
    window.scrollTo(0, document.body.scrollHeight);
}

// This is the callback function used for both ajax requests
// It will be called by JS automatically whenever we get a response from the server
function renderChat(messages) {
    // Store the HTML needed to move to the next line. This makes the coding easier to read
    let newline = "<br>";
    // Get an object representing the div displaying the chat
    let chatDiv = document.getElementById("chat");

    // filter message
    /*if (messages.startsWith("[") === true) {
        let parts = messages.split(":");
    } else {
        let parts = messages.split("-");
    }

    let parts = messages.split("-");

    // .replace(/<font .*>/, "")
    let username = parts[0].replace(/\<.*?[^\)]\>/g, "");
    let message = parts[1].replace(/\<.*?[^\)]\>/g, "");*/

    // new notification thing (and later have img pull the profile_picture link)
    if (Notification.permission === 'granted' && !document.hidden) {
         //new Notification(username, { body: message, icon: '/static/troll-face.jpeg'});
    }

    chatDiv["innerHTML"] = chatDiv["innerHTML"] + messages + newline;
}


function checkKey() {
    // Check if the enter key is pressed when typing
    if (event.key === "Enter") {
        sendMessage();
    }
}

  // Nav menu //
 //set the size of the Nav
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

function EditopenNav() {
    document.getElementById("editorStuff").style.width = "550px";
    document.getElementById("editorStuff").style.paddingLeft = "5%";
}

function EditcloseNav() {
    document.getElementById("editorStuff").style.width = "0";
    document.getElementById("editorStuff").style.paddingLeft = "0";
}

function JOTDopenNav() {
    document.getElementById("editorStuff").style.width = "550px";
    document.getElementById("editorStuff").style.paddingLeft = "5%";
}

function JOTDcloseNav() {
    document.getElementById("editorStuff").style.width = "0";
    document.getElementById("editorStuff").style.paddingLeft = "0";
}

function ModopenNav() {
    document.getElementById("modStuff").style.width = "550px";
    document.getElementById("modStuff").style.paddingLeft = "5%";
}

function ModcloseNav() {
    document.getElementById("modStuff").style.width = "0";
    document.getElementById("modStuff").style.paddingLeft = "0";
}

/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
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
    } else if (!event.target.matches('.mySidenav')) { // what was this for
        // whenever i can get sidenav-content (hidden element) implemented in css
        // simillar to dropdown-content, but with some widths changed and other stuff
        //var dropdowns = document.getElementsByClassName("dropdown-content");
        //var i;
        //for (i = 0; i < dropdowns.length; i++) {
        //  var openDropdown = dropdowns[i];
        //  if (openDropdown.classList.contains('show')) {
        //    openDropdown.classList.remove('show');
        //  }
        //}
    } /*else if (!event.target.matches('.dropbtnTXT')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('showTXT')) {
                openDropdown.classList.remove('showTXT');
            }
        }
    } */ //do we need this?
}

//The message text color dropdown button

function DropdownTXTtheme() {
    document.getElementById("DropdownTXT").classList.toggle("showTXT");
}
