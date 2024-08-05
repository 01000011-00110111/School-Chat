// Copyright (C) 2023  cserver45, cseven
// License info can be viewed in main.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat


socket.on('load_chunk', (messages) => {
    let newline = "<br>";
    let chatDiv = document.getElementById("chat");
    let chat = "";
    for (let message of messages) {
        chat += message + newline;
    }
    chatDiv.innerHTML = chat;
    window.scrollTo(0, document.body.scrollHeight);
});

function loadPrevious() {
    socket.emit('change_chunk', 'prev');
}

function loadNext() {
    socket.emit('change_chunk', 'next');
}

function resetPosition() {
    socket.emit('change_chunk', 'reset');
}