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
        // do something here to tell the user it failed, maybe retry?
        return;
    }
    // set values of localstorage vars here (and the other ones aswell)
    window.localStorage.setItem("username", Obj["displayName"]);
    window.localStorage.setItem("role", Obj["role"]);
    window.localStorage.setItem("role_color", Obj["roleColor"]);
    window.localStorage.setItem("user_color", Obj["userColor"]);
    window.localStorage.setItem("message_color", Obj["messageColor"]);
    window.localStorage.setItem("theme", Obj["theme"]);
    window.localStorage.setItem("permission", Obj["permission"]);
    document.getElementById("role_color")["value"] = Obj["roleColor"];
    document.getElementById("username")["value"] = Obj["displayName"]; 
    document.getElementById("role")["value"] = Obj["role"];
    document.getElementById("user_color")["value"] = Obj["userColor"];
    document.getElementById("message_color")["value"] = Obj["messageColor"];
    SPermission = Obj["SPermission"]
    SpecialMenu(SPermission);
    // set online user
    socket.emit("username_msg", Obj["displayName"]);
    // call the finction to change themes
    whichEvent(Obj["theme"]);
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
    document.getElementById("logoutStuff").style.display = "block";
    socket.emit('get_prefs', document.getElementById("user")["value"]);
}

function updateacc() {
    socket.emit('get_prefs', document.getElementById("user")["value"]);
}


function logout() {
    document.getElementById("loginStuff").style.display = "block";
    document.getElementById("logoutStuff").style.display = "none";
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
    socket.emit("username_msg", "");
    // needed to ensure the menu disappears after logout
    document.getElementById("toprightE").style.display = "none";
    document.getElementById("toprightD").style.display = "none";
    document.getElementById("toprightM").style.display = "none";
    document.getElementById("toprightJ").style.display = "none";
    document.getElementById("DevStuff").style.display = "none";
    document.getElementById("ModStuff").style.display = "none";
    document.getElementById("EditorStuff").style.display = "none";// need to hide the menu's
    document.getElementById("JOTDStuff").style.display = "block";
    devcloseNav();
    EditcloseNav();
    JOTDcloseNav();
    ModcloseNav();
    document.title = "OCD wleb Potato man Skill Issue!!!1!";
    // location.reload();
}

function SpecialMenu(SPermission) {
    // let username = document.getElementById("user")["value"];
    // later I should just make the server respond with the menu that needs to be loaded, so it responds to login changes, but this works for now
    if (SPermission === "Dev") {
        document.title = "Class Chat Dev";
        // yep something along the lines of what I was going to do
        const script = document.createElement('script');
        script.src = 'static/dev-menus.js';
        script.type = 'text/javascript';
        document.body.appendChild(script);
        document.getElementById("DevStuff").style.display = "block";
        document.getElementById("toprightD").style.display = "block";
    } else if (SPermission === "Mod") {
        document.title = "Class Chat Mod";
        const script = document.createElement('script');
        script.src = 'static/mod-menu.js';
        script.type = 'text/javascript';
        document.body.appendChild(script);
        document.getElementById("ModStuff").style.display = "block";
        document.getElementById("toprightM").style.display = "block"; 
    } else if (SPermission === "JOTD") {
        document.title = "Class Chat JOTD";
        document.getElementById("toprightJ").style.display = "block";
        document.getElementById("JOTDStuff").style.display = "block";
    } else if (SPermission === "Editor") {
        // so owen is not mad
        document.title = "Desmos | Graphing Calculator";
        document.querySelector("link[rel='shortcut icon']").href = "https://help.desmos.com/hc/en-us/article_attachments/4413863846413/desmos_icon_square.png";
        // document.querySelector("link[rel*='icon']").href = "https://help.desmos.com/hc/en-us/article_attachments/4413863846413/desmos_icon_square.png";
        document.getElementById("toprightE").style.display = "block";
        document.getElementById("EditorStuff").style.display = "block";
    }
}