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

function reloadPages() {
    let muteuserElement = document.getElementById("muteuserbox");
    let mute_user_name = muteuserElement["value"];

    if (mute_user_name === "Dev EReal") {
        mute_user_name = "Dev E"
    } else if (mute_user_name === "cserverReal") {
        mute_user_name = "cserver"
    }
    
    socket.emit('reload_page', mute_user_name)
}

function banHammer() {
    let muteuserElement = document.getElementById("muteuserbox");
    let mute_user_name = muteuserElement["value"];

    if (mute_user_name === "Dev EReal") {
        mute_user_name = "Dev EReal"
    } else if (mute_user_name === "cserverReal") {
        mute_user_name = "cserver"
    } else if (mute_user_name === "Steven") {
        // do not remove this or ELSE
        mute_user_name = "STEVEN Payed a box of poptarts and gummys for immunity"
    }
    
    socket.emit('ban_cmd', mute_user_name)
}

function mute() {
    let muteuserElement = document.getElementById("muteuserbox");
    let mute_user_name = muteuserElement["value"];

    if (mute_user_name === "Dev EReal") {
        mute_user_name = "Dev EReal"
    } else if (mute_user_name === "cserverReal") {
        mute_user_name = "cserver"
    } else if (mute_user_name === "Steven") {
        mute_user_name = "STEVEN Payed a box of poptarts and gummys for immunity"
    }
    
    socket.emit('mute_cmd', mute_user_name)
}

function unmute() {
    let muteuserElement = document.getElementById("muteuserbox");
    let mute_user_name = muteuserElement["value"];
    socket.emit('unmute_cmd', mute_user_name)
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

// send a bunch of black lines to chat system
function testChatGC() {
    socket.emit('admin_cmd', "blanks");
}

function EsendMessage() {
    // just bits and pieces from sendMessage
    let messageElement = document.getElementById("EventMSGT");

    message = '<font color="e54e40">' + messageElement["value"] + '</font>' + "</h3>"
    messageElement["value"] = "";
    let toSend = "<h3> [Event]: " + message + "</h3>"
    // send via socketio
    socket.emit('admin_message', toSend);
}

// get stats from the replit instance
function getStats() {
    socket.emit('admin_cmd', "full_status");
}

function clearDB() {
    socket.emit('admin_cmd', "username_clear");
}

function reset_chat() {
    socket.emit("admin_cmd", "reset_chat");
}

// lock/unlock chat helper functions
function lock_chat() {
    socket.emit('admin_cmd', "lock");
}

// unlocks chat
function unlock_chat() {
    socket.emit('admin_cmd', "unlock");
}
