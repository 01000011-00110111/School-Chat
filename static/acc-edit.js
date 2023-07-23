// define socketio connection
const socket = io();

function enteraccount() {
    document.getElementById("chatStuff").style.display = "block";
    document.getElementById("accountStuff").style.display = "block";
    socket.emit('get_prefs', document.getElementById("user")["value"]);
}

function update() {
    let loginuser = document.getElementById("user")["value"];
    let Euser = document.getElementById("username")["value"];
    let Erole = document.getElementById("role")["value"];
    let Cmessage = document.getElementById("message_color")["value"];
    let Crole = document.getElementById("role_color")["value"];
    let Cuser = document.getElementById("user_color")["value"];
    let Auser = document.getElementById("Ausername")["value"];
    let Apass = document.getElementById("Apassword")["value"];
    let cprofile = document.getElementById("profile")["value"];

    if (Apass === "") {
      let Apass = document.getElementById("pass")["value"];
    }
    
    socket.emit('update', Euser, Erole, Cmessage, Crole, Cuser, Auser, Apass, loginuser, cprofile);
}