/* modderation */

function banHammer() {
    user = document.getElementById("user")["value"];
    let muteuserElement = document.getElementById("muteuserbox");
    let mute_user_name = muteuserElement["value"];
    socket.emit('ban_cmd', mute_user_name, user)
}

function mute() {
    user = document.getElementById("user")["value"];
    let muteuserElement = document.getElementById("muteuserbox");
    let mute_user_name = muteuserElement["value"];
    socket.emit('mute_cmd', mute_user_name, user)
}

function unmute() {
    user = document.getElementById("user")["value"];
    let muteuserElement = document.getElementById("muteuserbox");
    let mute_user_name = muteuserElement["value"];
    socket.emit('unmute_cmd', mute_user_name, user)
}

function reset_chat() {
    user = document.getElementById("user")["value"];
    socket.emit("admin_cmd", "reset_chat", user);
}

function lock_chat() {
    user = document.getElementById("user")["value"];
    socket.emit('admin_cmd', "lock", user);
}

function unlock_chat() {
    user = document.getElementById("user")["value"];
    socket.emit('admin_cmd', "unlock", user);
}

/*  dev stuff */

function testChatGC() {
    user = document.getElementById("user")["value"];
        socket.emit('admin_cmd', "blanks", user);
}

function getStats() {
    user = document.getElementById("user")["value"];
    socket.emit('admin_cmd', "full_status", user);
}

function shutdown_server() {
    user = document.getElementById("user")["value"];
        socket.emit('admin_cmd', "shutdown", user);
}

// function clearDB() {
//     user = document.getElementById("user")["value"];
//     socket.emit('admin_cmd', "username_clear", user);
// } DANGER DANGER

/* messaging */

function EsendMessage() {
    user = document.getElementById("user")["value"];
    let messageElement = document.getElementById("EventMSGT");
    message = '<font color="e54e40">' + messageElement["value"] + '</font>' + "</h3>"
    messageElement["value"] = "";
    let toSend = "<h3> [Event]: " + message + "</h3>"
    socket.emit('admin_message', toSend, user);
}

function FsendMessageM() {
    user = document.getElementById("user")["value"];
    let messageElement = document.getElementById('fsendT');
    let toSend = "[Mod]: " + messageElement.value
    messageElement.value = "";
    socket.emit('admin_message', toSend, user);
} 

function FsendMessageA() {
    user = document.getElementById("user")["value"];
    let messageElement = document.getElementById('fsendT');
    let toSend = "[Admin]: " + messageElement.value
    messageElement.value = "";
    socket.emit('admin_message', toSend, user);
} 

function systemmessage() {
    user = document.getElementById("user")["value"];
    let messageElement = document.getElementById("systemsendT");
    message = '<font color="#ff7f00">' + messageElement["value"] + '</font>'
    messageElement["value"] = "";
    let toSend = "[SYSTEM]: " + message
    socket.emit('admin_message', toSend, user)
}

function SOsendMessage(elem) {
    user = document.getElementById("user")["value"];
    let messageElement = document.getElementById(elem);
    socket.emit('message_chat', "aaaaaaaaaaaaaaa", "[SONG]: ", "", "", messageElement.value, "#08bd71", "", user);
    messageElement.value = "";
}

function JsendMessage(elem) {
    user = document.getElementById("user")["value"];
    let message = document.getElementById(elem);
    socket.emit('message_chat', "aaaaaaaaaaaaaaaa", "[Joke of the day]: ", "", "", message.value, "#D51956", "", user);
    message.value = "";
}

/* etc */

function refreshUsers() {
    user = document.getElementById("user")["value"];
    socket.emit('admin_cmd', "refresh_users", user);
}

function dummyajax(jsonData) {
    return;
}