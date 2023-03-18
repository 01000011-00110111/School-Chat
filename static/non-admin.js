function JsendMessage() {
    //let ismutted = getCookie("permission")

    //if (ismutted === 'false') {
    let message = document.getElementById('jsendT').value;
    let toSend = "[Joke of the day]: <font color='#D51956'>" + message + "</font>"
    messageElement.value = "";
    /* } else if (ismutted === 'banned') {
        let messageElement = document.getElementById('jsendT');
        let toSend = "[shayla is never banned]: <font color='#19d784'>" + messageElement.value + "</font>"
        messageElement.value = "";
    } else if (ismutted === 'true') {
        let messageElement = document.getElementById('jsendT');
        let toSend = "[shayla is never mutted]: <font color='#19d784'>" + messageElement.value + "</font>"
        messageElement.value = "";
    } */
    socket.emit('message_chat', "", "[Joke of the day]: ", "", "", message, "#D51956", "");
}

function SOsendMessage() {
    let messageElement = document.getElementById('SOsendT');
    let toSend = "<font color='#08bd71'>[SONG]: " + messageElement.value + "</font>"
    messageElement.value = "";
    socket.emit('message_chat', toSend);
}

// take a img url, and convert it into a img html tag
function sendImage() {
    let messageElement = document.getElementById("sendimgT");
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