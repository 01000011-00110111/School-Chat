let theme = {}

const body = document.getElementsByTagName("body")[0];
const chat = document.getElementById("chat");
const message = document.getElementById("message");
const chatbox = document.getElementById("chatbox");
const sides = document.getElementById("sides");
const topleft = document.getElementById("topleft");
const send = document.getElementById("send");
const sidebar = document.getElementById("activenav");
const online = document.getElementById("online_users");
const online_users = sidebar.getElementsByTagName('button');
const sidenav = document.getElementsByClassName("sidenav")[0];
const snavText = sidenav.getElementsByTagName("a");
const roomText = document.getElementById("RoomDisplay");
const roomBar = document.getElementById("room_bar");
const topbar = document.getElementById("topbar");

function setTheme(data) {
    let colors = data.theme
    theme = data.theme
    let snav_iter = snavText.length;
    body.style.background = colors['body']
    chat.style.color = colors['chat-text']
    message.style.background = colors['chat-background']
    chatbox.style.background = colors['chatbox-background']
    sides.style.color = colors['sides-text']
    sides.style.background = colors['sides-background']
    sidebar.style.background = colors['sidebar-background']
    sidebar.style.borderColor = colors['sidebar-border']
    for (let i = 0; i < online_users.length; i++) {
        online_users[i].style.color = colors['sidebar-text']
    }
    sidebar.style.boxShadow = colors['sidebar-boxShadow']
    topleft.style.background = colors['topleft-background']
    topleft.style.color = colors['topleft-text']
    send.style.background = colors['send-background']
    send.style.color = colors['send-text']
    sidenav.style.background = colors['sidenav-background']
    sidenav.style.color = colors['sidenav-color']
    for (let i = 0; i < snav_iter; i++) {
        snavText[i].style.color = colors['sidenav-a-color']
        snavText[i].style.background = colors['sidenav-a-background']
    }
    roomText.style.color = colors['roomText-text']
    topbar.style.background = colors['topbar-background']
    topbar.style.boxShadow = colors['topbar-boxShadow']
}

socket.on('set_theme', (theme) =>{
    setTheme(theme)
    console.log(theme)
})

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