// define socketio connection
const socket = io();

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

function loadChat() {
    ajaxGetRequest("/chat_logs", loadChatStartup); 
}

function runStartup() {
    loadChat();
    socket.emit("username", "Viewer");
}

function loadChatStartup(jsonString) {
    let newline = "<br>";
    let chatDiv = document.getElementById("chat");
    let chat = "";
    let messages = JSON.parse(jsonString);
    for (let messageObj of messages) {
        chat = chat + messageObj["message"] + newline;
    }

    chatDiv["innerHTML"] = chat;
    window.scrollTo(0, document.body.scrollHeight);
}

function renderChat(messages) {
    let newline = "<br>";
    let chatDiv = document.getElementById("chat");

    chatDiv["innerHTML"] = chatDiv["innerHTML"] + messages + newline;
    window.scrollTo(0, document.body.scrollHeight);
}
