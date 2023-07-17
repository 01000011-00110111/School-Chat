function login() {
    let loginuserElement = document.getElementById("user");
    let passwordElement = document.getElementById("pass");
    let loginuser = loginuserElement["value"];
    let passwd = passwordElement["value"];
    let tosch = document.getElementById("tosCH");

    if (loginuser === "" || passwd === "" || tosch.checked == false) {
        return;
    } else {
        socket.emit('login', loginuser, passwd);
    }
}


socket.on("login_att", (state) => {
    if (state === 'true') {
        enteraccount();
    }
});

socket.on("return_prefs", (Obj) => {
    if ('failed' in Obj) {
        console.log('We need a failed login function')
    }
    window.localStorage.setItem("username", Obj["displayName"]);
    window.localStorage.setItem("pfp", Obj["profile"]);
    socket.emit("username_msg", Obj["displayName"]);
    whichEvent(Obj["theme"]);
    let pfp = document.getElementById("pfpmenu");
    let picture = window.localStorage.getItem("pfp");
    if (picture === '') {
        pfp.src = 'static/favicon.ico';
    } else {
        pfp.src = picture;
    }
});

function enteraccount() {
    socket.emit('get_prefs', document.getElementById("user")["value"]);
    document.getElementById("LoginPopup").style.display = 'none';
}

function logout() {
    let chatDiv = document.getElementById("chat");
    let usernmElement = document.getElementById("user");
    let passwdElement = document.getElementById("pass");
    let tosch = document.getElementById("tosCH");
    chatDiv["innerHTML"] = '';
    window.scrollTo(0, document.body.scrollHeight);
    passwdElement["value"] = '';
    usernmElement["value"] = '';
    document.getElementById("pfpmenu").src = "static/favicon.ico";
    runCheckStartup();
}
