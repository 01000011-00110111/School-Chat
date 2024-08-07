// Copyright (C) 2023, 2024  cserver45, cseven
// License info can be viewed in main.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat
let project = {}

const pushNotification = (sender, message, icon) => {
  createNotification(sender, message, icon);

  const remove_notification = () => {
    const notifications = document.getElementsByTagName('notification');
    for (let i = 0; i < notifications.length; i++) {
      notifications[i].remove()
    } 
  }
  setTimeout(remove_notification, 6710)
}

const createNotification = (title, content, img) => {
  const notifcation = document.createElement('notification');
  const notification_title = document.createElement('h4');
  const notification_content = document.createElement('p');
  const content_panel = document.createElement('div');
  const img_panel = document.createElement('div');
  const close_panel = document.createElement('div');
  const close_button = document.createElement('button')
  const icon = document.createElement('img');

  img_panel.classList.add("img_panel");
  content_panel.classList.add("content_panel");
  close_panel.classList.add('close_panel');

  close_button.innerHTML = '<i class="fa-solid fa-x"></i>';
  notification_title.innerHTML = title;
  notification_content.innerHTML = content;
  icon.src = img;

  const end_notification = () => {
    notifcation.style.animationName = "notification_slide_out";
    notifcation.style.animationDuration = ".7s";
  }
   setTimeout(end_notification, 6000)

  close_button.addEventListener('click', () => {
    notifcation.remove()
  });
  
  document.getElementById("main").appendChild(notifcation);
  notifcation.appendChild(img_panel);
  notifcation.appendChild(content_panel);
  notifcation.appendChild(close_panel)
  content_panel.appendChild(notification_title);
  content_panel.appendChild(notification_content);
  img_panel.appendChild(icon);
  close_panel.appendChild(close_button);
}

function OpenProperties() {
  let controls = document.getElementById("controls");
  
  controls.style.marginLeft = "0%";
  controls.style.transition = "all 1s";
}

function CloseProperties() {
  controls.style.marginLeft = "-22%";
  controls.style.transition = "all 1s";
}

// Document Object Model imports
let theme_name1 = document.getElementById("n_name");

let applyButton = document.getElementById("applyButton");
let editmodeText = document.getElementById("editmodeText");
const exit_button = document.getElementById("exit_editor_button");
const editor_dropdown = document.getElementById("editor_dropdown");
const editor_dropdown_button = document.getElementById("editor_dropdown_button");

const body = document.getElementsByTagName("body")[0];
const chat = document.getElementById("chat");
const message = document.getElementById("message");
const chatbox = document.getElementById("chatbox");
const sides = document.getElementById("sides");
const topleft = document.getElementById("topleft");
const send = document.getElementById("send");
const sidebar = document.getElementById("activenav");
const sidenav = document.getElementsByClassName("sidenav")[0];
const extratext = document.getElementById('extratext');
const extrabutton = document.getElementsByClassName("extrabuttons");
const snavText = document.querySelectorAll("#room_names");
const roomText = document.getElementById("RoomDisplay");
const roomBar = document.getElementById("room_bar");
const topbar = document.getElementById("topbar");
const online = document.getElementById("online");
const offline = document.getElementById("offline");
// const hrElement = document.querySelector("hr");
// const online = document.getElementById("online_users");

const ColorPickers = document.querySelectorAll("#ColorPicker");
const color_inputs = document.querySelectorAll("#color_display_input");
const gradient_button = document.getElementById("gradient_mode_button");

// After this is the Theme & CSE code

