function JsendMessage(elem) {
    user = document.getElementById("user")["value"];
    if (user === "C7" || user === "cserverReal" || user === "Shayla (The Midget)") {
        let message = document.getElementById(elem);
        socket.emit('message_chat', "aaaaaaaaaaaaaaaa", "[Joke of the day]: ", "", "", message.value, "#D51956", "");
        message.value = "";
    }
}

function SOsendMessage(elem) {
    user = document.getElementById("user")["value"];
    if (user === "C7" || user === "cserverReal" || "Owen...") {
        let messageElement = document.getElementById(elem);
        socket.emit('message_chat', "aaaaaaaaaaaaaaa", "[SONG]: ", "", "", messageElement.value, "#08bd71", "");
        messageElement.value = "";
    }
}

// take a img url, and convert it into a img html tag
function sendImage(elem) {
    let messageElement = document.getElementById(elem);
    let toSend = "<img src='" + messageElement["value"] + "'></img>"

    messageElement["value"] = "";

    socket.emit('admin_message', toSend);
}

function refreshUsers() {
    socket.emit('admin_cmd', "refresh_users");
}

// see comment inside function    
function dummyajax(jsonData) {
    // dummy function so ajaxPostRequest doesent error out from no function callback
    return;
}