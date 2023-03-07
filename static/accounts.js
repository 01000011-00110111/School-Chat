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
      enteraccount(accid);
  } else {
      failedlogin();
  }
});

function failedlogin() {
    if (failedattempts = "") {
      let failedattempts = "1" 
    }else if (failedattempts = "1") {
      let failedattempts = "2" 
    } else if (failedattempts = "2") {
      let failedattempts = "3" 
    } else if (failedattempts = "3") {
      window.refresh()
    }
}

function enteraccount(accid) {
  // oneday will have somting here  
}