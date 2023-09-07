// Copyright (C) 2023  cserver45, cseven
// License info can be viewed in main.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat


function ProfilesB() {
    let Profileactive = window.localStorage.getItem("Profileactive");
    let Pbutton = document.getElementById("pfpbtn");
    if (Profileactive === "true") {
        let element = document.getElementsByClassName("pfp");
        for(var i = 0; i < element.length; i++) {
            element[i].style.display = 'none';
        }
        document.getElementById("chat").style.lineheight = "32px";
        window.localStorage.setItem("Profileactive", "false");
        Pbutton.value = "Enable profile pictures";
        Pbutton.style.backgroundColor = "green";
    } else {
        let element = document.getElementsByClassName("pfp");
        for(var i = 0; i < element.length; i++) {
            element[i].style.display = '';
        }
        document.getElementById("chat").style.lineheight = "40px";
        window.localStorage.setItem("Profileactive", "true");
        Pbutton.value = "Disable profile pictures";
        Pbutton.style.backgroundColor = "red";
    }
}

// for event theme
// set what event is currently being used
function whichEvent(event = "test") {
    // SET WHAT EVENT IS HAPPENING HERE
    // MUST BE ALL LOWERCASE TO WORK

    // if statement to cycle thru diffrent event functions
    if (event === "christmas") {
        setChristmasTheme();
    } else if (event === "dark") {
        setDarkStyle();
    } else if (event === "light") {
        setLightStyle();
    } else if (event === "") {
        whichEvent();
    } else if (event === "dev") {
        setDevStyle();
    } else if (event === "4th") {
        set4thStyle();
    } else if (event === "ogdev") {
        setOgDevStyle();
    }
}
  
// sets theme to dark mode
function setDarkStyle() {
    // get all id tags
    let body = document.getElementsByTagName("body")[0]; 
    let chat = document.getElementById("chat");
    let message = document.getElementById("message");
    let chatbox = document.getElementById("chatbox");
    let sides = document.getElementById("sides");
    let topleft = document.getElementById("topleft");
    let send = document.getElementById("send");
    let sidebar = document.getElementById("activenav");
    let sidenav = document.getElementById("mySidenav");
    let snav_text = sidenav.getElementsByTagName("a");
    let snav_iter = snav_text.length;
    // then set the color to what it is in the css document
    body.style.backgroundColor = "#000000";
    chat.style.color = "#ffffff";
    message.style.color = "#000000";
    chatbox.style.backgroundColor = "#181616";
    sides.style.backgroundColor = "#121212";
    sidebar.style.backgroundColor = "#171717";
    topleft.style.backgroundColor = "#f5f2f2";
    topleft.style.color = "#192080";
    send.style.backgroundColor = "#192080";
    send.style.color = "#ffffff";
    sidenav.style.backgroundColor = "#111";
    // for loop to cycle thru links in sidebar
    for (let i = 0; i < snav_iter; i++) {
        snav_text[i].style.color = "#818181";
    }
}

function setLightstyle() {
    // get all id tags
    let body = document.getElementsByTagName("body")[0]; 
    let chat = document.getElementById("chat");
    let message = document.getElementById("message");
    let chatbox = document.getElementById("chatbox");
    let sides = document.getElementById("sides");
    let topleft = document.getElementById("topleft");
    let send = document.getElementById("send");
    let sidebar = document.getElementById("activenav");
    let sidenav = document.getElementsByClassName("sidenav")[0];
    let snav_text = sidenav.getElementsByTagName("a");
    let snav_iter = snav_text.length;
    // then set the color to what it is in the css document
    body.style.backgroundColor = "#c0bfbc";
    chat.style.color = "#000000";
    message.style.color = "#000000";
    chatbox.style.backgroundColor = "#deddda";
    sides.style.backgroundColor = "#c0bfbc";
    sidebar.style.backgroundColor = "#000000";
    topleft.style.backgroundColor = "#5A5A5A";
    topleft.style.color = "#1b0670";
    send.style.backgroundColor = "#3daec4";
    send.style.color = "#33575e";
    sidenav.style.backgroundColor = "#b9c6c9";
    // for loop to cycle thru links in sidebar
    for (let i = 0; i < snav_iter; i++) {
        snav_text[i].style.color = "#192080";
    }
}


