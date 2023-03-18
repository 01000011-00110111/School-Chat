// this is needed, because we have to create the socket here, but not load chat.js (where the socket would be created originally)
// define socketio connection
const socket = io();

// and now the signup code

function signup() {
    SUsername = document.getElementById("SUsername")['value'];
    SDesplayname = document.getElementById("SDesplayname")['value'];
    SPassword = document.getElementById("SPassword")['value'];
    SPassword2 = document.getElementById("SPassword 2nd time")['value'];
    SRole = document.getElementById("SRole")['value'];
    if (SRole === "" || SPassword === "" || SDesplayname === "" || SUsername === "") {
        return;
    } else {
        if (SPassword === SPassword2) {
            socket.emit('signup', SUsername, SDesplayname, SPassword, SRole);
            document.getElementById("SUsername")['value'] = "";
            document.getElementById("SDesplayname")['value'] = "";
            document.getElementById("SPassword")['value'] = "";
            document.getElementById("SPassword 2nd time")['value'] = "";
            document.getElementById("SRole")['value'] = "";
        }
    }
}