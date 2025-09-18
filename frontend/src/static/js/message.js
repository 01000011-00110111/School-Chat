// Copyright (C) 2023-2025  cserver45, cseven, CastyiGlitchxz
// License info can be viewed in app.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat
function loadChat(data) {
    let newline = "<br>";
    let chatDiv = document.getElementById("chat");
    chatDiv["innerHTML"] = "";
    let msgs = ""; 
    for (let messageObj of data) {
        let message = renderMessage(messageObj);
        msgs += message + newline;
    }
    chatDiv["innerHTML"] = msgs;
    window.scrollTo(0, chatDiv.scrollHeight);
}

function renderChat(message_data) {
    let newline = "<br>";
    let chatDiv = document.getElementById("chat");
    chatDiv["innerHTML"] = chatDiv["innerHTML"] + renderMessage(message_data) + newline;
    chatDiv.scrollTop = chatDiv.scrollHeight;
    // activate_hyperlinks();
}

/**
 * This function converts HTML tags into plain text, HTML will not be display in chat using this method.
 * @param {*} input 
 * @returns 
 */
function escapeHTML(input) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;'
    };
    return input.replace(/[&<>"']/g, function(match) {
        return map[match];
    });
}

function renderMessage(message_data) {
    let badges = message_data.badges || [];

    return `
        <div class='user_message'> 
        <div class='message_image_container'>${message_data["profile"]}</div>
        <div class='message_info'>
        <div class='message_info_container'>${message_data["user"]}<p>*</p>
        <p>${message_data["date"]}</p>
        ${badges}
        </div>
        <div class='message_content_container'>${message_data["message"]}</div> </div>
        </div>
    `
}

export { renderChat, renderMessage, loadChat }