function saveProject() {
  const online_users = document.querySelectorAll("#online_buttons");
  theme = {
    'body': body.style.background,
    'chat-text': chat.style.color,
    'chat-background': message.style.background,
    'chat-color': message.style.color,
    // 'chatbox-background': chatbox.style.background,
    'sides-text': sides.style.color,
    'sides-background': sides.style.background,
    'sidebar-background': sidebar.style.background,
    'sidebar-boxShadow': sidebar.style.boxShadow,
    'sidebar-border': sidebar.style.borderColor,
    'sidebar-text': online_users[0].style.color,
    'topleft-background': topleft.style.background,
    'topleft-text': topleft.style.color,
    'send-background': send.style.background,
    'send-text': send.style.color,
    'sidenav-background': sidenav.style.background,
    'sidenav-color': snavText[0].style.color,
    'sidenav-text': sidenav.style.color,
    'sidenav-a-background': snavText[0].style.background,
    'sidenav-a-color': snavText[0].style.color,
    'roomText-text': roomText.style.color,
    'topbar-background': topbar.style.background,
    'topbar-boxShadow': topbar.style.boxShadow,
    'online-color': online.style.color,
    'offline-color': offline.style.color,
  }
  // project = {
  //   "name": theme_name1.value,
  //   'author': [getCookie("Userid"), getCookie("DisplayName").replace(/"/g, '')],
  //   theme: theme,
  //   'status': 'private',
  // }
  // project.project = theme
  // project.name = theme_name1.value
  socket.emit('save_project', project['themeID'], theme, theme_name1.value, false)
}

function publishProject() {
  const room_names = document.querySelectorAll("#room_names");
  const online_users = document.querySelectorAll("#online_buttons");
  var room_names_background = "";
  var room_names_color = "";
  var online_users_color = "";
  for (let index = 0; index < room_names.length; index++) {
    room_names_background = room_names[index].style.background;
    room_names_color = room_names[index].style.color;
  }

  for (let index = 0; index < online_users.length; index++) {
    online_users_color = online_users[index].style.color;
  }

  theme = {
    'body': body.style.background,
    'chat-text': chat.style.color,
    'chat-background': message.style.background,
    'chat-color': message.style.color,
    // 'chatbox-background': chatbox.style.background,
    'sides-text': sides.style.color,
    'sides-background': sides.style.background,
    'sidebar-background': sidebar.style.background,
    'sidebar-boxShadow': sidebar.style.boxShadow,
    'sidebar-border': sidebar.style.borderColor,
    'sidebar-text': online_users[0].style.color,
    'topleft-background': topleft.style.background,
    'topleft-text': topleft.style.color,
    'send-background': send.style.background,
    'send-text': send.style.color,
    'sidenav-background': sidenav.style.background,
    'sidenav-color': snavText[0].style.color,
    // 'sidenav-text': sidenav.style.color,
    'sidenav-a-background': snavText[0].style.background,
    'sidenav-a-color': snavText[0].style.color,
    'roomText-text': roomText.style.color,
    'topbar-background': topbar.style.background,
    'topbar-boxShadow': topbar.style.boxShadow,
    'online-color': online.style.color,
    'offline-color': offline.style.color,
  }
  // project.theme = theme
  // project.project = theme
  // project.name = theme_name1.value
  // project['status'] = 'public'
  socket.emit('save_project', project['themeID'], theme, theme_name1.value, true)
}

// Controls Sidenav
function openNav() {
  if (currentSelection != "Edit") {
    if (window.screen.width <= 450) {
      document.getElementById("mySidenav").style.width = "100%";
    } else {
      document.getElementById("mySidenav").style.width = "250px";
    }
  }
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}

const propertyStates = ["disabled", "enabled"];
const setProperties = (background, text, shadow, border) => {
  if (background === propertyStates[0]) {
    ColorPickers[0].style.display = "none";
  } else if (border === propertyStates[1]) {
    ColorPickers[0].style.display = "flex";
  }

  if (text === propertyStates[0]) {
    ColorPickers[2].style.display = "none";
  } else if (border === propertyStates[1]) {
    ColorPickers[2].style.display = "flex";
  }

  if (shadow === propertyStates[0]) {
    ColorPickers[3].style.display = "none";
  } else if (border === propertyStates[1]) {
    ColorPickers[3].style.display = "flex";
  }

  if (border === propertyStates[0]) {
    ColorPickers[4].style.display = "none";
  } else if (border === propertyStates[1]) {
    ColorPickers[4].style.display = "flex";
  }
}

const selectionMode = ["View", "Edit"];
var currentSelection = selectionMode[0];

