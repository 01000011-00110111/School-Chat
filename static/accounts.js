function pass() {
    ismutted = 'false'
    document.cookie = "permission=" + ismutted + "; path=/";
}

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
        failedlogin();
    }
    window.localStorage.setItem("username", Obj["displayName"]);
    window.localStorage.setItem("role", Obj["role"]);
    window.localStorage.setItem("theme", Obj["theme"]);
    window.localStorage.setItem("permission", Obj["permission"]);
    window.localStorage.setItem("profile_picture",Obj["profile"]);
    document.getElementById("username")["value"] = Obj["displayName"]; 
    document.getElementById("role")["value"] = Obj["role"];
    document.getElementById("profile_picture")["value"] = Obj["profile"];
    window.sessionStorage.setItem("SPermission", Obj["SPermission"]);
    socket.emit("username_msg", Obj["displayName"]);
    whichEvent(Obj["theme"]);
    ProfilesE();
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
        document.getElementById("loginStuff").style.display = "block";
        window.sessionStorage.setItem("login_att", "");
    }
}

function enteraccount() {
    document.getElementById("loginStuff").style.display = "none";
    document.getElementById("logoutStuff").style.display = "block";
    socket.emit('get_prefs', document.getElementById("user")["value"]);
    socket.emit('get_perms');
}

function updateacc() {
    socket.emit('get_prefs', document.getElementById("user")["value"]);
    socket.emit('get_perms');
}


function logout() {
    document.getElementById("loginStuff").style.display = "block";
    document.getElementById("logoutStuff").style.display = "none";
    let usernmElement = document.getElementById("user");
    let passwdElement = document.getElementById("pass");
    let roleElement = document.getElementById("role");
  
    window.localStorage.setItem("username", "");
    window.localStorage.setItem("role", "");
    window.localStorage.setItem("theme", 'dark');
    document.getElementById("role")["value"] = "";
    document.getElementById("username")["value"] = "";
    document.getElementById("profile_picture")["value"] = "";
    whichEvent("dark");
  
    usernmElement["value"] = "";
    passwdElement["value"] = "";
    roleElement["value"] = "";
    socket.emit("username_msg", "");
    document.getElementById("toprightE").style.display = "none";
    document.getElementById("toprightD").style.display = "none";
    document.getElementById("toprightM").style.display = "none";
    document.getElementById("toprightJ").style.display = "none";
    document.getElementById("DevStuff").style.display = "none";
    document.getElementById("ModStuff").style.display = "none";
    document.getElementById("EditorStuff").style.display = "none";
    document.getElementById("JOTDStuff").style.display = "none";
    devcloseNav();
    EditcloseNav();
    JOTDcloseNav();
    ModcloseNav();
    document.title = "OCD wleb Potato man Skill Issue!!!1!";
}

function SpecialMenu(Dev, Mod, Edit, JOTD) {
    let SPermission = window.sessionStorage.getItem("SPermission");
    let username = document.getElementById("user")["value"];
    if (SPermission === Dev) {
        document.title = "Class Chat Dev is down for now!!";
        document.getElementById("DevStuff").style.display = "block";
        document.getElementById("toprightD").style.display = "block";
        document.getElementById("toprightD").style.display = "block";
    } else if (SPermission === Mod) {
        document.title = "Class Chat Mod";
        document.getElementById("ModStuff").style.display = "block";
        document.getElementById("toprightM").style.display = "block"; 
    } else if (SPermission === JOTD) {
        document.title = "Class Chat JOTD";
        document.getElementById("toprightJ").style.display = "block";
        document.getElementById("JOTDStuff").style.display = "block";
    } else if (SPermission === Edit) {
        document.title = "Desmos | Graphing Calculator";
        document.getElementById("toprightE").style.display = "block";
        document.getElementById("EditorStuff").style.display = "block";
    }
}