function set4thStyle() {
    // get all id tags
    let body = document.getElementsByTagName("body")[0]; 
    let chat = document.getElementById("chat");
    let message = document.getElementById("message");
    let chatbox = document.getElementById("chatbox");
    let sides = document.getElementById("sides");
    let topleft = document.getElementById("topleft");
    let send = document.getElementById("send");
    let sidebar = document.getElementById("activenav");
    let sidenav = document.getElementsByClassName("sidenav")[0];
    let snav_text = sidenav.getElementsByTagName("a");
    let snav_iter = snav_text.length;
    // then set the color to what it is in the css document
    body.style.backgroundColor = "#cfcfcf";
    chat.style.color = "#926f03";
    message.style.color = "#000000";
    chatbox.style.backgroundColor = "#d4d4d4";
    sides.style.backgroundColor = "#0909ff";
    sidebar.style.backgroundColor ="#0000e6";
    topleft.style.backgroundColor = "#d4d4d4";
    topleft.style.color = "#930000";
    send.style.backgroundColor = "#ff0000";
    send.style.color = "#ffffff";
    sidenav.style.backgroundColor = "#550000";
    // for loop to cycle thru links in sidebar
    for (let i = 0; i < snav_iter; i++) {
    snav_text[i].style.color = "#ffffff";
    }
}



function setOgDevStyle() {
    // get all id tags
    let body = document.getElementsByTagName("body")[0]; 
    let chat = document.getElementById("chat");
    let message = document.getElementById("message");
    let chatbox = document.getElementById("chatbox");
    let sides = document.getElementById("sides");
    let topleft = document.getElementById("topleft");
    let send = document.getElementById("send");
    let sidebar = document.getElementById("activenav");
    let sidenav = document.getElementsByClassName("sidenav")[0]
    let snav_text = sidenav.getElementsByTagName("a")
    let snav_iter = snav_text.length;
    // then set the color to what it is in the css document
    body.style.backgroundColor = "#000000";
    chat.style.color = "#228e3d";
    message.style.color = "#000000";
    chatbox.style.backgroundColor = "#181616";
    sides.style.backgroundColor = "#121212";
    sidebar.style.backgroundColor = "#171717"
    sidebar.style.color = "#ffffff"
    topleft.style.backgroundColor = "#121212";
    topleft.style.color = "#696969";
    send.style.backgroundColor = "#192080";
    send.style.color = "#ffffff";
    sidenav.style.backgroundColor = "#111";
    // for loop to cycle thru links in sidebar
    for (let i = 0; i < snav_iter; i++) {
        snav_text[i].style.color = "#818181";
    }
}

function setDevStyle() {
    // get all id tags
    let body = document.getElementsByTagName("body")[0]; 
    let chat = document.getElementById("chat");
    let message = document.getElementById("message");
    let chatbox = document.getElementById("chatbox");
    let sides = document.getElementById("sides");
    let topleft = document.getElementById("topleft");
    let send = document.getElementById("send");
    let sidebar = document.getElementById("activenav");
    let sidenav = document.getElementsByClassName("sidenav")[0];
    let snav_text = sidenav.getElementsByTagName("a");
    let snav_iter = snav_text.length;
    // then set the color to what it is in the css document
    body.style.backgroundColor = "#000000";
    chat.style.color = "#18691f";
    message.style.color = "#000000";
    chatbox.style.backgroundColor = "#0d0d0d";
    sides.style.backgroundColor = "#080808";
    sidebar.style.backgroundColor ="#080808";
    topleft.style.backgroundColor = "#0d0d0d";
    topleft.style.color = "#ffffff";
    send.style.backgroundColor = "#006600";
    send.style.color = "#ffffff";
    sidenav.style.backgroundColor = "#0f0f0f";
    // for loop to cycle thru links in sidebar
    for (let i = 0; i < snav_iter; i++) {
        snav_text[i].style.color = "#8a4e11";
    }
}