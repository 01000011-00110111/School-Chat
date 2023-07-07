// set the theme
function setTheme(theme) {
    // set theme when button is pressed
    // other style function will change this, not directly called
    window.localStorage.setItem("theme", theme);
}

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
    } else if (event === "thanks") {
        setThanksTheme();
    } else if (event === "hollow") {
        setHollowTheme();
    } else if (event === "newyears") {
        setNewyearsTheme();
    } else if (event === "") {
        whichEvent();
    } else if (event === "special1") {
        setSpecalStyle();
    } else if (event === "valstyle") {
         valstyle();
    } else if (event === "dev") {
        setDevStyle();
    } else if (event === "A1st") {
        A1st();
    } else if (event === "WKfix") {
        webkitAnimationfix();
    } else if (event === "testing2") {
        setTestingStyle2();
    } else if (event === "testing3") {
        setTestingStyle3();
    } else if (event === "testing4") {
        setTestingStyle4();
    } else if (event === "4th") {
        set4thStyle();
    } else if (event === "test") {
        setTestStyle();
    } else if (event === "ogdev") {
        setOgDevStyle();
    }
}
  
// sets theme to dark mode
function setDarkStyle() {
    // set theme in cookie
    setTheme("dark");
    // get all id tags
    let body = document.getElementById("body");
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

function setLightStyle() {
    // set theme in cookie    
    setTheme("light");
    // get all id tags
    let body = document.getElementById("body");
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
    body.style.backgroundColor = "#ffffff";
    chat.style.color = "#000000";
    message.style.color = "#000000";
    chatbox.style.backgroundColor = "#deddda";
    sides.style.backgroundColor = "#c0bfbc";
    sidebar.style.backgroundColor = "#171717";
    topleft.style.backgroundColor = "#5A5A5A";
    topleft.style.color = "#1b0670";
    send.style.backgroundColor = "#192080";
    send.style.color = "#ffffff";
    sidenav.style.backgroundColor = "#b9c6c9";
    // for loop to cycle thru links in sidebar
    for (let i = 0; i < snav_iter; i++) {
        snav_text[i].style.color = "#192080";
    }
}

// never gonna give you up never gonna let you down
/*
We're no strangers to love
You know the rules and so do I (do I)
A full commitment's what I'm thinking of
You wouldn't get this from any other guy
I just wanna tell you how I'm feeling
Gotta make you understand
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
We've known each other for so long
Your heart's been aching, but you're too shy to say it (say it)
Inside, we both know what's been going on (going on)
We know the game and we're gonna play it
And if you ask me how I'm feeling
Don't tell me you're too blind to see
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
We've known each other for so long
Your heart's been aching, but you're too shy to say it (to say it)
Inside, we both know what's been going on (going on)
We know the game and we're gonna play it
I just wanna tell you how I'm feeling
Gotta make you understand
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
*/
// event themes after here

function set4thStyle() {
    // set theme in cookie
    setTheme('4th');
    // get all id tags
    let body = document.getElementById("body");
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
    // set theme in cookie
    setTheme("ogdev");
    // get all id tags
    let body = document.getElementById("body");
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
    // set theme in cookie
    setTheme("dev");
    // get all id tags
    let body = document.getElementById("body");
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




function A1st() {
    // set theme in cookie
    setTheme("A1st");
    // get all id tags
    let body = document.getElementById("body");
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
    body.style.webkitAnimation = "rainbowb 5s infinite";
    chat.style.color = "#ffffff";
    message.style.color = "#000000";
    chatbox.style.webkitAnimation = "rainbowb 5s infinite";
    sides.style.webkitAnimation = "rainbowb 5s infinite";
    sidebar.style.webkitAnimation = "rainbowb 5s infinite";
    topleft.style.webkitAnimation = "rainbowb 5s infinite";
    topleft.style.color = "#192080";
    send.style.webkitAnimation = "rainbowb 5s infinite";
    send.style.color = "#ffffff";
    sidenav.style.webkitAnimation = "rainbowb 5s infinite";
    // for loop to cycle thru links in sidebar
    for (let i = 0; i < snav_iter; i++) {
        snav_text[i].style.color = "#818181";
    }
}


function webkitAnimationfix() {
    // set theme in cookie
    setTheme("WKfix");
    // get all id tags
    let body = document.getElementById("body");
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
    body.style.webkitAnimation = "";
    chat.style.color = "#ffffff";
    message.style.color = "#000000";
    chatbox.style.webkitAnimation = "";
    sides.style.webkitAnimation = "";
    sidebar.style.webkitAnimation = "";
    topleft.style.webkitAnimation = "";
    topleft.style.color = "#192080";
    send.style.webkitAnimation = "";
    send.style.color = "#ffffff";
    sidenav.style.webkitAnimation = "";
    // for loop to cycle thru links in sidebar
    for (let i = 0; i < snav_iter; i++) {
        snav_text[i].style.color = "#818181";
    }
}