const setSelectionMode = (modeInt) => {
  currentSelection = selectionMode[modeInt];
  editmodeText.innerHTML = currentSelection;
}
setSelectionMode(0)

const AllContent = document.querySelectorAll("#ChatMockup");
const menuOwner = document.getElementById("menuOwner");

// Opens a project
function open_project(data) {
  const online_users = document.querySelectorAll("#online_buttons");

  let colors = data.project
  let snav_iter = snavText.length;
  let extra_iter = extrabutton.length;
  theme_name1.value = data.name;
  document.title = `${data.name} - Theme Editor`;
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
  for (let i = 0; i < snav_iter; i++) {
      snavText[i].style.color = colors['sidenav-a-color']
      snavText[i].style.background = colors['sidenav-a-background']
  }
  for (var i = 0; i < extra_iter; i++) {
    extrabutton[i].style.color = colors['sidenav-a-color']
    extrabutton[i].style.background = colors['sidenav-a-background']
  }
  roomText.style.color = colors['roomText-text']
  topbar.style.background = colors['topbar-background']
  topbar.style.boxShadow = colors['topbar-boxShadow']
  online.style.color = colors['online-color']
  offline.style.color = colors['offline-color']

  const deployment_indicator = document.getElementById("deployment_indicator");
  const deployment_text = document.getElementById("deployment_text");
  if (data.status === "public") {
    deployment_indicator.style.background = "lime";
    deployment_text.innerHTML = "Deployed";
  } else {
    deployment_indicator.style.background = "red";
    deployment_text.innerHTML = "Undeployed";
  }
}

const gradient_icon = document.getElementById("gradient_mode_button");
const colorMode = ["Solid", "Gradient"]
var currentColorMode = colorMode[0]

const setColorMode = (modeInt) => {
  currentColorMode = colorMode[modeInt];
}

const enableGradient = () => {
  ColorPickers[1].style.display = "flex";
  setColorMode(1);
  gradient_icon.innerHTML = '<i class="fa-solid fa-circle"></i>';
}

const disableGradient = () => {
  ColorPickers[1].style.display = "none";
  setColorMode(0);
  gradient_icon.innerHTML = '<i class="fa-solid fa-circle-half-stroke"></i>';
}

gradient_button.addEventListener('click', () => {
  if (currentColorMode != colorMode[1]) {
    enableGradient();
  } else {
    disableGradient();
  }
})

var shadow_user = "";

