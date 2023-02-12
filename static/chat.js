// define socketio connection
const socket = io();

// add messages as they are recieved
socket.on("message_chat", (message) => {
    renderChat(message);
});

socket.on("reset_chat", (who) => {
    let chatDiv = document.getElementById("chat");
    if (who === "admin") {
        chatDiv["innerHTML"] = "[SYSTEM]: <font color='#ff7f00'>Chat reset by a admin.</font><br>"
    } else if (who === "auto") {
        chatDiv["innerHTML"] = "[SYSTEM]: <font color='#ff7f00'>Chat reset by automatic wipe system.</font><br>"
    }
});

socket.on("force_username", (statement) => {
    socket.emit("username", window.localStorage.getItem("username"));
});

socket.on("cookieEater", (statement) => {
    deleteAllCookies();
    let userElement = document.getElementById("user"); 
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
    for (onlineUser of db) {
        if (onlineUser === "cserverReal") {
            onlineUser = "cserver"
        } else if (onlineUser === null) {
            onlineUser = "Anonymous"
        } else if (onlineUser === "") {
            onlineUser = "Anonymous"
        } else if (onlineUser === "Dev EReal") {
            onlineUser = "Dev E"
        }
        online = online + onlineUser + newline;
    }
    onlineDiv["innerHTML"] = online;
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
    let userElement = document.getElementById("user");
    let user_name = userElement["value"];
    console.log(muteUserName);
    console.log(user_name);
    if (user_name === muteUserName) {
        let ismutted = 'banned'
        document.cookie = "permission=" + ismutted + "; path=/";
    }
}

function muteusr(muteUserName) {
    let userElement = document.getElementById("user");
    let user_name = userElement["value"];
    console.log(muteUserName);
    console.log(user_name);
    if (user_name === muteUserName) {
        let ismutted = 'true'
        document.cookie = "permission=" + ismutted + "; path=/";
    }
}

function unmuteusr(muteUserName) {
    let userElement = document.getElementById("user");
    let user_name = userElement["value"];
    let ismutted = getCookie('permission');
    console.log(muteUserName);
    console.log(user_name);
    if (ismutted === 'true') {
        if (user_name === muteUserName) {
            let ismutted = 'false';
            document.cookie = "permission=" + ismutted + "; path=/";
        }
    } else {
        let ismutted = 'banned'
    }
}

// This function requests the server send it a full chat log
function loadChat() {
    ajaxGetRequest("/chat", loadChatStartup); 
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
    whichEvent(window.localStorage.getItem("theme"));
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
    document.cookie = "permission=false; path=/";
    runStartup();
    checkMsgBox();
}

// stuff to run at startup and what happens when you do agree to the rules
function runStartup() {
    // load previous chat messages
    loadChat();
    // add the username currently in a cookie unless there is none
    let userElement = document.getElementById("user"); 
    let user_color = document.getElementById("user_color");
    let message_color = document.getElementById("message_color");
    let role_color = document.getElementById("role_color");
    let roleElement = document.getElementById("role");
    user_color["value"] = window.localStorage.getItem("user_color");
    message_color["value"] = window.localStorage.getItem("message_color");
    role_color["value"] = window.localStorage.getItem("role_color");
    roleElement["value"] = window.localStorage.getItem("role");
    userElement["value"] = window.localStorage.getItem("username");
    ismutted = getCookie("permission");
    // remove when popup is implemented
    whichEvent(window.localStorage.getItem("theme"));
    window.localStorage.getItem("permission");
    socket.emit("username", window.localStorage.getItem("username"));
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

// This function sends the server the new message and receives
// the full chat log in response
function sendMessage() {
    // Get an object representing the text box (where we get the user and msg to get sent)
    let messageElement = document.getElementById("message");
    let userElement = document.getElementById("user");
    let profileElement = document.getElementById("profile_picture");
    let roleElement = document.getElementById("role")
    let messageColorElement = document.getElementById("message_color");
    let roleColorElement = document.getElementById("role_color");
    let userColorElement = document.getElementById("user_color");  
    let ismutted = getCookie("permission");
    window.localStorage.setItem("permission", "false");
    
  
    // Save the message text 
    let message = messageElement["value"];
    let user_name = userElement["value"];
    let profile_picture = profileElement["value"]
    let role = roleElement["value"]
    let user_color = userColorElement["value"];
    let message_color = messageColorElement["value"];
    let role_color = roleColorElement["value"]; 

    //if (theme === 'light' && )
    if (user_color === "#000000") {
        user_color = "#ffffff";
    }

    if (message_color === "#000000") {
        message_color = "#ffffff";
    }

    if (role_color === "#000000") {
        role_color = "#ffffff";
    }

    // needs to be here, otherwise cookie is overriten
    socket.emit("username_msg", user_name, getCookie("username"));

    // just so nothing gets overritten in cookies, is has to be up here
    document.cookie = "username=" + user_name + "; path=/";
    document.cookie = "profile_picture=" + profile_picture + "; path=/";
    document.cookie = "user_color=" + user_color + "; path=/";
    document.cookie = "message_color=" + message_color + "; path=/";
    document.cookie = "role_color=" + role_color + "; path=/";
    document.cookie = "role=" + role + "; path=/";

    // session stuff goes here
    window.localStorage.setItem("role", role);
    window.localStorage.setItem("role_color", role_color);
    window.localStorage.setItem("message_color", message_color);
    window.localStorage.setItem("user_color", user_color);
    window.localStorage.setItem("username", user_name);
    window.localStorage.setItem("profile_picture", profile_picture);
    

    let profile_img = "<img style='max-height:25px; max-width:25px; overflow: hidden' src='" + profile_picture + "'></img>";
  
    if (ismutted === 'true') {
        return;
    } else if (ismutted === 'banned') {
        return;
    }
    
    if (message === "") {
        return;
    } else if (message === " ") {
        return;
    } else if (message === "  ") {
        return;
    }

    if (role === "Stoopid" || role === "half stupid-smart" || role === "dumbbbb") {
        role = "super -smart"
    }


    // wetll too late 
    // the stupid long user_name check
    // now implemented on server side
    // took much longer than it should have
    // Let the user "see" the message was sent by clearing the textbox
    messageElement["value"] = "";
    // We will send the message as a JSON encoding of an obejct.
    // This will simplify what is needed for future improvements
    // add this in later by changing message to user_color_name
    // console.log(user_color)
    let user_color_name = "<font color='" + user_color + "'>" + user_name + "</font>";
    let message_color_send = "<font color='" + message_color + "'>" + message + "</font>";
    let role_color_send = "<font color='" + role_color + "'>" + role + "</font>";
    // add profile_picture before user_name after I figure out how to limit how big an image is // i know how
    // still need user chooseable colors, will add to github issue tracker
    if (role === "") {
        let toSend = profile_img + user_color_name.toString() + " - " + message_color_send
        socket.emit('message_chat', toSend);
        return;
    } else {
        let toSend = profile_img + user_color_name.toString() + " (" + role_color_send + ")" + " - " + message_color_send
        socket.emit('message_chat', toSend);
        return;
    }
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
    console.log(localStorage.getItem("permission"))
    window.scrollTo(0, document.body.scrollHeight);
}

// This is the callback function used for both ajax requests
// It will be called by JS automatically whenever we get a response from the server
function renderChat(messages) {
    // Store the HTML needed to move to the next line. This makes the coding easier to read
    let newline = "<br>";
    // Get an object representing the div displaying the chat
    let chatDiv = document.getElementById("chat");

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
    document.getElementById("devSidenav").style.width = "550px";
    document.getElementById("devSidenav").style.paddingLeft = "5%";
}

function devcloseNav() {          
    document.getElementById("devSidenav").style.width = "0";
    document.getElementById("devSidenav").style.paddingLeft = "0";
}

function openaccNav() {
    document.getElementById("accSidenav").style.width = "250px";
}

function closeaccNav() {          
    document.getElementById("accSidenav").style.width = "0";
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
    } else if (!event.target.matches('.mySidenav')) {
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
