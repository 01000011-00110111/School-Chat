// set the theme
function setTheme(theme) {
    // set theme when button is pressed
    // other style function will change this, not directly called
    document.cookie = "theme=" + theme + "; path=/";
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
    }else if (event === "newyears") {
        setNewyearsTheme();
    } else if (event === "") {
        whichEvent();
    } else if (event === "special1" || event === "special2") {
        setSpecalStyle();
    } else if (event === "dev") {
        setDevStyle();
    } else if (event === "testing1") {
        setTestingStyle1();
    } else if (event === "testing2") {
        setTestingStyle2();
    } else if (event === "testing3") {
        setTestingStyle3();
    } else if (event === "testing4") {
        setTestingStyle4();
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
    let snav_text = sidenav.getElementsByTagName("a")
    let snav_iter = snav_text.length;
    // then set the color to what it is in the css document
    body.style.backgroundColor = "#000000";
    chat.style.color = "#ffffff";
    message.style.color = "#000000";
    chatbox.style.backgroundColor = "#181616";
    sides.style.backgroundColor = "#121212";
    sidebar.style.backgroundColor = "#171717";
    topleft.style.backgroundColor = "#f5f2f2";
    topleft.style.color = "#696969";
    send.style.backgroundColor = "#192080";
    send.style.color = "#ffffff";
    sidenav.style.backgroundColor = "#111";
    // for loop to cycle thru links in sidebar
    for (let i = 0; i < snav_iter; i++) {
        snav_text[i].style.color = "#818181";
    }
}

// sets theme to light mode for those people who are wierd
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
    let sidenav = document.getElementsByClassName("sidenav")[0]
    let snav_text = sidenav.getElementsByTagName("a")
    let snav_iter = snav_text.length;
    // then set the color to what it is in the css document
    body.style.backgroundColor = "#ffffff";
    chat.style.color = "#000000";
    message.style.color = "#000000";
    chatbox.style.backgroundColor = "#deddda";
    sides.style.backgroundColor = "#c0bfbc";
    topleft.style.backgroundColor = "#5A5A5A";
    topleft.style.color = "#000000";
    send.style.backgroundColor = "#192080";
    send.style.color = "#ffffff";
    sidenav.style.backgroundColor = "#b9c6c9";
    // for loop to cycle thru links in sidebar
    for (let i = 0; i < snav_iter; i++) {
        snav_text[i].style.color = "#313536";
    }
}

