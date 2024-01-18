// Copyright (C) 2023  cserver45, cseven
// License info can be viewed in main.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat

// define socketio connection
const socket = io();

socket.on("online", (db) => {
    // let newline = "<br>"
    let online = "";
    let onlineDiv = document.getElementById("online_users");
    let online_count = db.length;
    
    for (onlineUser of db) {
        online = `${online}<button id="online_buttons" onclick="openuserinfo('${onlineUser[1]}')">${onlineUser[0]}${onlineUser[1]}</button><br>`
        // online = online + '<button id="online_buttons" onclick="openuserinfo(\'' + onlineUser[1] + '\')">' + onlineUser[0] + onlineUser[1] + '</button>' + newline;
        // online = online + `<a onclick="openuserinfo('${onlineUser}')">${onlineUser}</a><br>`;
    }
    
    let final_online = "<font size=5%>Online: " + online_count + "</font><br><br>" + online;
    onlineDiv.innerHTML = final_online;
});


// it returns from the dead!
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
