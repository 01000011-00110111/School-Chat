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
        let pfp = document.getElementsByClassName("pfp")[0];
        for (let i = 0; i < pfp.length; i++) {
            pfp[i].style.display = "none";
        }
        document.getElementById("chat").style.lineheight = "32";
        window.localStorage.setItem("Profileactive", "false");
        Pbutton.value = "Enable profile pictures";
        Pbutton.style.backgroundColor = "green";
    } else {
        let pfp = document.getElementsByClassName("pfp")[0];
        for (let i = 0; i < pfp.length; i++) {
            pfp[i].style.display = "";
        }
        document.getElementById("chat").style.lineheight = "40";
        window.localStorage.setItem("Profileactive", "true");
        Pbutton.value = "Disable profile pictures";
        Pbutton.style.backgroundColor = "red";
    }
}

// for event theme
// set what event is currently being used
function whichEvent(event = "dark") {
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

// sets theme to christmas (event)
function setChristmasTheme() {
    // set theme in cookie
    setTheme("christmas");
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
    body.style.backgroundColor = "#115029";
    chat.style.color = "#ffffff";
    message.style.color = "#4c0606";
    chatbox.style.backgroundColor = "#a91919";
    sides.style.backgroundColor = "#176d38";
    sidebar.style.backgroundColor = "#171717";
    topleft.style.backgroundColor = "#176d38";
    topleft.style.color = "#c2bcbc";
    send.style.backgroundColor = "#6caa55";
    send.style.color = "#c2bcbc";
    sidenav.style.backgroundColor = "#292";
    // for loop to cycle thru links in sidebar
    for (let i = 0; i < snav_iter; i++) {
        snav_text[i].style.color = "#d0c8c8";
    }
}
//this is new years thing that will never use 
function setNewyearsTheme() {
    // set theme in cookie
    setTheme("newyears");
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
    //its red make
    body.style.backgroundColor = "#115029";
    chat.style.color = "#ffffff";
    message.style.color = "#4c0606";
    chatbox.style.backgroundColor = "#a91919";
    sides.style.backgroundColor = "#176d38";
    sidebar.style.backgroundColor = "#171717";
    topleft.style.backgroundColor = "#176d38";
    topleft.style.color = "#c2bcbc";
    send.style.backgroundColor = "#6caa55";
    send.style.color = "#c2bcbc";
    sidenav.style.backgroundColor = "#292";
    // for loop to cycle thru links in sidebar
    for (let i = 0; i < snav_iter; i++) {
        snav_text[i].style.color = "#d0c8c8";
    }
}

// sets theme to thanksgiving (event)
function setThanksTheme() {
    // set theme in cookie
    setTheme("thanks");
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
    body.style.backgroundColor = "#44220b";
    chat.style.color = "#4e8926";
    message.style.color = "#000000";
    chatbox.style.backgroundColor = "#e26831";
    sides.style.backgroundColor = "#44220b";
    sidebar.style.backgroundColor = "#171717";
    // ADD styling elements to css file from here
    topleft.style.backgroundColor = "#176d38";
    topleft.style.color = "#c2bcbc";
    sidenav.style.backgroundColor = "#292";
    // to here
    send.style.backgroundColor = "#d63420";
    send.style.color = "#fcaf2c";
    // for loop to cycle thru links in sidebar
    for (let i = 0; i < snav_iter; i++) {
        snav_text[i].style.color = "#d0c8c8";
    }
}

// sets theme to thanksgiving (event)
function setHollowTheme() {
    // set theme in cookie
    setTheme("hollow");
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
    body.style.backgroundColor = "#2c2525";
    chat.style.color = "#c64600";
    message.style.color = "#e66100";
    chatbox.style.backgroundColor = "#2c2525";
    sides.style.backgroundColor = "#2c2525";
    sidebar.style.backgroundColor = "#171717";
    // ADD styling elements to css file from here
    topleft.style.backgroundColor = "#176d38";
    topleft.style.color = "#35312a";
    sidenav.style.backgroundColor = "#111";
    // to here
    send.style.backgroundColor = "#0093b0";
    send.style.color = "#000000";
    // for loop to cycle thru links in sidebar
    for (let i = 0; i < snav_iter; i++) {
        snav_text[i].style.color = "#d0c8c8";
    }
}

// sets theme to thanksgiving (event)
function setThanksTheme() {
    // set theme in cookie
    setTheme("thanks");
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
    body.style.backgroundColor = "#44220b";
    chat.style.color = "#4e8926";
    message.style.color = "#000000";
    chatbox.style.backgroundColor = "#e26831";
    sides.style.backgroundColor = "#44220b";
    sidebar.style.backgroundColor = "#171717";
    // ADD styling elements to css file from here
    topleft.style.backgroundColor = "#176d38";
    topleft.style.color = "#c2bcbc";
    sidenav.style.backgroundColor = "#292";
    // to here
    send.style.backgroundColor = "#d63420";
    send.style.color = "#fcaf2c";
    // for loop to cycle thru links in sidebar
    for (let i = 0; i < snav_iter; i++) {
        snav_text[i].style.color = "#d0c8c8";
    }
}

// sets theme to specal style
function setSpecalStyle() {
        setTheme("special1");
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
        body.style.backgroundColor = "#0d2f47";
        chat.style.color = "#0e8775";
        message.style.color = "#2c9696";
        chatbox.style.backgroundColor = "#0d4242";
        sides.style.backgroundColor = "#024a7d";
        sidebar.style.backgroundColor = "#171717";
        // ADD styling elements to css file from here
        topleft.style.backgroundColor = "#024a7d";
        topleft.style.color = "#0481d9";
        sidenav.style.backgroundColor = "#2c5978";
        // to here
        send.style.backgroundColor = "#0d5e5e";
        send.style.color = "#010a0f";
        // for loop to cycle thru links in sidebar
        for (let i = 0; i < snav_iter; i++) {
            snav_text[i].style.color = "#818181";
        }
    } 

function valstyle() {
        // set theme in cookie
    setTheme("valstyle");
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
    body.style.backgroundColor = "#910410";
    chat.style.color = "#fafcfb";
    message.style.color = "#000000";
    chatbox.style.backgroundColor = "#d41320";
    sides.style.backgroundColor = "#910410";
    sidebar.style.backgroundColor = "#171717";
    topleft.style.backgroundColor = "#d41320";
    topleft.style.color = "#ed0968";
    send.style.backgroundColor = "#ed0968";
    send.style.color = "#ffffff";
    sidenav.style.backgroundColor = "#d41320";
    // for loop to cycle thru links in sidebar
    for (let i = 0; i < snav_iter; i++) {
        snav_text[i].style.color = "#313536";
    }
}

function set4thStyle() {
    // set theme in cookie
    setTheme("4th");
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
    body.style.backgroundColor = "#0000FF";
    chat.style.color = "#ffffff";
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


//owens testing styles for all themes
function setTestingStyle2() {
    // set theme in cookie
    setTheme("testing2");
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
    body.style.backgroundColor = "#f59218";
    chat.style.color = "#000000";
    message.style.color = "#000000";
    chatbox.style.backgroundColor = "#413f5e";
    sides.style.backgroundColor = "#413f5e";
    sidebar.style.backgroundColor = "#171717";
    topleft.style.backgroundColor = "#5A5A5A";
    topleft.style.color = "#413f5e";
    send.style.backgroundColor = "#f59218";
    send.style.color = "#413f5e";
    sidenav.style.backgroundColor = "#413f5e";
    // for loop to cycle thru links in sidebar
    for (let i = 0; i < snav_iter; i++) {
        snav_text[i].style.color = "#313536";
    }
}

function setTestingStyle3() {
    // set theme in cookie
    setTheme("testing3");
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
    body.style.backgroundColor = "#910410";
    chat.style.color = "#fafcfb";
    message.style.color = "#000000";
    chatbox.style.backgroundColor = "#d41320";
    sides.style.backgroundColor = "#910410";
    sidebar.style.backgroundColor = "#171717";
    topleft.style.backgroundColor = "#d41320";
    topleft.style.color = "#ed0968";
    send.style.backgroundColor = "#ed0968";
    send.style.color = "#ffffff";
    sidenav.style.backgroundColor = "#d41320";
    // for loop to cycle thru links in sidebar
    for (let i = 0; i < snav_iter; i++) {
        snav_text[i].style.color = "#313536";
    }
}

function setTestingStyle4() {
    // set theme in cookie
    setTheme("testing4");
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
    body.style.backgroundColor = "#434270";
    chat.style.color = "#000000";
    message.style.color = "#000000";
    chatbox.style.backgroundColor = "#deddda";
    sides.style.backgroundColor = "#c0bfbc";
    sidebar.style.backgroundColor = "#171717";
    topleft.style.backgroundColor = "#5A5A5A";
    topleft.style.color = "#000000";
    send.style.backgroundColor = "#343cad";
    send.style.color = "#ffffff";
    sidenav.style.backgroundColor = "#729fcf";
    // for loop to cycle thru links in sidebar
    for (let i = 0; i < snav_iter; i++) {
        snav_text[i].style.color = "#313536";
    }
}