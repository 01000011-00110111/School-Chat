// Copyright (C) 2023, 2024  cserver45, cseven
// License info can be viewed in main.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat
let project = {}

let project_content = "";

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
const color_boxes = document.querySelectorAll('.color_picker');
const background_controller = document.getElementById("background_mode");
const media_importer = document.getElementById("media_importer");
const media_name = document.getElementById("media_name");
const media_label = document.getElementById("media_label");
const gradient_slider = document.getElementById("gradient_slider");
const gradient_slider_value = document.getElementById("gradient_slider_value");

// After this is the Theme & CSE code

function saveProject() {
  const online_users = document.querySelectorAll("#onlineList_user");
  theme = {
    'body': body.style.background,
    'chat-text': chat.style.color,
    'chat-background': message.style.background,
    'chat-color': message.style.color,
    'image-background': body.style.backgroundImage,
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
  socket.emit('save_project', project['themeID'], theme, theme_name1.value, false)
}

function publishProject() {
  const room_names = document.querySelectorAll("#room_names");
  const online_users = document.querySelectorAll("#onlineList_user");
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
    'image-background': body.style.backgroundImage,
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
  const drawer = document.getElementsByTagName('drawer');
  if (background === propertyStates[0]) {
    ColorPickers[0].style.display = "none";
    drawer[0].style.display = "none";
    drawer[1].style.display = "none";
  } else if (border === propertyStates[1]) {
    ColorPickers[0].style.display = "flex";
    drawer[0].style.display = "grid";
    drawer[1].style.display = "grid";
  }

  if (text === propertyStates[0]) {
    ColorPickers[2].style.display = "none";
    drawer[2].style.display = "none";
  } else if (border === propertyStates[1]) {
    ColorPickers[2].style.display = "flex";
    drawer[2].style.display = "grid";
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

  if (shadow === propertyStates[0] && border === propertyStates[0]) {
    drawer[3].style.display = "none";
  } else {
    drawer[3].style.display = "grid";
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
  const online_users = document.querySelectorAll("#onlineList_user");

  let colors = data.project
  let snav_iter = snavText.length;
  let extra_iter = extrabutton.length;
  theme_name1.value = data.name;
  document.title = `${data.name} - Theme Editor`;
  body.style.background = colors['body']
  chat.style.background = colors['body']
  chat.style.color = colors['chat-text']
  body.style.backgroundImage = colors['image-background']
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

const gradient_div = document.getElementById("gradient_div");
const gradient_text = document.getElementById("gradient_text");
const gradient_icon = document.getElementById("gradient_mode_button");
const colorMode = ["Solid", "Gradient", "Image"];
var currentColorMode;

function isGradient(value) {
  const gradientPattern = /^(linear-gradient|radial-gradient|repeating-linear-gradient|repeating-radial-gradient)\(/;
  return gradientPattern.test(value);
}

const setColorMode = (modeInt) => {
  currentColorMode = colorMode[modeInt];
}
setColorMode(0)

const enableGradient = () => {
  ColorPickers[1].style.display = "flex";
  setColorMode(1);
  gradient_slider.style.display = "block";
  gradient_slider_value.style.display = "block";
}

const disableGradient = () => {
  ColorPickers[1].style.display = "none";
  setColorMode(0);
  gradient_slider.style.display = "none";
  gradient_slider_value.style.display = "none";
}

const enableImages = () => {
  media_label.style.display = "block";
  setColorMode(2);
}

const disableImages = () => {
  media_label.style.display = "none";
}

const get_controller_state = () => {
  if (background_controller.options[background_controller.selectedIndex].value == "gradient_color") {
    enableGradient();
    disableImages();
  }

  if (background_controller.options[background_controller.selectedIndex].value == "solid_color") {
    disableGradient();
    disableImages();
  }

  if (background_controller.options[background_controller.selectedIndex].value == "background_image") {
    disableGradient();
    enableImages();
  }
}

background_controller.addEventListener('input', (event) => {
  get_controller_state();
});
get_controller_state();

const drawer = document.getElementsByTagName('drawer_header');
const drawerMode = ['open', 'closed'];
var currentDrawerMode = ['open', 'open', 'open'];

const setDrawerMode = (modeInt) => {
  currentDrawerMode = drawerMode[modeInt];
}

function openDrawer(index) {
  const drawerBox = document.getElementsByTagName("drawer")[index];
  const drawerButton = document.getElementsByClassName('drawer_dropdown_button')[index];
  const drawerBody = document.getElementsByTagName('drawer_content')[index];
  setDrawerMode(0);
  drawerButton.innerHTML = '<i class="fa-solid fa-chevron-down"></i>';
  drawerBox.style.minHeight = '174px';
  drawerBody.style.display = "grid";
}

function closeDrawer(index) {
  const drawerBox = document.getElementsByTagName('drawer')[index];
  const drawerButton = document.getElementsByClassName('drawer_dropdown_button')[index];
  const drawerBody = document.getElementsByTagName('drawer_content')[index];
  setDrawerMode(1);
  drawerButton.innerHTML = '<i class="fa-solid fa-chevron-up"></i>';
  drawerBox.style.minHeight = '0px';
  drawerBody.style.display = "none";
}

for (let index = 0; index < drawer.length; index++) {
  drawer[index].addEventListener('click', () => {
    if (currentDrawerMode === drawerMode[1]) {
      openDrawer(index);
    } else {
      closeDrawer(index);
    }
  })
}

gradient_slider.addEventListener('input', () => {
  gradient_slider_value.value = gradient_slider.value;
});

gradient_slider_value.addEventListener('input', () => {
  gradient_slider.value = gradient_slider_value.value;
});

const min = gradient_slider.min;
const max = gradient_slider.max;;
const slider_value = gradient_slider.value

gradient_slider.style.background = `linear-gradient(to right, #404a70 0%, #404a70 ${(slider_value-min)/(max-min)*100}%, #DEE2E6 ${(slider_value-min)/(max-min)*100}%, #DEE2E6 100%)`;

function extractRGBValues(rgbString) {
  const match = rgbString.match(/\d+/g);
  if (match) {
    return match.map(Number);
  }
  return [0, 0, 0];
}

function rgbToHex(rgb) {
  r = rgb[0]
  g = rgb[1]
  b = rgb[2]
  return "#" + (1 << 24 | r << 16 | g << 8 | b).toString(16).slice(1);
}

media_importer.addEventListener('input', (event) => {
  media_name.innerHTML = media_importer.files[0].name;
});

var shadow_user = "";

AllContent.forEach((element) => {
  element.addEventListener("click", (event) => {
    if (event.target.id != "" && currentSelection === "Edit") {
      OpenProperties();

      var SelectedLayer = event.target.id;
      const ColorBox = document.getElementById("body-color");
      const gradientColor = document.getElementById("2nd-body-color")
      const textColor = document.getElementById("text-color");
      const borderColor = document.getElementById("border-color");
      const shadowColor = document.getElementById("shadow-color");
      const ColorDisplay = document.getElementsByClassName("ColorDisplay");
      menuOwner.innerHTML = SelectedLayer;

      switch(SelectedLayer) {
        case "topbar":
          setProperties("enabled", "enabled", "enabled", "disabled");
          break;
        case "chat":
          setProperties("enabled", "enabled", "disabled", "disabled");
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
        case "onlineList_user":
          setProperties("disabled", "enable", "disabled", "disabled");
          break;
        case "RoomDisplay":
          setProperties("disabled", "enable", "disabled", "disabled");
          break;
        case "topleft":
          setProperties("disabled", "enable", "disabled", "disabled");
          break;
        case "message":
          setProperties("enabled", "enabled", "disabled", "disabled");
        break;
        case "send":
          setProperties("enabled", "enabled", "disabled", "disabled");
          break;
        case "pfpmenu":
          setProperties("disabled", "disabled", "disabled", "disabled");
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
        layer = document.getElementById(`${SelectedLayer}`)
        if (isGradient(layer.style.background)) {
            var c1 = layer.style.background
            .split(',')
            .map(color => color.trim())
            .slice(1)
            .join(', ')
            .replace(/\)\)+/, ')')
            .split('), ')
            .map((color, index, array) => index === array.length - 1 ? color : color + ')')
            .map(color => color.trim());
          // }
          c0 = rgbToHex(extractRGBValues(c1[0]))
          c1 = rgbToHex(extractRGBValues(c1[1]))
          setColorMode(1)
          enableGradient()
        } else {
          var c0 = rgbToHex(extractRGBValues(layer.style.background));
          var c1 = rgbToHex(extractRGBValues(layer.style.background));
          setColorMode(0)
          disableGradient()
        }
        const c2 = rgbToHex(extractRGBValues(layer.style.color));
        const c3 = rgbToHex(extractRGBValues(layer.style.boxShadow.slice(layer.style.boxShadow)))
        const c4 = rgbToHex(extractRGBValues(layer.style.borderColor));

        ColorDisplay[0].style.background = c0
        ColorDisplay[1].style.background = c1
        ColorDisplay[2].style.background = c2
        ColorDisplay[3].style.background = c3
        ColorDisplay[4].style.background = c4

        color_inputs[0].value = c0
        color_inputs[1].value = c1
        color_inputs[2].value = c2
        color_inputs[3].value = c3
        color_inputs[4].value = c4

        ColorBox.value = c0
        gradientColor.value = c1
        textColor.value = c2
        shadowColor.value = c3
        borderColor.value = c4
      };

          fetchColors();

          for (let index = 0; index < color_inputs.length; index++) {
            color_inputs[index].addEventListener('focusout', (event) => {
              if (isGradient(document.getElementById(`${SelectedLayer}`).style.background)) {
                color = document.getElementById(SelectedLayer).style.background
              .split(',')
              .map(color => color.trim())
              .slice(1)
              .join(', ')
              .replace(/\)\)+/, ')')
              .split('), ')
              .map((color, index, array) => index === array.length - 1 ? color : color + ')')
              .map(color => color.trim());
                const c0 = rgbToHex(extractRGBValues(document.getElementById(`${SelectedLayer}`).style.background));
                const c1 = rgbToHex(extractRGBValues(document.getElementById(`${SelectedLayer}`).style.background));
                ColorBox.value = c0
                gradientColor.value = c1
              } else {
                ColorBox.value = color_inputs[0].value
              }
              textColor.value = color_inputs[2].value
              document.getElementById(SelectedLayer).style.boxShadow = color_inputs[3].value
              borderColor.value = color_inputs[4].value
              fetchColors();
            })
          }

      for (let index = 0; index < color_boxes.length; index++) {
        color_boxes[index].addEventListener('input', (event) => {
          ColorDisplay[index].style.background = color_boxes[index].value
          color_inputs[index].value = color_boxes[index].value
        })
      }

      media_importer.addEventListener('input', (event) => {
        apply_changes();
      });

      gradient_slider.oninput = function() {
        apply_changes();
      };

      const apply_changes = () => {
        if (SelectedLayer == menuOwner.innerHTML) {

          switch (SelectedLayer) {
            case "topbar":
              shadow_user = "0px -1px 44px 15px"
              break;
            case "activenav":
              shadow_user = "10px 20px 17px 16px"
              break; 
            default:
              shadow_user = ""
              break;
          }
        
          if (SelectedLayer === "online_buttons") {
            const online_buttons = document.querySelectorAll("#online_buttons");
            for (let index = 0; index < online_buttons.length; index++) {
              online_buttons[index].style.color = textColor.value;
            }
          }

          switch (currentColorMode) {
            case 'Solid':
              document.getElementById(SelectedLayer).style.setProperty('background', ColorBox.value);
              document.getElementById(SelectedLayer).style.setProperty('color', textColor.value);
              document.getElementById(SelectedLayer).style.setProperty('border-color', borderColor.value);
              document.getElementById(SelectedLayer).style.boxShadow = `${shadow_user} ${shadowColor.value}`;
              break;
            
            case 'Gradient':
              document.getElementById(SelectedLayer).style.setProperty('background', `linear-gradient(${gradient_slider.value}deg, ${ColorBox.value}, ${gradientColor.value})`);
              document.getElementById(SelectedLayer).style.setProperty('color', textColor.value);
              document.getElementById(SelectedLayer).style.setProperty('border-color', borderColor.value);
              document.getElementById(SelectedLayer).style.boxShadow = `${shadow_user} ${shadowColor.value}`;
              fetchColors();
              break;

            case 'Image':
              document.getElementById(SelectedLayer).style.setProperty('background-image', `url("${media_importer.value}")`)
              document.getElementById(SelectedLayer).style.setProperty('color', textColor.value)
              document.getElementById(SelectedLayer).style.setProperty('border-color', borderColor.value)
              document.getElementById(SelectedLayer).style.boxShadow = `${shadow_user} ${shadowColor.value}`;
              break;
          }

          function Update() {
            if (SelectedLayer === 'chat') {
              body.style.background = chat.style.background;
            } 
            if (SelectedLayer === 'room_names') {
              rooms = document.querySelectorAll('#room_names');
              extra = document.getElementsByClassName('extrabuttons');
              for (let index = 0; index < rooms.length; index++) {
                rooms[index].style.background = ColorBox.value;
                rooms[index].style.color = textColor.value;        
              }
              for (let index = 0; index < extra.length; index++) {
                extra[index].style.background = ColorBox.value;
                extra[index].style.color = textColor.value;        
              }
            }
          };
            Update();
        };
      };

      for (let index = 0; index < color_boxes.length; index++) {
        color_boxes[index].addEventListener('input', (event) => {
          apply_changes();
        });    
      }
      /////
    }
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
  project_content = JSON.stringify(theme);
  open_project(theme);
  sessionStorage.setItem('editing', theme['themeID']);
});

socket.on('response', (response, limit) => {
  if (limit === true) {
    window.location.href = '/projects';
  }
  pushNotification('System:', response, '/static/favicon.ico')
});

function download(filename, text) {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}

document.getElementById('export_project_button').addEventListener('click', () => {
  download(`${theme_name1.value}.themifyProj`, project_content);
});