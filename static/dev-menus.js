  // Dev menu js code to keep chat.js cleaner and easy to read and find what you need//

function systemmessage() {
    user = document.getElementById("user")["value"];
    if (user === "C7" || user === "cserverReal") {
        let messageElement = document.getElementById("systemsendT");

        message = '<font color="#ff7f00">' + messageElement["value"] + '</font>'
        messageElement["value"] = "";
        let toSend = "[SYSTEM]: " + message
        socket.emit('admin_message', toSend)
    }
}

function reloadiframe() {
    user = document.getElementById("user")["value"];
    if (user === "C7" || user === "cserverReal") {
        document.getElementById('dev_chat_iframe').src += ''; 
    }
}

function reloadPages() {
    user = document.getElementById("user")["value"];
    if (user === "C7" || user === "cserverReal") {
        let muteuserElement = document.getElementById("muteuserbox");
        let mute_user_name = muteuserElement["value"];
    
        if (mute_user_name === "Dev EReal") {
            mute_user_name = "Dev E"
        } else if (mute_user_name === "cserverReal") {
            mute_user_name = "cserver"
        }
        
        socket.emit('reload_page', mute_user_name)
    }
}

function banHammer() {
    user = document.getElementById("user")["value"];
    if (user === "C7" || user === "cserverReal") {
        let muteuserElement = document.getElementById("muteuserbox");
        let mute_user_name = muteuserElement["value"];
    
        if (mute_user_name === "Dev EReal") {
            mute_user_name = "Dev EReal"
        } else if (mute_user_name === "cserverReal") {
            mute_user_name = "cserver"
        } else if (mute_user_name === "Steven") {
            mute_user_name = "STEVEN Payed a box of poptarts and gummys for immunity"
        }
        
        socket.emit('ban_cmd', mute_user_name)
    }
}

function mute() {
    user = document.getElementById("user")["value"];
    if (user === "C7" || user === "cserverReal") {
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
}

function unmute() {
    user = document.getElementById("user")["value"];
    if (user === "C7" || user === "cserverReal") {
        let muteuserElement = document.getElementById("muteuserbox");
        let mute_user_name = muteuserElement["value"];
        socket.emit('unmute_cmd', mute_user_name)
    }
}

function urlsend() {
    user = document.getElementById("user")["value"];
    if (user === "C7" || user === "cserverReal") {
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
}

function FsendMessageA() {
    user = document.getElementById("user")["value"];
    if (user === "C7" || user === "cserverReal") {
        let messageElement = document.getElementById('fsendT');
        // 100% CPU usage lol on tablet lol
        //console.log(document.getElementById("user_name"));
        let toSend = "[Admin]: " + messageElement.value
    
        messageElement.value = "";
        socket.emit('admin_message', toSend);
    }
} 

function FsendMessageM() {
    user = document.getElementById("user")["value"];
    if (user === "C7" || user === "cserverReal") {
        let messageElement = document.getElementById('fsendT');
        // 100% CPU usage lol on tablet lol
        //console.log(document.getElementById("user_name"));
        let toSend = "[Mod]: " + messageElement.value
    
        messageElement.value = "";
        socket.emit('admin_message', toSend);
    }
} 

function testChatGC() {
    user = document.getElementById("user")["value"];
    if (user === "C7" || user === "cserverReal") {
        socket.emit('admin_cmd', "blanks");
    }
}

function EsendMessage() {
    user = document.getElementById("user")["value"];
    if (user === "C7" || user === "cserverReal") {
        let messageElement = document.getElementById("EventMSGT");
    
        message = '<font color="e54e40">' + messageElement["value"] + '</font>' + "</h3>"
        messageElement["value"] = "";
        let toSend = "<h3> [Event]: " + message + "</h3>"
        socket.emit('admin_message', toSend);
    }
}

function getStats() {
    user = document.getElementById("user")["value"];
    if (user === "C7" || user === "cserverReal") {
        socket.emit('admin_cmd', "full_status");
    }
}

function clearDB() {
    user = document.getElementById("user")["value"];
    if (user === "C7" || user === "cserverReal") {
        socket.emit('admin_cmd', "username_clear");
    }
}

function reset_chat() {
    user = document.getElementById("user")["value"];
    if (user === "C7" || user === "cserverReal") {
        socket.emit("admin_cmd", "reset_chat");
    }
}

function lock_chat() {
    user = document.getElementById("user")["value"];
    if (user === "C7" || user === "cserverReal") {
        socket.emit('admin_cmd', "lock");
    }
}

function unlock_chat() {
    user = document.getElementById("user")["value"];
    if (user === "C7" || user === "cserverReal") {
        socket.emit('admin_cmd', "unlock");
    }
}
