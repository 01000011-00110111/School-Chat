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
let BodyColor = document.getElementById("body-color");
let SidenavColor = document.getElementById("sn-color");
let SidesColor = document.getElementById("s-color");
let TextColor = document.getElementById("t-color");
let OnlineListColor = document.getElementById("oul-color");
let OnlineListTextColor = document.getElementById("oult-color");
let ChatBoxColor = document.getElementById("chb-color");
let SendButton = document.getElementById("sb-color");
let TopLeft = document.getElementById("snb-color");
let SidenavTextColor = document.getElementById("snt-color");
let BorderColor = document.getElementById("bdr-color");
let ShadowColor = document.getElementById("shd-color");
let TopbarColor = document.getElementById("tpb-color");
let TopbarTextColor = document.getElementById("tpbt-color");
let DropDownBorderColor = document.getElementById("tpbdr-color");
let TopbarShadowColor = document.getElementById("tpbs-color");
let theme_name1 = document.getElementById("n_name");
let theme_name2 = document.getElementById("themeNL");

let textbox1 = document.getElementById("textbox1");
let textbox2 = document.getElementById("textbox2");
let textbox3 = document.getElementById("textbox3");
let textbox4 = document.getElementById("textbox4");
let textbox5 = document.getElementById("textbox5");
let textbox6 = document.getElementById("textbox6");

let infobox = document.getElementById("info");

let Response = document.getElementById("Response");

let snbr = document.getElementById("sn-br");
let snwd = document.getElementById("sn-wd");

let applyButton = document.getElementById("applyButton");
let code = document.getElementById("code");
let editmodeText = document.getElementById("editmodeText");

// Don't be confused

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
const roomText = document.getElementById("room_text");
const roomBar = document.getElementById("room_bar");
const topbar = document.getElementById("topbar");
// const hrElement = document.querySelector("hr");


//   let sidenav = document.getElementsByClassName("sidenav")[0];
//   let snav_text = sidenav.getElementsByTagName("a");
//   let snav_iter = snav_text.length;
//   for (let i = 0; i < snav_iter; i++) {
//       snav_text[i].style.color = SidenavTextColor.value;
//   }
// }

// After this is the Theme & CSE code


// Fix this later
// function showcode() {
//   code.style.display = "grid";
//  const theme = `
//   const ${theme_name1.value} = [
//     "${body.style.background}",
//     "${chat.style.color}",
//     "${message.style.color}",
//     "${chatbox.style.background}",
//     "${sides.style.background}",
//     "${sidebar.style.background}",
//     "${sidebar.style.borderColor}",
//     "${sidebar.style.color}",
//     "${topleft.style.background}",
//     "${topleft.style.color}",
//     "${send.style.background}",
//     "${send.style.color}",
//     "${sidenav.style.background}",
//     "${sidenav.style.color}",
//     "",
//     "${topbar.style.background}"
//   ];
//   `

//   code.innerHTML = theme;
// }

function saveProject() {
  theme = [
    body.style.background,
    chat.style.color,
    message.style.color,
    chatbox.style.backgrund,
    sides.style.background,
    sidebar.style.background,
    sidebar.style.borderColor,
    sidebar.style.color,
    topleft.style.background,
    topleft.style.color,
    send.style.background,
    send.style.color,
    sidenav.style.background,
    sidenav.style.color,
    "",
    topbar.style.background,
  ]
  project = {
    "name": theme_name1.value,
    'author': [getCookie("Userid"), getCookie("DisplayName")],
    theme: theme,
    'status': 'private',
  }

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
function open_project(data) {
  let colors = data.theme
  BodyColor.style.background = colors[0]
  chat.style.color = colors[1]
  message.style.background = colors[2]
  chatbox.style.color = colors[3]
  sides.style.color = colors[4]
  sides.style.background = colors[5]
  sidebar.style.background = colors[6]
  sidebar.style.borderColor = colors[7]
  sidebar.style.color = colors[8]
  topleft.style.background = colors[9]
  topleft.style.color = colors[10]
  SendButton.style.background = colors[11]
  SendButton.style.color = colors[12]
  sidenav
  sidenav
  roomText.style.color = colors[15]
  topbar.style.backgrounda = colors[16]
};

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
          console.log(`${shadow_user} ${shadowColor.value}`)

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
  socket.emit('get_project', window.sessionStorage.getitem('editing'))
}

socket.on('set_theme', (theme) => {
  open_project(theme);
});