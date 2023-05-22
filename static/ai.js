function sendMessageai() {
    let messageElement = document.getElementById("message");
    let message = messageElement["value"];
    let userElement = document.getElementById("username");
    let username = userElement["value"];
    messageElement["value"] = "";
    socket.emit('message_ai', message, username);
}

socket.on("ai_responce", (responce) => {
    renderChat(responce);
});

function renderChat(responce) {
    let newline = "<br>";
    let chatDiv = document.getElementById("chat");
    chatDiv["innerHTML"] = chatDiv["innerHTML"] + responce + newline;
}