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
const snavText = sidenav.getElementsByTagName("a");
const roomText = document.getElementById("RoomDisplay");
const roomBar = document.getElementById("room_bar");
const topbar = document.getElementById("topbar");
// const hrElement = document.querySelector("hr");


// After this is the Theme & CSE code


function saveProject() {
  // theme = [
  //   body.style.background,
  //   chat.style.color,
  //   message.style.color,
  //   chatbox.style.background,
  //   sides.style.background,
  //   sidebar.style.background,
  //   sidebar.style.borderColor,
  //   sidebar.style.color,
  //   topleft.style.background,
  //   topleft.style.color,
  //   send.style.background,
  //   send.style.color,
  //   sidenav.style.background,
  //   sidenav.style.color,
  //   roomText.style.color,
  //   topbar.style.background,
  // ]
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
    'sidenav-a-background': snavText.style.background[0],
    'sidenav-a-color': snavText.style.color[0],
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
  project['theme'] = theme
  project['name'] = theme_name1.value
  socket.emit('save_project', project)
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
    'sidenav-a-background': snavText.style.background,
    'sidenav-a-color': snavText.style.color,
    'roomText-text': roomText.style.color,
    'topbar-background': topbar.style.background,
    'topbar-boxShadow': topbar.style.boxShadow,
  }
  project['theme'] = theme
  project['name'] = theme_name1.value
  project['status'] = 'public'
  socket.emit('save_project', project)
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
function setTheme(data) {
  let colors = data.theme
  let snav_iter = snavText.length;
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

// Work in progress
const properties = {
  "Background Color": "disabled",
  "Text Color": "disabled",
  "Border Color": "disabled",
  "Shadow Color": "disabled",
};

var shadow_user = "";

AllContent.forEach((element) => {
  element.addEventListener("click", (event) => {
    if (currentSelection === "Edit") {
      element.classList.toggle("active");

      menuOwner.innerHTML = event.target.id;

      OpenProperties();

      var SelectedLayer = event.target.id;
      const ColorBox = document.getElementById("body-color");
      const textColor = document.getElementById("text-color");
      const borderColor = document.getElementById("border-color");
      const shadowColor = document.getElementById("shadow-color")
      const LayerProperties = document.getElementById("LayerProperties");
      const LayerOpacity = document.getElementById("LayerOpacity");
      const Chat = document.getElementById("ChatMockup");


      document.getElementsByClassName("ColorDisplay")[0].style.background = document.getElementById(`${SelectedLayer}`).style.background;
      document.getElementsByClassName("ColorDisplay")[1].style.background = document.getElementById(`${SelectedLayer}`).style.color;
      document.getElementsByClassName("ColorDisplay")[2].style.background = document.getElementById(`${SelectedLayer}`).style.shadowColor;
      document.getElementsByClassName("ColorDisplay")[3].style.background = document.getElementById(`${SelectedLayer}`).style.borderColor;

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

          document.getElementById(SelectedLayer).style.background = ColorBox.value;
          document.getElementById(SelectedLayer).style.color = textColor.value;
          document.getElementById(SelectedLayer).style.borderColor = borderColor.value;
          document.getElementById(SelectedLayer).style.boxShadow = `${shadow_user} ${shadowColor.value}`;

          LayerProperties.addEventListener("click", (event) => {
            document.getElementById(SelectedLayer).style.display = "none";
          });

          setInterval(Update, 100);

          function Update() {
            // event.target.style.background = ColorBox.value;
            document.body.style.background = chat.style.background;
            Chat.style.background = chat.style.background;
            
            event.target.style.opacity = LayerOpacity.value + "%";
          };

          Update();
          
          document.getElementsByClassName("ColorDisplay")[0].style.background = document.getElementById(`${SelectedLayer}`).style.background;
          document.getElementsByClassName("ColorDisplay")[1].style.background = document.getElementById(`${SelectedLayer}`).style.color; 
          document.getElementsByClassName("ColorDisplay")[2].style.background = document.getElementById(`${SelectedLayer}`).style.boxShadow;  
          document.getElementsByClassName("ColorDisplay")[3].style.background = document.getElementById(`${SelectedLayer}`).style.borderColor;
        };
      });
    };
  });
});

document.title = theme_name1.value + " - Theme Editor";

theme_name1.addEventListener("focusout", (event) => {
  document.title = theme_name1.value + " - Theme Editor";
});

function isMobile() {
  var check = false;
  (function(a){
    if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))) 
      check = true;
  })(navigator.userAgent||navigator.vendor||window.opera);
  return check;
};

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