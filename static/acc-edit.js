// this is needed, because we have to create the socket here, but not load chat.js (where the socket would be created originally)
// define socketio connection
const socket = io();
// here too cause why not

function login() {
    let loginuserElement = document.getElementById("user");
    let passwordElement = document.getElementById("pass");
    let loginuser = loginuserElement["value"];
    let passwd = passwordElement["value"];

    if (loginuser === "" || passwd === "") {
        return;
    } else {
        socket.emit('login', loginuser, passwd);
    }
}


socket.on("login_att", (state) => {
    if (state === 'true') {
        enteraccount();
    } else {
        failedlogin();
    }
});

socket.on("return_prefs", (Obj) => {
    if ('failed' in Obj) {
        // do something here to tell the user it failed, maybe retry?
        return;
    }
    // set values of localstorage vars here (and the other ones aswell)
    // window.localStorage.setItem("username", Obj["displayName"]);
    // window.localStorage.setItem("role", Obj["role"]);
    // window.localStorage.setItem("role_color", Obj["roleColor"]);
    // window.localStorage.setItem("user_color", Obj["userColor"]);
    // window.localStorage.setItem("message_color", Obj["messageColor"]);
    // window.localStorage.setItem("theme", Obj["theme"]);
    // window.localStorage.setItem("permission", Obj["permission"]);
    document.getElementById("Ausername")["value"] = document.getElementById("user")["value"];
    document.getElementById("Apassword")["value"] = ""
    document.getElementById("role_color")["value"] = Obj["roleColor"];
    document.getElementById("username")["value"] = Obj["displayName"]; 
    document.getElementById("role")["value"] = Obj["role"];
    document.getElementById("user_color")["value"] = Obj["userColor"];
    document.getElementById("message_color")["value"] = Obj["messageColor"];
});

function failedlogin() {
    let failedattempts = window.localStorage.getItem("login_att");
    if (failedattempts === "") {
        window.sessionStorage.setItem("login_att", "1");
        return;
    } else if (failedattempts === "1") {
        window.sessionStorage.setItem("login_att", "2");
        return;
    } else if (failedattempts === "2") {
        window.sessionStorage.setItem("login_att", "3");
        return;
    } else if (failedattempts === "3") {
        document.getElementById("loginStuff").style.display = "block";
        window.sessionStorage.setItem("login_att", "");
    }
}

// ea sports its in the game
//
function enteraccount() {
    document.getElementById("loginStuff").style.display = "none";
    document.getElementById("chatStuff").style.display = "block";
    document.getElementById("accountStuff").style.display = "block";
    socket.emit('get_prefs', document.getElementById("user")["value"]);
}

function logout() {
    document.getElementById("loginStuff").style.display = "block";
    document.getElementById("chatStuff").style.display = "none";
    document.getElementById("accountStuff").style.display = "none";
    let usernmElement = document.getElementById("user");
    let passwdElement = document.getElementById("pass");
    let roleElement = document.getElementById("role");
  
    window.localStorage.setItem("username", "");
    window.localStorage.setItem("role", "");
    window.localStorage.setItem("role_color", "#ffffff");
    window.localStorage.setItem("user_color", "#ffffff");
    window.localStorage.setItem("message_color", "#ffffff");
    window.localStorage.setItem("theme", 'dark');
    document.getElementById("role")["value"] = "";
    document.getElementById("user_color")["value"] = "#ffffff";
    document.getElementById("message_color")["value"] = "#ffffff";
    document.getElementById("username")["value"] = "";
    whichEvent("dark");
  
    usernmElement["value"] = "";
    passwdElement["value"] = "";
    roleElement["value"] = "";
    // location.reload();
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

    if (Apass === "") {
      let Apass = document.getElementById("pass")["value"];
    }
    
    socket.emit('update', Euser, Erole, Cmessage, Crole, Cuser, Auser, Apass, loginuser);
}