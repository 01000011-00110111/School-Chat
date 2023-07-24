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
        socket.emit('get_prefs', document.getElementById("user")["value"]);
        // enteraccount();
    }
});

socket.on("return_prefs", (Obj) => {
    if ('failed' in Obj) {
        console.log('We need a failed to grab function')
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

// function enteraccount() { do we want to keep this?
//     socket.emit('get_prefs', document.getElementById("user")["value"]);
// }
