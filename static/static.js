// Copyright (C) 2023  cserver45, cseven
// License info can be viewed in main.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat

// define socketio connection
const socket = io();

socket.on("online", (db) => {
    let newline = "<br>"
    let online = "";
    let onlinels = '';
    let onlineDiv = document.getElementById("online_users");
    // let onlinelsDiv = document.getElementById("onlinels");
    let online_count = db.length;
    for (onlineUser of db) {
        online = online + onlineUser + newline;
        onlinels = onlinels + `<a onclick="openuserinfo(${onlineUser})>` + onlineUser + '</a>';
    }
    let final_online = "<font size=5%>Online: " + online_count + "</font><br><br>" + online;
    // onlinelsDiv["innerHTML"] = onlinels;
    onlineDiv["innerHTML"] = final_online;
});