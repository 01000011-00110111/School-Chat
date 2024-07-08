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
    snavLinkColor,
    roomTextColor,
    topbarColor
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
    const roomText = document.getElementById("RoomDisplay");
    const topbar = document.getElementById("topbar");
    // const hrElement = document.querySelector("hr");

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
    roomText.style.color = roomTextColor;
    topbar.style.backgroundColor = topbarColor;
    // hrElement.sytle.bordeColor = sidebarborderColor;

    for (let i = 0; i < snavText.length; i++) {
        snavText[i].style.color = snavLinkColor;
    }
}

function setTheme(themeName) {
    const themes = {
        dark: darkTheme,
        better_dark: betterdarkTheme,
        light: lightTheme,
        ogdev: ogDevTheme,
        dev: devTheme,
        halloween: halloweenTheme,
        // winter: winterTheme,
        white_lavender: whiteLavender,
        greenish_white: Greenish_white
    };

    setStyles(...themes[themeName]);
}

// Note the the code for the themes are arraganged in this order, so if you want the background to be the color black you change the first value of the theme to #000000 or black.

// Background Color
// Chat Color
// Message Color
// Chatbox Color
// Sides Color
// Sidebar Background Color
// Sidebar Border Color
// Sidebar Text Color
// Topleft Background Color
// Topleft Text Color
// Send Button Background Color
// Send Button Text Color
// Sidenav Color
// Sidenav Link Color
// Room Text color
// Topbar Background Color

const darkTheme = [
    "#000000",
    "#ffffff",
    "#000000",
    "#181616",
    "#121212",
    "#171717",
    "#f5f2f2",
    "#ffffff",
    "#c73228",
    "#192080",
    "#192080",
    "#ffffff",
    "#111111",
    "#818181",
    "#000000",
    "#ffffff"
];

const lightTheme = [
    "#c0bfbc",
    "#000000",
    "#000000",
    "#deddda",
    "#c0bfbc",
    "#000000",
    "#3b3b3b",
    "#ffffff",
    "#5A5A5A",
    "#1b0670",
    "#3daec4",
    "#33575e",
    "#b9c6c9",
    "#192080",
    "#000000",
    "#ffffff"
];

const ogDevTheme = [
    "#000000",
    "#228e3d",
    "#000000",
    "#181616",
    "#121212",
    "#171717",
    "#3b3b3b",
    "#ffffff",
    "#121212",
    "#696969",
    "#192080",
    "#ffffff",
    "#111111",
    "#818181",
    "#000000",
    "#ffffff"
];

const devTheme = [
    "#000000",
    "#18691f",
    "#000000",
    "#0d0d0d",
    "#080808",
    "#080808",
    "#0d0d0d",
    "#ffffff",
    "#ffffff",
    "#ffffff",
    "#006600",
    "#ffffff",
    "#0f0f0f",
    "#8a4e11",
    "#000000"
];

const halloweenTheme = [
    "#000000",
    "#d64304",
    "#a64903",
    "#000111",
    "#000000",
    "#d65e13",
    "#bf4a06",
    "#000000",
    "#000000",
    "#d64304",
    "#d65e13",
    "#111111",
    "#000000",
    "#d65e13",
    "#d65e13",
    "#ffffff"
];

const betterdarkTheme = [
  "#000000",
  "#ffffff",
  "",
  "#transparent",
  "#000000",
  "#0c0c0c",
  "#000000",
  "#ffffff",
  "#transparent",
  "192080",
  "#e9e9ed",
  "#000000",
  "#111111",
  "#ffffff",
  "#dd7016",
  "#000000"
];

const whiteLavender = [ 
	"rgb(245, 245, 245)", 
	"rgb(0, 0, 0)", 
	"rgb(141, 129, 203)", 
	"rgb(255, 255, 255)", 
	"rgb(255, 255, 255)", 
	"rgb(255, 255, 255)", 
	"rgb(130, 117, 191)", 
	"rgb(0, 0, 0)",
	"rgb(130, 117, 191)", 
	"rgb(255, 255, 255)", 
	"rgb(130, 117, 191)", 
	"rgb(255, 255, 255)", 
	"rgb(130, 117, 191)", 
	"rgb(255, 255, 255)",
	"rgb(255, 255, 255)", 
	"rgb(133, 117, 196)"
];

const Greenish_white = [ 
	"rgb(0, 216, 12)", 
	"rgb(255, 255, 255)", 
	"", 
	"", 
	"rgb(0, 249, 0)", 
	"rgb(0, 216, 12)", 
	"rgb(255, 255, 255)", 
	"rgb(255, 255, 255)", 
	"", 
	"rgb(25, 32, 128)", 
	"", 
	"", 
	"rgb(254, 255, 255)", 
	"rgb(0, 249, 0)", 
	"rgb(0, 216, 12)", 
	"rgb(255, 255, 255)"
];