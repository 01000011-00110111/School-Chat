  // mod menu js code to keep chat.js and dev-menu.js cleaner and easy to read and find what you need//

function banHammer() {
    socket.emit('admin_cmd', "ban")
}

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

// see comment inside function
function dummyajax(jsonData) {
    // dummy function so ajaxPostRequest doesent error out from no function callback
    return;
}
