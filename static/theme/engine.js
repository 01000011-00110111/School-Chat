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
let code = document.getElementById("code");
let editmodeText = document.getElementById("editmodeText");

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
const snavText = document.getElementById("room_names");
const roomText = document.getElementById("RoomDisplay");
const roomBar = document.getElementById("room_bar");
const topbar = document.getElementById("topbar");
// const hrElement = document.querySelector("hr");

const ColorPickers = document.querySelectorAll("#ColorPicker");

// After this is the Theme & CSE code


function saveProject() {
  theme = {
    'body': body.style.background,
    'chat-text': chat.style.color,
    'chat-background': message.style.background,
    'chatbox-background': chatbox.style.background,
    'sides-text': sides.style.color,
    'sides-background': sides.style.background,
    'sidebar-background': sidebar.style.background,
    'sidebar-boxShadow': sidebar.style.boxShadow,
    'sidebar-border': sidebar.style.borderColor,
    'sidebar-text': sidebar.style.color,
    'topleft-background': topleft.style.background,
    'topleft-text': topleft.style.color,
    'send-background': send.style.background,
    'send-text': send.style.color,
    // 'sidenav-background': sidenav.style.background,
    // 'sidenav-color': snavText.style.color,
    'sidenav-background': sidenav.style.background,
    'sidenav-text': sidenav.style.color,
    // 'sidenav-a-background': snavText.style.background[0],
    // 'sidenav-a-color': snavText.style.color[0],
    'roomText-text': roomText.style.color,
    'topbar-background': topbar.style.background,
    'topbar-boxShadow': topbar.style.boxShadow,
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
  theme = {
    'body': body.style.background,
    'chat-text': chat.style.color,
    'chat-background': message.style.background,
    'chatbox-background': chatbox.style.background,
    'sides-text': sides.style.color,
    'sides-background': sides.style.background,
    'sidebar-background': sidebar.style.background,
    'sidebar-boxShadow': sidebar.style.boxShadow,
    'sidebar-border': sidebar.style.borderColor,
    'sidebar-text': sidebar.style.color,
    'topleft-background': topleft.style.background,
    'topleft-text': topleft.style.color,
    'send-background': send.style.background,
    'send-text': send.style.color,
    // 'sidenav-background': sidenav.style.background,
    // 'sidenav-color': snavText.style.color,
    'sidenav-background': sidenav.style.background,
    'sidenav-text': sidenav.style.color,
    // 'sidenav-a-background': snavText.style.background,
    // 'sidenav-a-color': snavText.style.color,
    'roomText-text': roomText.style.color,
    'topbar-background': topbar.style.background,
    'topbar-boxShadow': topbar.style.boxShadow,
  }
  // project.theme = theme
  // project.project = theme
  // project.name = theme_name1.value
  // project['status'] = 'public'
  socket.emit('save_project', project['themeID'], theme, theme_name1.value, true)
}

// socket.on()

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
    ColorPickers[1].style.dsplay = "none";
  } else if (border === propertyStates[1]) {
    ColorPickers[1].style.display = "flex";
  }

  if (shadow === propertyStates[0]) {
    ColorPickers[2].style.display = "none";
  } else if (border === propertyStates[1]) {
    ColorPickers[2].style.display = "flex";
  }

  if (border === propertyStates[0]) {
    ColorPickers[3].style.display = "none";
  } else if (border === propertyStates[1]) {
    ColorPickers[3].style.display = "flex";
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
  let colors = data.project
  let snav_iter = snavText.length;
  theme_name1.value = data.name
  body.style.background = colors['body']
  chat.style.color = colors['chat-text']
  message.style.background = colors['chat-background']
  chatbox.style.background = colors['chatbox-background']
  sides.style.color = colors['sides-text']
  sides.style.background = colors['sides-background']
  sidebar.style.background = colors['sidebar-background']
  sidebar.style.borderColor = colors['sidebar-border']
  sidebar.style.color = colors['sidebar-text']
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

var shadow_user = "";

AllContent.forEach((element) => {
  element.addEventListener("click", (event) => {
    if (event.target.id != "") {
      if (currentSelection === "Edit") {
        element.classList.toggle("active");

        menuOwner.innerHTML = event.target.id;

        OpenProperties();

        var SelectedLayer = event.target.id;
        const ColorBox = document.getElementById("body-color");
        const textColor = document.getElementById("text-color");
        const borderColor = document.getElementById("border-color");
        const shadowColor = document.getElementById("shadow-color");
        const LayerProperties = document.getElementById("LayerProperties");
        const LayerOpacity = document.getElementById("LayerOpacity");
        const Chat = document.getElementById("ChatMockup");

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
          default:
            setProperties("enabled", "enabled", "enabled", "enabled");
        } 


        const fetchColors = () => {
          document.getElementsByClassName("ColorDisplay")[0].style.background = document.getElementById(`${SelectedLayer}`).style.background;
          document.getElementsByClassName("ColorDisplay")[1].style.background = document.getElementById(`${SelectedLayer}`).style.color;
          document.getElementsByClassName("ColorDisplay")[2].style.background = document.getElementById(`${SelectedLayer}`).style.shadowColor;
          document.getElementsByClassName("ColorDisplay")[3].style.background = document.getElementById(`${SelectedLayer}`).style.borderColor;
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

            document.getElementById(SelectedLayer).style.background = ColorBox.value;
            document.getElementById(SelectedLayer).style.color = textColor.value;
            document.getElementById(SelectedLayer).style.borderColor = borderColor.value;
            document.getElementById(SelectedLayer).style.boxShadow = `${shadow_user} ${shadowColor.value}`;

            setInterval(Update, 100);

            function Update() {
              // event.target.style.background = ColorBox.value;
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
});

socket.on('response', (response, limit) => {
  console.log(response)

  if (limit === true) {
    window.location.href = '/projects';
  }
  pushNotification('System:', response, '/static/favicon.ico')
});