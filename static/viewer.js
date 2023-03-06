// define socketio connection
const socket = io();

// add messages as they are recieved
socket.on("message_chat", (message) => {
    renderChat(message);
});

socket.on("reset_chat", (who) => {
    let chatDiv = document.getElementById("chat");
    if (who === "admin") {
        chatDiv["innerHTML"] = "[SYSTEM]: <font color='#ff7f00'>Chat reset by a admin.</font><br>"
    } else if (who === "auto") {
        chatDiv["innerHTML"] = "[SYSTEM]: <font color='#ff7f00'>Chat reset by automatic wipe system.</font><br>"
    }
});

socket.on("force_username", (statement) => {
    socket.emit("username", "Viewer");
});

socket.on("online", (db) => {
    let newline = "<br>"
    let online = "";
    let onlineDiv = document.getElementById("online_users");
    let online_count = 0
    for (onlineUser of db) {
        if (onlineUser === "cserverReal") {
            onlineUser = "cserver"
        } else if (onlineUser === null) {
            onlineUser = "Anonymous"
        } else if (onlineUser === "") {
            onlineUser = "Anonymous"
        } else if (onlineUser === "Dev EReal") {
            onlineUser = "Dev E"
        }
        online = online + onlineUser + newline;
        online_count++
    }
    let final_online = "<font size=5%>Online: " + online_count + "</font><br><br>" + online
    onlineDiv["innerHTML"] = final_online;
});

// This function requests the server send it a full chat log
function loadChat() {
    ajaxGetRequest("/chat", loadChatStartup); 
}

// stuff to run at startup and what happens when you do agree to the rules
function runStartup() {
    // load previous chat messages
    loadChat();
    socket.emit("username", "Viewer");
}

function runCheckReset(message) {
    console.log(message)
    if (message === "[SYSTEM]: <font color='#ff7f00'>Chat reset by a admin.</font>") {
        let chatDiv = document.getElementById("chat");
        console.log("here")
        chatDiv["innerHTML"] = "[SYSTEM]: <font color='#ff7f00'>Chat reset by a admin.</font><br>"
        console.log(message)
        return "true";
    } 
}

// ran at startup so you get previous messages
function loadChatStartup(jsonString) {
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

// This is the callback function used for both ajax requests
// It will be called by JS automatically whenever we get a response from the server
function renderChat(messages) {
    // Store the HTML needed to move to the next line. This makes the coding easier to read
    let newline = "<br>";
    // Get an object representing the div displaying the chat
    let chatDiv = document.getElementById("chat");

    chatDiv["innerHTML"] = chatDiv["innerHTML"] + messages + newline;
    window.scrollTo(0, document.body.scrollHeight);
}
