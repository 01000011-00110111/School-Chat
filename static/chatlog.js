// ran at startup so you get previous messages
function loadBackupChat(jsonString) {
    let newline = "<br>";
    // Get an object representing the div displaying the chat
    let chatDiv = document.getElementById("chat");
    let chat = "";
    let messages = JSON.parse(jsonString);
    // Loop through each message in the data sent from the server
    for (let messageObj of messages) {
        // Update our accumulator with the message's text
        chat = chat + messageObj["message"] + newline;
    }

    chatDiv["innerHTML"] = chat;
    window.scrollTo(0, document.body.scrollHeight);
}