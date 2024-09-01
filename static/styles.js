// Copyright (C) 2023, 2024  cserver45, cseven
// License info can be viewed in main.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat
let theme = {}

const body = document.getElementsByTagName("body")[0];
const chat = document.getElementById("chat");
const message = document.getElementById("message");
const chatbox = document.getElementById("chatbox");
const sides = document.getElementById("sides");
const topleft = document.getElementById("topleft");
const send = document.getElementById("send");
const sidebar = document.getElementById("activenav");
const sidenav = document.getElementsByClassName("sidenav")[0];
// const extratext = document.getElementById('extratext');
const extrabutton = document.getElementsByClassName("extrabuttons");
const snavText = document.querySelectorAll("#room_names");
const roomText = document.getElementById("RoomDisplay");
const roomBar = document.getElementById("room_bar");
const topbar = document.getElementById("topbar");
const online = document.getElementById("online");
const offline = document.getElementById("offline");

function setTheme(data) {
    const online_users = document.querySelectorAll("#online_buttons");
    let colors = data.theme
    theme = data.theme
    // let snav_iter = snavText.length;
    let extra_iter = extrabutton.length;
    body.style.background = colors['body']
    chat.style.color = colors['chat-text']
    message.style.background = colors['chat-background']
    message.style.color = colors['chat-color']
    // chatbox.style.background = colors['chatbox-background']
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
    sidenav.style.color = colors['sidenav-color']
    // for (let i = 0; i < snav_iter; i++) {
    //     snavText[i].style.color = colors['sidenav-a-color']
    //     snavText[i].style.background = colors['sidenav-a-background']
    // }
    for (var i = 0; i < extra_iter; i++) {
      extrabutton[i].style.color = colors['sidenav-a-color']
      extrabutton[i].style.background = colors['sidenav-a-background']
    }
    roomText.style.color = colors['roomText-text']
    topbar.style.background = colors['topbar-background']
    topbar.style.boxShadow = colors['topbar-boxShadow']
    online.style.color = colors['online-color']
    offline.style.color = colors['offline-color']
    // console.log('done theme')
    socket.emit("get_full_list");
}

socket.on('set_theme', (theme) =>{
    setTheme(theme)
    // console.log(theme)
})