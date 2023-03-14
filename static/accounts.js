function pass() {
    ismutted = 'false'
    document.cookie = "permission=" + ismutted + "; path=/";
}

function login() {
    let loginuserElement = document.getElementById("user");
    let passwordElement = document.getElementById("pass");
    let loginuser = loginuserElement["value"];
    let passwd = passwordElement["value"]

    if (loginuser === "" || passwd === "") {
        return;
    }

    socket.emit('login', loginuser, passwd);
}


socket.on("login_att", (state) => {
    if (state === 'true') {
        enteraccount();
    } else {
        failedlogin();
    }
});

socket.on("return_prefs", (Obj) => {
    // must check if the dicgt only has a failed attempt thing first
    if ('failed' in Obj) {
        // do something here to tell the user it failed, maybe retry?
        return;
    }
    // set values of localstorage vars here
     window.localStorage.setItem("username", displayName);
     window.localStorage.setItem("role", role);
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
    socket.emit('fetch_prefs', document.getElementById("user")["value"]);
}


function logout() {
    document.getElementById("loginStuff").style.display = "block";
    document.getElementById("logoutStuff").style.display = "none";
    let passwdElement =  document.getElementById("user");
    let usernmElement =  document.getElementById("pass");
    let roleElement =  document.getElementById("role");

    usernmElement["value"] = "";
    passwdElement["value"] = "";
    roleElement["value"] = "";
    // location.reload();
}