  // mod menu js code to keep chat.js and dev-menu.js cleaner and easy to read and find what you need//

function clearCookies() {
    socket.emit('admin_message', "[Admin]: Cookies will be deleted in 10 seconds...");
    socket.emit('admin_cmd', "cookieEater")
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

function banHammer() {
    let muteuserElement = document.getElementById("muteuserbox");
    let userElement = document.getElementById("user");
    let mute_user_name = muteuserElement["value"];
    let user_name = userElement["value"];
        
    if (mute_user_name === "Dev E") {
        mute_user_name = user_name
    } else if (mute_user_name === "cserver") {
        mute_user_name = user_name
    }
    
    socket.emit('ban_cmd', mute_user_name)
}

function mute() {
    let muteuserElement = document.getElementById("muteuserbox");
    let userElement = document.getElementById("user");
    let mute_user_name = muteuserElement["value"];
    let user_name = userElement["value"];

    if (mute_user_name === "Dev E") {
        mute_user_name = user_name
    } else if (mute_user_name === "cserver") {
        mute_user_name = user_name
    }
    
    socket.emit('mute_cmd', mute_user_name)
}

function unmute() {
    let muteuserElement = document.getElementById("muteuserbox");
    let mute_user_name = muteuserElement["value"];
    socket.emit('unmute_cmd', mute_user_name)
}

// get stats from the replit instance
function getStats() {
    socket.emit('admin_cmd', "full_status");
}

/*
function lock_chat() {
    socket.emit('admin_cmd', "lock");
}

function unlock_chat() {
    socket.emit('admin_cmd', "unlock");
}*/