// never gonna give you up never gonna let you down
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
    let sidenav = document.getElementsByClassName("sidenav")[0]
    let snav_text = sidenav.getElementsByTagName("a")
    let snav_iter = snav_text.length;
    // then set the color to what it is in the css document
    body.style.backgroundColor = "#115029";
    chat.style.color = "#ffffff";
    message.style.color = "#4c0606";
    chatbox.style.backgroundColor = "#a91919";
    sides.style.backgroundColor = "#176d38";
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
    let sidenav = document.getElementsByClassName("sidenav")[0]
    let snav_text = sidenav.getElementsByTagName("a")
    let snav_iter = snav_text.length;
    // then set the color to what it is in the css document
    //its red make
    body.style.backgroundColor = "#115029";
    chat.style.color = "#ffffff";
    message.style.color = "#4c0606";
    chatbox.style.backgroundColor = "#a91919";
    sides.style.backgroundColor = "#176d38";
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
    let sidenav = document.getElementsByClassName("sidenav")[0]
    let snav_text = sidenav.getElementsByTagName("a")
    let snav_iter = snav_text.length;
    // then set the color to what it is in the css document
    body.style.backgroundColor = "#44220b";
    chat.style.color = "#4e8926";
    message.style.color = "#000000";
    chatbox.style.backgroundColor = "#e26831";
    sides.style.backgroundColor = "#44220b";
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
    let sidenav = document.getElementsByClassName("sidenav")[0]
    let snav_text = sidenav.getElementsByTagName("a")
    let snav_iter = snav_text.length;
    // then set the color to what it is in the css document
    body.style.backgroundColor = "#2c2525";
    chat.style.color = "#c64600";
    message.style.color = "#e66100";
    chatbox.style.backgroundColor = "#2c2525";
    sides.style.backgroundColor = "#2c2525";
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
    let sidenav = document.getElementsByClassName("sidenav")[0]
    let snav_text = sidenav.getElementsByTagName("a")
    let snav_iter = snav_text.length;
    // then set the color to what it is in the css document
    body.style.backgroundColor = "#44220b";
    chat.style.color = "#4e8926";
    message.style.color = "#000000";
    chatbox.style.backgroundColor = "#e26831";
    sides.style.backgroundColor = "#44220b";
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
    // ig this easter egg
    let userElement = document.getElementById("user");
    let user_name = userElement["value"];
    if (user_name === "DLHTCS") { // put your username here sir // how dare you sir
        // set theme in cookie
        setTheme("special1");
        // get all id tags
        let body = document.getElementById("body");
        let chat = document.getElementById("chat");
        let message = document.getElementById("message");
        let chatbox = document.getElementById("chatbox");
        let sides = document.getElementById("sides");
        let topleft = document.getElementById("topleft");
        let send = document.getElementById("send");
        let sidenav = document.getElementsByClassName("sidenav")[0]
        let snav_text = sidenav.getElementsByTagName("a")
        let snav_iter = snav_text.length;
        // then set the color to what it is in the css document
        body.style.backgroundColor = "#0d2f47";
        chat.style.color = "#0e8775";
        message.style.color = "#2c9696";
        chatbox.style.backgroundColor = "#0d4242";
        sides.style.backgroundColor = "#024a7d";
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
    } else if (user_name === "lovetheme") { // wow // I know i hate it too
        // set theme in cookie
        setTheme("special2");
        // get all id tags
        let body = document.getElementById("body");
        let chat = document.getElementById("chat");
        let message = document.getElementById("message");
        let chatbox = document.getElementById("chatbox");
        let sides = document.getElementById("sides");
        let topleft = document.getElementById("topleft");
        let send = document.getElementById("send");
        let sidenav = document.getElementsByClassName("sidenav")[0]
        let snav_text = sidenav.getElementsByTagName("a")
        let snav_iter = snav_text.length;
        // then set the color to what it is in the css document
        body.style.backgroundColor = "#d10d7c";
        chat.style.color = "#ffffff";
        message.style.color = "";
        chatbox.style.backgroundColor = "#c711d1";
        sides.style.backgroundColor = "#d10d7c";
        // ADD styling elements to css file from here
        topleft.style.backgroundColor = "d10d7c";
        topleft.style.color = "ffffff";
        sidenav.style.backgroundColor = "";
        // to here
        send.style.backgroundColor = "";
        send.style.color = "";
        // for loop to cycle thru links in sidebar
        for (let i = 0; i < snav_iter; i++) {
            snav_text[i].style.color = "#818181";
        }
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



//owens testing styles for all themes
function setTestingStyle1() {
    // set theme in cookie
    setTheme("testing1");
    // get all id tags
    let body = document.getElementById("body");
    let chat = document.getElementById("chat");
    let message = document.getElementById("message");
    let chatbox = document.getElementById("chatbox");
    let sides = document.getElementById("sides");
    let topleft = document.getElementById("topleft");
    let send = document.getElementById("send");
    let sidenav = document.getElementsByClassName("sidenav")[0]
    let snav_text = sidenav.getElementsByTagName("a")
    let snav_iter = snav_text.length;
    // then set the color to what it is in the css document
    body.style.backgroundColor = "#434270";
    chat.style.color = "#000000";
    message.style.color = "#000000";
    chatbox.style.backgroundColor = "#deddda";
    sides.style.backgroundColor = "#c0bfbc";
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
    let sidenav = document.getElementsByClassName("sidenav")[0]
    let snav_text = sidenav.getElementsByTagName("a")
    let snav_iter = snav_text.length;
    // then set the color to what it is in the css document
    body.style.backgroundColor = "#f59218";
    chat.style.color = "#000000";
    message.style.color = "#000000";
    chatbox.style.backgroundColor = "#413f5e";
    sides.style.backgroundColor = "#413f5e";
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
    let sidenav = document.getElementsByClassName("sidenav")[0]
    let snav_text = sidenav.getElementsByTagName("a")
    let snav_iter = snav_text.length;
    // then set the color to what it is in the css document
    body.style.backgroundColor = "#434270";
    chat.style.color = "#000000";
    message.style.color = "#000000";
    chatbox.style.backgroundColor = "#deddda";
    sides.style.backgroundColor = "#c0bfbc";
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
    let sidenav = document.getElementsByClassName("sidenav")[0]
    let snav_text = sidenav.getElementsByTagName("a")
    let snav_iter = snav_text.length;
    // then set the color to what it is in the css document
    body.style.backgroundColor = "#434270";
    chat.style.color = "#000000";
    message.style.color = "#000000";
    chatbox.style.backgroundColor = "#deddda";
    sides.style.backgroundColor = "#c0bfbc";
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