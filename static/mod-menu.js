// mod menu js code to keep chat.js and dev-menu.js cleaner and easy to read and find what you need//

function FsendMessageM() {
    let messageElement = document.getElementById('fsendTM');
    // 100% CPU usage lol on tablet lol
    //console.log(document.getElementById("user_name"));
    let toSend = "[Mod]: " + messageElement.value

    messageElement.value = "";
    // we use a diffrent endpoint, so it doesen't get blocked by the add_message function on the server end
    // also gets rid of a lot of checks inside add_message
    socket.emit('admin_message', toSend);
} 

function banHammer() {
    let muteuserElement = document.getElementById("muteuserboxM");
    let userElement = document.getElementById("user");
    let mute_user_name = muteuserElement["value"];
    let user_name = userElement["value"];
        
    if (mute_user_name === "Dev E") {
        mute_user_name = user_name
    } else if (mute_user_name === "cserver") {
        mute_user_name = user_name
    } else if (mute_user_name === "Steven") {
        mute_user_name = "STEVEN Payed a box of poptarts and gummys for immunity"
    }
    
    socket.emit('ban_cmd', mute_user_name)
}

function mute() {
    let muteuserElement = document.getElementById("muteuserboxM");
    let userElement = document.getElementById("user");
    let mute_user_name = muteuserElement["value"];
    let user_name = userElement["value"];

    if (mute_user_name === "Dev E") {
        mute_user_name = user_name
    } else if (mute_user_name === "cserver") {
        mute_user_name = user_name
    } else if (mute_user_name === "Steven") {
        mute_user_name = "STEVEN Payed a box of poptarts and gummys for immunity"
    }
    
    socket.emit('mute_cmd', mute_user_name)
}

function unmute() {
    let muteuserElement = document.getElementById("muteuserboxM");
    let mute_user_name = muteuserElement["value"];
    socket.emit('unmute_cmd', mute_user_name)
}

// get stats from the replit instance
function getStats() {
    socket.emit('admin_cmd', "full_status");
}

function reset_chat() {
    socket.emit("admin_cmd", "reset_chat");
}

function lock_chat() {
    socket.emit('admin_cmd', "lock");
}

/*// unlocks chat
function unlock_chat() {
    socket.emit('admin_cmd', "unlock");
}*/
