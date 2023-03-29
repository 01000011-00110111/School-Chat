function JsendMessage() {
    let message = document.getElementById('jsendT');
    socket.emit('message_chat', "aaaaaaaaaaaaaaaa", "[Joke of the day]: ", "", "", message.value, "#D51956", "");
    message.value = "";
}

// needed so JOTD still works
function JsendMessageJ() {
    let message = document.getElementById('jsendTJ');
    socket.emit('message_chat', "aaaaaaaaaaaaaaaa", "[Joke of the day]: ", "", "", message.value, "#D51956", "");
    message.value = "";
}

function SOsendMessage() {
    let messageElement = document.getElementById('SOsendT');
    socket.emit('message_chat', "aaaaaaaaaaaaaaa", "[SONG]: ", "", "", messageElement.value, "#08bd71", "");
    messageElement.value = "";
}

function SOsendMessageE() {
    let messageElement = document.getElementById('SOsendTE');
    socket.emit('message_chat', "aaaaaaaaaaaaaaa", "[SONG]: ", "", "", messageElement.value, "#08bd71", "");
    messageElement.value = "";
}

// take a img url, and convert it into a img html tag
function sendImage() {
    let messageElement = document.getElementById("sendimgT");
    let toSend = "<img src='" + messageElement["value"] + "'></img>"

    messageElement["value"] = "";

    socket.emit('admin_message', toSend);
 =} //need to make of this

function refreshUsers() {
    socket.emit('admin_cmd', "refresh_users");
}

// see comment inside function    
function dummyajax(jsonData) {
    // dummy function so ajaxPostRequest doesent error out from no function callback
    return;
}