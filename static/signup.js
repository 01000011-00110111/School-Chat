// this is needed, because we have to create the socket here, but not load chat.js (where the socket would be created originally)
// define socketio connection
const socket = io();

function signup() {
    let SUsername = document.getElementById("SUsername")['value'];
    let SDesplayname = document.getElementById("SDesplayname")['value'];
    let SPassword = document.getElementById("SPassword")['value'];
    let SPassword2 = document.getElementById("SPassword2")['value'];
    let SRole = document.getElementById("SRole")['value'];
    if (SRole === "" || SPassword === "" || SDesplayname === "" || SUsername === "" || SPassword2 === "") {
        return;
    } else {
        if (SPassword === SPassword2) {
            Sprofile = "";
            socket.emit('signup', SUsername, SDesplayname, SPassword, SRole, Sprofile);
            document.getElementById("SUsername")['value'] = "";
            document.getElementById("SDesplayname")['value'] = "";
            document.getElementById("SPassword")['value'] = "";
            document.getElementById("SPassword2")['value'] = "";
            document.getElementById("SRole")['value'] = "";
            window.localStorage.setItem("signup", "done")
        }
    }
}