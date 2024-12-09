const Chat_object = {
    messages: []
}

function loadChat(data) {
    Chat_object.messages = data
    console.log(data)
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
    // console.log(messages)
    let newline = "<br>";
    let chatDiv = document.getElementById("chat");
    chatDiv["innerHTML"] = chatDiv["innerHTML"] + renderMessage(message_data) + newline;
    // activate_hyperlinks();
}

function renderMessage(message_data) {
    // console.log(message_data)
    // console.log(messages)
    // let newline = "<br>";
    // let chatDiv = document.getElementById("chat");
    let badges = '';
    for (let i = 0; i < message_data["badges"].length; i++) {
        if (message_data["badges"][i] !== null) {
            badges += message_data["badges"][i];
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

export { Chat_object, renderChat, renderMessage, loadChat }