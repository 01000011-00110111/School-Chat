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
    console.log(message_data);
    let badges = message_data.badges || [];
    for (let i = 0; i < message_data.badges.length; i++) {
        console.log(message_data.badges, badges)
        if (message_data.badges[i] !== null || message_data.badges[i] !== undefined) {
            badges += message_data.badges[i];
        }
    }

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