AllContent.forEach((element) => {
  element.addEventListener("click", (event) => {
    if (event.target.id != "") {
      if (currentSelection === "Edit") {
        element.classList.toggle("active");
        OpenProperties();

        var SelectedLayer = event.target.id;
        const ColorBox = document.getElementById("body-color");
        const gradientColor = document.getElementById("2nd-body-color")
        const textColor = document.getElementById("text-color");
        const borderColor = document.getElementById("border-color");
        const shadowColor = document.getElementById("shadow-color");
        const Chat = document.getElementById("ChatMockup");
        menuOwner.innerHTML = SelectedLayer;

        switch(SelectedLayer) {
          case "topbar":
            setProperties("enabled", "enabled", "enabled", "enabled");
            break;
          case "mySidenav":
            setProperties("enabled", "enabled", "disabled", "disabled");
            break;
          case "activenav":
            setProperties("enabled", "enabled", "enabled", "enabled");
            break;
          case "sides":
            setProperties("enabled", "disabled", "disabled", "disabled");
            break;
          case "room_names":
            setProperties("enable", "enable", "disabled", "disabled");
            break;
          case "online_buttons":
            setProperties("disabled", "enable", "disabled", "disabled");
            break;
          case "RoomDisplay":
            setProperties("disabled", "enable", "disabled", "disabled");
            break;
          case "topleft":
            setProperties("disabled", "enable", "disabled", "disabled");
            break;
          case "send":
            setProperties("enabled", "enabled", "disabled", "disabled");
            break;
          case "pfpmenu":
            setProperties("disabled", "disabled", "disabled", "enabled");
            break;
          case "online":
            setProperties("disabled", "enabled", "disabled", "disabled");
          break;
          case "offline":
            setProperties("disabled", "enabled", "disabled", "disabled");
          break;
          default:
            setProperties("enabled", "enabled", "enabled", "enabled");
        }

        const fetchColors = () => {
          document.getElementsByClassName("ColorDisplay")[0].style.background = document.getElementById(`${SelectedLayer}`).style.background;
          document.getElementsByClassName("ColorDisplay")[2].style.background = document.getElementById(`${SelectedLayer}`).style.color;
          document.getElementsByClassName("ColorDisplay")[3].style.background = document.getElementById(`${SelectedLayer}`).style.boxShadow.slice(document.getElementById(`${SelectedLayer}`).style.boxShadow.split(" ")[3], 16)
          document.getElementsByClassName("ColorDisplay")[4].style.background = document.getElementById(`${SelectedLayer}`).style.borderColor;
        };
        fetchColors();

        applyButton.addEventListener("click", (event) => {
          if (SelectedLayer == menuOwner.innerHTML) {

            if (SelectedLayer === "topbar") {
              shadow_user = "0px -1px 44px 15px"
            }
            else if (SelectedLayer === "activenav")
            {
              shadow_user = "10px 20px 17px 16px"
            }
            else
            {
              shadow_user = ""
            }

            if (SelectedLayer === "room_names") {
              const rooms = document.querySelectorAll('#room_names');
              for (let index = 0; index < rooms.length; index++) {
                rooms[index].style.background = ColorBox.value;
                rooms[index].style.color = textColor.value;        
              }
            }
          
            if (SelectedLayer === "online_buttons") {
              const online_buttons = document.querySelectorAll("#online_buttons");
              for (let index = 0; index < online_buttons.length; index++) {
                online_buttons[index].style.color = textColor.value;
              }
            }

            switch (currentColorMode) {
              case 'Solid':
                document.getElementById(SelectedLayer).style.setProperty('background', ColorBox.value)
                document.getElementById(SelectedLayer).style.setProperty('color', textColor.value)
                document.getElementById(SelectedLayer).style.setProperty('border-color', borderColor.value)
                document.getElementById(SelectedLayer).style.boxShadow = `${shadow_user} ${shadowColor.value}`;
                break;
              
              case 'Gradient':
                document.getElementById(SelectedLayer).style.setProperty('background', `linear-gradient(to right, ${ColorBox.value}, ${gradientColor.value})`)
                document.getElementById(SelectedLayer).style.setProperty('color', textColor.value)
                document.getElementById(SelectedLayer).style.setProperty('border-color', borderColor.value)
                document.getElementById(SelectedLayer).style.boxShadow = `${shadow_user} ${shadowColor.value}`;
                break;
            }

            function Update() {
              document.body.style.background = chat.style.background;
              Chat.style.background = chat.style.background;
            };

            Update();
            fetchColors();
          };
        });
      };
    };
  });
});

document.title = theme_name1.value + " - Theme Editor";

theme_name1.addEventListener("focusout", (event) => {
  document.title = theme_name1.value + " - Theme Editor";
});

exit_button.addEventListener('click', (event) => {
  window.location.href = "/projects";
});

editor_dropdown_button.addEventListener('click', (event) => {
  if (editor_dropdown.style.display != "grid") {
    editor_dropdown.style.display = "grid";
  } else {
    editor_dropdown.style.display = "none";
  }
});

/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function openColorPanel() {
  document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
} 

function Runstartup() {
  value = sessionStorage.getItem("editing")
  if (value !== '') {
    socket.emit('get_project', value)
  } else {
    socket.emit('create_project')
  }
}

socket.on('set_theme', (theme) => {
  project = theme
  open_project(theme);
  sessionStorage.setItem('editing', theme['themeID']);
});

socket.on('response', (response, limit) => {
  console.log(response)

  if (limit === true) {
    window.location.href = '/projects';
  }
  pushNotification('System:', response, '/static/favicon.ico')
});