function JsendMessage() {
    //let ismutted = getCookie("permission")

    //if (ismutted === 'false') {
    let messageElement = document.getElementById('jsendT');
    let toSend = "[Joke of the day]: <font color='#D51956'>" + messageElement.value + "</font>"
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
    socket.emit('message_chat', toSend);
}

function SOsendMessage() {
    let messageElement = document.getElementById('SOsendT');
    let toSend = "<font color='#08bd71'>[SONG]: " + messageElement.value + "</font>"
    messageElement.value = "";
    socket.emit('message_chat', toSend);
}

// see comment inside function    
function dummyajax(jsonData) {
    // dummy function so ajaxPostRequest doesent error out from no function callback
    return;
}