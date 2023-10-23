function setStyles(
    backgroundColor,
    chatColor,
    messageColor,
    chatboxColor,
    sidesColor,
    sidebarColor,
    sidebarborderColor,
    sidebarTextColor,
    topleftColor,
    topleftTextColor,
    sendBgColor,
    sendTextColor,
    sidenavColor,
    snavLinkColor
) {
    const body = document.getElementsByTagName("body")[0];
    const chat = document.getElementById("chat");
    const message = document.getElementById("message");
    const chatbox = document.getElementById("chatbox");
    const sides = document.getElementById("sides");
    const topleft = document.getElementById("topleft");
    const send = document.getElementById("send");
    const sidebar = document.getElementById("activenav");
    const online = document.getElementById("online_users");
    const sidenav = document.getElementsByClassName("sidenav")[0];
    const snavText = sidenav.getElementsByTagName("a");

    body.style.backgroundColor = backgroundColor;
    chat.style.color = chatColor;
    message.style.color = messageColor;
    chatbox.style.backgroundColor = chatboxColor;
    sides.style.backgroundColor = sidesColor;
    sidebar.style.backgroundColor = sidebarColor;
    sidebar.style.borderLeft = `4px solid ${sidebarborderColor}`;
    online.style.color = sidebarTextColor;
    topleft.style.backgroundColor = topleftColor;
    topleft.style.color = topleftTextColor;
    send.style.backgroundColor = sendBgColor;
    send.style.color = sendTextColor;
    sidenav.style.backgroundColor = sidenavColor;

    for (let i = 0; i < snavText.length; i++) {
        snavText[i].style.color = snavLinkColor;
    }
}

function setTheme(themeName) {
    const themes = {
        dark: darkTheme,
        light: lightTheme,
        ogdev: ogDevTheme,
        dev: devTheme,
        halloween: halloweenTheme,
        winter: winterTheme,
    };

    setStyles(...themes[themeName]);
}

const darkTheme = [
    "#000000",
    "#ffffff",
    "#000000",
    "#181616",
    "#121212",
    "#171717",
    "#f5f2f2",   // Sidebar Background Color
    "#3b3b3b",   // Sidebar Border Color
    "#c73228",   // Sidebar Text Color
    "#192080",
    "#192080",
    "#ffffff",
    "#111",
    "#818181",
];

const lightTheme = [
    "#c0bfbc",   // Background Color
    "#000000",   // Chat Color
    "#000000",   // Message Color
    "#deddda",   // Chatbox Color
    "#c0bfbc",   // Sides Color
    "#000000",   // Sidebar Background Color
    "#3b3b3b",   // Sidebar Border Color
    "#ffffff",   // Sidebar Text Color
    "#5A5A5A",   // Topleft Background Color
    "#1b0670",   // Topleft Text Color
    "#3daec4",   // Send Button Background Color
    "#33575e",   // Send Button Text Color
    "#b9c6c9",   // Sidenav Color
    "#192080"    // Sidenav Link Color
];

const ogDevTheme = [
    "#000000",  // Background Color
    "#228e3d",  // Chat Color
    "#000000",  // Message Color
    "#181616",  // Chatbox Color
    "#121212",  // Sides Color
    "#171717",  // Sidebar Background Color
    "#3b3b3b",  // Sidebar Border Color
    "#ffffff",  // Sidebar Text Color
    "#121212",  // Topleft Background Color
    "#696969",  // Topleft Text Color
    "#192080",  // Send Button Background Color
    "#ffffff",  // Send Button Text Color
    "#111",     // Sidenav Color   
    "#818181",  // Sidenav Link Color
];

const devTheme = [
    "#000000",
    "#18691f",
    "#000000",
    "#0d0d0d",
    "#080808",
    "#080808",
    "#0d0d0d",   // Sidebar Background Color
    "#3b3b3b",   // Sidebar Border Color
    "#ffffff",   // Sidebar Text Color
    "#ffffff",
    "#006600",
    "#ffffff",
    "#0f0f0f",
    "#8a4e11",
];

const halloweenTheme = [
    "#000000", // Background Color
    "#d64304", // Chat Color
    "#a64903", // Message Color
    "#000", // Chatbox Color
    "#121212", // Sides Color
    "#d65e13", // Sidebar Backgroud Color
    "#bf4a06", // Sidebar Line Color
    "#3b3b3b", // Sidebar Border Color
    "#bf4a06", // Sidebar Text Color
    "#d64304", // Topleft Background Color
    "#d64304", // 
    "#000", 
    "#111",
    "#d64304",
]; 

const winterTheme = [
    "#AED9FF",
    "#d64304",
    "#000000",
    "#FF9933",
    "#121212",
    "#FF9933",
    "#f5f2f2",   // Sidebar Background Color
    "#3b3b3b",   // Sidebar Border Color
    "#ffffff",   // Sidebar Text Color
    "#FF9933",
    "#d64304",
    "#ffffff",
    "#111",
    "#d64304", 
];
