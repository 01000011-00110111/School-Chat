// define socketio connection
const socket = io();

function pass() {
    ismutted = 'false'
    document.cookie = "permission=" + ismutted + "; path=/";
}

function login() {
    let loginuserElement = document.getElementById("user");
    let passwordElement = document.getElementById("pass");
    let loginuser = loginuserElement["value"];
    let passwd = passwordElement["value"]

    socket.emit('login', loginuser, passwd);
}

//add start of socketio
socket.on("login2", (aproved) => {
  if (aproved === 'true') {
      enteraccount();
  } else {
      failedlogin();
  }
});

function failedlogin() {
    // sigh depression
}