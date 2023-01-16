  // Dev menu js code to keep chat.js cleaner and easy to read and find what you need//

// send message as the user [SYSTEM]
function systemmessage() {
    // just bits and pieces from sendMessage
    let messageElement = document.getElementById("systemsendT");

    message = '<font color="#ff7f00">' + messageElement["value"] + '</font>'
    messageElement["value"] = "";
    let toSend = "[SYSTEM]: " + message
    // send to socketio
    socket.emit('admin_message', toSend);
}

//"<a href='" + urlElement + "'>" + urlsendElement + "</a>"
function urlsend() {
    let urlElement = document.getElementById('urlsendT');
    let urlsendElement = document.getElementById('urlsendT2');
    message = "<a href='" + urlElement["value"] + "'>";
    urlmessage = urlsendElement["value"];
    urlElement["value"] = "";
    urlsendElement["value"] = "";
    let toSend = "[URL] - " + message + urlmessage + "</a>"
    if (message === "<a href=''>") {
        return;
    } else if (urlmessage === "") {
        return;
    }  
    socket.emit('admin_message', toSend);
}
// let hrefurlElement = "<a href='" + urlElement + "'>" + urlsendElement + "</a>"
// let message = hrefurlElement

//the force send code need a better info here
function FsendMessageA() {
    let messageElement = document.getElementById('fsendT');
    // 100% CPU usage lol on tablet lol
    //console.log(document.getElementById("user_name"));
    let toSend = "[Admin]: " + messageElement.value

    messageElement.value = "";
    // we use a diffrent endpoint, so it doesen't get blocked by the add_message function on the server end
    // also gets rid of a lot of checks inside add_message
    socket.emit('admin_message', toSend);
} 

function FsendMessageM() {
    let messageElement = document.getElementById('fsendT');
    // 100% CPU usage lol on tablet lol
    //console.log(document.getElementById("user_name"));
    let toSend = "[Mod]: " + messageElement.value

    messageElement.value = "";
    // we use a diffrent endpoint, so it doesen't get blocked by the add_message function on the server end
    // also gets rid of a lot of checks inside add_message
    socket.emit('admin_message', toSend);
} 

// take a img url, and convert it into a img html tag
function sendImage() {
    let messageElement = document.getElementById("sendimgT");
    let toSend = "<img src='" + messageElement["value"] + "'></img>"

    messageElement["value"] = "";

    socket.emit('admin_message', toSend);
}

// send a bunch of black lines to chat system
function testChatGC() {
    socket.emit('admin_cmd', "blanks");
}

function EsendMessage() {
    // just bits and pieces from sendMessage
    let messageElement = document.getElementById("EventMSGT");

    message = '<font color="e54e40">' + messageElement["value"] + '</font>' + "</h3>"
    messageElement["value"] = "";
    let toSend = "<h3> [Event]: " + message
    // send via socketio
    socket.emit('admin_message', toSend);
}

function reset_chat() {
    ajaxGetRequest('/reset', dummyajax);
}

// get stats from the replit instance
function getStats() {
    ajaxGetRequest("/stats", dummyajax);
}

// lock/unlock chat helper functions
function lock_chat() {
    ajaxGetRequest("/lock", dummyajax);
}

// unlocks chat
function unlock_chat() {
    ajaxGetRequest("/unlock", dummyajax);
}

function mute() {
    // filler
}

function unmute() {
    // filler
} 

function ban() {
    //document.cookie = "=" + user_name + "; path=/";
}

// see comment inside function
function dummyajax(jsonData) {
    // dummy function so ajaxPostRequest doesent error out from no function callback
    return;
}
