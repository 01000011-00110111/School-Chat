function pass() {
    ismutted = 'false'
    document.cookie = "permission=" + ismutted + "; path=/";
}

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
    } else {
        failedlogin();
    }
});

socket.on("return_prefs", (Obj) => {
    if ('failed' in Obj) {
        failedlogin();
    }
    window.localStorage.setItem("username", Obj["displayName"]);
    window.localStorage.setItem("pfp", Obj["profile"]);
    socket.emit("username_msg", Obj["displayName"]);
    whichEvent(Obj["theme"]);
    document.getElementById("pfpmenu").src = window.localStorage.getItem("pfp");
    runStartup();
});


socket.on("return_perms", (Dev, Mod, Edit, JOTD) => {
    SpecialMenu(Dev, Mod, Edit, JOTD);
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

        window.sessionStorage.setItem("login_att", "");
    }
}

function enteraccount() {
    socket.emit('get_prefs', document.getElementById("user")["value"]);
    socket.emit('get_perms');
    document.getElementById("LoginPopup").style.display = 'none';
}

function updateacc() {
    socket.emit('get_prefs', document.getElementById("user")["value"]);
    socket.emit('get_perms');
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
    document.getElementById("toprightD").style.display = "none";
    document.getElementById("toprightM").style.display = "none";
    document.getElementById("DevStuff").style.display = "none";
    document.getElementById("ModStuff").style.display = "none";
    document.getElementById("LoginPopup").style.display = 'block';
    document.getElementById("pfpmenu").src = "static/favicon.ico";
    devcloseNav();
    ModcloseNav();
    runCheckStartup();
    document.title = "OCD wleb Potato man Skill Issue!!!1!";
}

function SpecialMenu(Dev, Mod, Edit, JOTD) {
    let SPermission = window.sessionStorage.getItem("SPermission");
    let username = document.getElementById("user")["value"];
    if (SPermission === Dev) {
        document.title = "Class Chat Dev";
        document.getElementById("DevStuff").style.display = "block";
        document.getElementById("toprightD").style.display = "block";
        document.getElementById("toprightD").style.display = "block";
    } else if (SPermission === Mod) {
        document.title = "Class Chat Mod";
        document.getElementById("ModStuff").style.display = "block";
        document.getElementById("toprightM").style.display = "block"; 
    }
}