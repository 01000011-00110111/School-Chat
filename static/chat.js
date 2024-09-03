/* eslint-disable no-unused-vars */
/* eslint-disable no-undef */
// Copyright (C) 2023, 2024  cserver45, cseven
// License info can be viewed in main.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat

socket.on("message_chat", (message) => {
    renderChat((message));
});

socket.on("chat_muted", (user_perm) => {
    if (user_perm[0] === "Debugpass" || user_perm[0] === "adminpass" || user_perm[0] === "modpass") {
        null
    } else {
        const send_button = document.getElementById("send");

        message.disabled = true;
        message.placeholder = "You can't chat in this room";
        send_button.disabled = true;
    }
});

socket.on("chat_unmuted", () => {
    const send_button = document.getElementById("send");

    message.disabled = false;
    message.placeholder = "type your message here";
    send_button.disabled = false;
})

socket.on("troll", (message, ID) => {
    renderChat(message, ID);
    var audio = new Audio('static/airhorn_default.wav');
    audio.play();
});

socket.on("pingTime", (time, ID) => {
    socket.emit('pingtest', time, ID);
});

socket.on("force_room_update", (_statement) => {
    userid = getCookie("Userid")
    socket.emit("get_rooms", userid);
});

socket.on("reset_chat", (who, ID) => {
    if (ID === window.sessionStorage.getItem('ID')) {
        let chatDiv = document.getElementById("chat");
        if (who === "admin") {
            chatDiv.innerHTML = "[SYSTEM]: <font color='#ff7f00'>Chat reset by an admin.</font><br>";
        } else if (who === 'owner/mod') {
            chatDiv.innerHTML = "[SYSTEM]: <font color='#ff7f00'>Chat reset by this chat rooms Owner or Mod.</font><br>"
        } else if (who === "priv") {
            chatDiv.innerHTML = "[SYSTEM]: <font color='#ff7f00'>Chat reset by a private chat user.</font><br>";
        } else if (who === "auto") {
            chatDiv.innerHTML = "[SYSTEM]: <font color='#ff7f00'>Chat reset by automatic wipe system.</font><br>";
        }
    }
});

  

function runStartup() {
    socket.emit('get_theme', getCookie('Theme'))
    if (!window.sessionStorage.getItem("ID")) {
        window.sessionStorage.setItem("ID", 'ilQvQwgOhm9kNAOrRqbr');
    }
    if (!window.sessionStorage.getItem('private')) {
        changeRoom(window.sessionStorage.getItem("ID"))
    } else {
        // socket.emit('private_connect', getCookie('Userid'), user, window.sessionStorage.getItem('ID'))
        changeRoom('ilQvQwgOhm9kNAOrRqbr')
    }
    userid = getCookie("Userid")
    document.getElementById("pfpmenu").src = getCookie("Profile");
    socket.emit("get_rooms", userid);
}

socket.on("roomsList", (result, permission) => {
    let newline = "<br>"
    let rooms = "";
    let RoomDiv = document.getElementById("ChatRoomls");
    for (room of result) {
        if (permission != 'locked') {
        rooms = rooms + `<hr id="room_bar"><a id="room_names" style="color: ${theme['sidenav-a-color']}; background: ${theme['sidenav-a-background']}" onclick=changeRoom("${room.vid}")>/` + room.name + '</a><hr id="room_bar">';
        } else {
            rooms = '<hr id="room_bar">verify to have access to chat rooms<hr id="room_bar">'
            changeRoom('zxMhhAPfWOxuZylxwkES')
          }
    }
    RoomDiv["innerHTML"] = rooms;
    // for (room of result) {CheckIfExist(result);}
});

function CheckIfExist(_params) {
    if (window.sessionStorage.getItem("ID") != room.vid) {
        changeRoom('ilQvQwgOhm9kNAOrRqbr')
    } else {return}
}

socket.on("room_data", (data) => {
    // console.log(data)
    window.sessionStorage.setItem("ID", data['roomid']);
    window.sessionStorage.setItem("private", 'false')
    let newline = "<br>";
    let chatDiv = document.getElementById("chat");
    // update the url when the room is changed.
    let room_cat = window.location.href.split("/")[3];
    window.history.replaceState({"pageTitle": `${data['name']} - Chat`}, "", `/${room_cat}/${data['name']}`);
    roomname = document.getElementById("RoomDisplay").innerHTML = '/'+data['name'];
    document.title = `/${data['name']} - Chat`;
    let chat = ""; 
    for (let messageObj of data['msg']) {
        chat = chat + messageObj + newline;
    }

    chatDiv["innerHTML"] = chat;
    window.scrollTo(0, chatDiv.scrollHeight);
});

socket.on("private_data", (data) => {
    // console.log(data)
    window.sessionStorage.setItem("ID", data['pmid'])
    window.sessionStorage.setItem("private", 'true');
    let newline = "<br>";
    let chatDiv = document.getElementById("chat");
    // update the url when the room is changed.
    let room_cat = window.location.href.split("/")[3];
    window.history.replaceState({"pageTitle": `Private Chat`}, "", `/${room_cat}/Private/${data['name']}`);
    roomname = document.getElementById("RoomDisplay").innerHTML = `Private Chat: ${data['name']}`;
    document.title = `/Private - ${data['name']}`;
    let chat = ""; 
    for (let messageObj of data['message']) {
        chat = chat + messageObj + newline;
    }

    chatDiv["innerHTML"] = chat;
    window.scrollTo(0, chatDiv.scrollHeight);
});

function changeRoom(room) {
    window.sessionStorage.setItem("ID", room);
    closeNav();
    setTimeout(activate_hyperlinks, 200)
    socket.emit('room_connect', room, getCookie("Userid"))
}


function openuserinfo(user) {
    socket.emit('private_connect', getCookie('Userid'), user, window.sessionStorage.getItem('ID'))
}

function getMessage() {
    let messageElement = document.getElementById("message");
    let message = messageElement["value"];
    messageElement["value"] = "";
    let hidden = false
    var admin = document.getElementById('send_as_admin');
    if (admin) {
        if (admin.checked) {
            hidden = true;
            message = '$sudo admin ' + message;
        }
    }
    sendMessage(message, hidden);
}

function sendMessage(message, hidden) {
    let user = getCookie('Username')
    let userid = getCookie('Userid')
    if (message === "") {
        return;
    }
    if (message.includes("$sudo song")) {
        hidden = true;
    }
    // later i'll implement hiding the cmd
    let chatDiv = document.getElementById("chat");
    // this is needed, because this goes over socketio, not a normal http request
    private = window.sessionStorage.getItem('private')
    ID = window.sessionStorage.getItem("ID")
    socket.emit('message_chat', user, message, ID, userid, private, hidden);

    window.scrollTo(0, chatDiv.scrollHeight);
}

const sudo_cmd_menu = document.getElementById("sudo_cmd_menu")

/**
 * Opens the sudo command menu and other text functions
 */
const open_command_menu = () => {
    sudo_cmd_menu.style.setProperty("display", "grid")
}

/**
 * Closes the sudo command menu and other text functions
 */
const close_command_menu = () => {
    sudo_cmd_menu.style.setProperty("display", "none")
}

/* This trigger the sudo command menu when you type the trigger word ($, @, &, &*) */
const sudo_button = document.querySelectorAll(".sudo_cmd_button")
message.addEventListener('input', (event) => {
    // const inputValue = message.value.trim();
    const commandPrefixes = ["$", "@", "&", "&*", "filter:"];

    let containsCommand = commandPrefixes.some(prefix => message.value.includes(prefix));

    if (containsCommand) {
        open_command_menu();
    } else if (!containsCommand) {
        close_command_menu();
    }
});

/* This closes the sudo command menu when you click the enter button */
message.addEventListener('keypress', (event) => {
    if (event.key === "Enter") {
        close_command_menu()
    }
});

/* This closes the sudo command menu when you click outside of the textinput */
message.addEventListener('focusout', (event) => {
    setTimeout(close_command_menu, 100)
});

/* This controls the button length letting js assign command_buttons and command_badges */
for (let index = 0; index < sudo_button.length; index++) {
    ul = document.getElementById("sudo_list");
    li = ul.getElementsByTagName('li');

    const command_tag = document.createElement('div');
    command_tag.classList.add(`${sudo_button[index].getAttribute("privilege")}`)
    command_tag.innerHTML = sudo_button[index].getAttribute("privilege")
    li[index].appendChild(command_tag)

    sudo_button[index].addEventListener('click', () => {
        message.value = `${sudo_button[index].getAttribute("trigger")}${sudo_button[index].getAttribute("command")}`;
        message.focus()
        close_command_menu()
    })
}

function search_commands() {
    // Declare variables
    var filter, ul, li, a, i, txtValue;
    filter = message.value.toLowerCase();
    ul = document.getElementById("sudo_list");
    li = ul.getElementsByTagName('li');
  
    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < li.length; i++) {
      a = li[i].getElementsByTagName("button")[0];
      txtValue = a.textContent || a.innerText;
      if (txtValue.toLowerCase().includes(filter)) {
        li[i].style.display = "";
      } else {
        li[i].style.display = "none";
      } if (message.value === "&*") {
        li[i].style.display = "";
      } if (message.value === `$filter{type:${sudo_button[i].getAttribute("privilege")}}`) {
        const command_badge = document.querySelectorAll(".user")
        for (let index = 0; index < command_badge.length; index++) {
            if (command_badge[index].innerHTML === "user") {
                li[i].style.display = "";
            }
        }
      } if (message.value === "color_change") {
        message.style.setProperty('animation', 'clr_typing 3s infinite')
      }
    }
}

/* This is a search filter that filters through the commands and hides the ones that don't match the search filters typed */
// function search_commands() {
//     // Declare variables
//     var filter, ul, li, a, i, txtValue;
//     filter = message.value.toLowerCase();
//     ul = document.getElementById("sudo_list");
//     li = ul.getElementsByTagName('li');
//     const variations = ["$", "@", "&"];
//     let bypass = false;
//     let actualFilter = '';
    
//     // Trim any leading or trailing whitespace from the filter
//     const trimmedFilter = filter.trim();
    
//     // Find the longest matching prefix
//     const prefix = variations.reduce((longest, current) => {
//         return trimmedFilter.startsWith(current) && current.length > longest.length ? current : longest;
//     }, "");
    
//     // Remove the prefix and any leading/trailing spaces
//     if (prefix) {
//         actualFilter = trimmedFilter.substring(prefix.length).trim();
//         if (variations.includes(trimmedFilter)) { // Check if the exact trimmed filter is one of the variations
//             bypass = true;
//         }
//     }
  
//     // Loop through all list items, and hide those who don't match the search query
//     if (!bypass) {
//     for (i = 0; i < li.length; i++) {
//         a = li[i].getElementsByTagName("button")[0];
//         txtValue = a.textContent || a.innerText;
//         if (txtValue.toLowerCase().indexOf(actualFilter) > -1) {
//             li[i].style.display = "";
//         } else {
//           li[i].style.display = "none";
//         } if (message.value === "&*") {
//           li[i].style.display = "";
//         } if (message.value === `$filter{type:${sudo_button[i].getAttribute("privilege")}}`) {
//           const command_badge = document.querySelectorAll(".user")
//           for (let index = 0; index < command_badge.length; index++) {
//               if (command_badge[index].innerHTML === "user") {
//                   li[i].style.display = "";
//               }
//           }
//         } if (message.value === "color_change") {
//           message.style.setProperty('animation', 'clr_typing 3s infinite')
//         }
//       }
//     }
//   }


// setInterval(BTMLog, 3000)

const disclaimer = (title, message, link) => {
    const disclaimer_backdrop = document.createElement('div');
    const disclaimer_body = document.createElement('div');
    const disclaimer_control_panel = document.createElement('div');
    const disclaimer_title = document.createElement('h2');
    const disclaimer_message = document.createElement('p');
    const back_button = document.createElement('button');
    const continue_button = document.createElement('button');

    disclaimer_title.innerHTML = title;
    disclaimer_message.innerHTML = `${message} ${link}`;
    back_button.innerHTML = "Stay here";
    continue_button.innerHTML = "Continue";

    disclaimer_backdrop.setAttribute("id", "disclaimer_background");
    disclaimer_body.classList.add("disclaimer");
    disclaimer_control_panel.classList.add("disclaimer_buttons");
    disclaimer_title.classList.add("disclaimer_title");
    continue_button.setAttribute("id", "continue_button");
    back_button.setAttribute("id", "stay_button");
    disclaimer_message.setAttribute("id", "message_body");

    document.body.appendChild(disclaimer_backdrop);
    disclaimer_backdrop.appendChild(disclaimer_body);
    disclaimer_body.appendChild(disclaimer_title);
    disclaimer_body.appendChild(disclaimer_message);
    disclaimer_body.appendChild(disclaimer_control_panel);
    disclaimer_control_panel.appendChild(back_button);
    disclaimer_control_panel.appendChild(continue_button);

    back_button.addEventListener('click', () => {
        disclaimer_backdrop.remove();
    });

    continue_button.addEventListener('click', () => {
        window.location.href = link;
    });
}

const hyperlinks = document.querySelectorAll('a');

const isValidUrl = urlString => {
    let url;
    try {
        url = new URL(urlString);
    }
    catch(e) {
        return false;
    }
    return url.protocol === "http:" || url.protocol === "https:";
};

const default_leave_msg = "You are about to leave this site. You clicked on a link that leads you to another site. Continue at your own risk. <br> <br>";

/**
 * This function activates the hyperlinks when chat is loaded,
 * This function takes no parameters.
 */
const activate_hyperlinks = () => {
    console.info("Chat hyperlinks activated")
    const chat_hyperlinks = chat.querySelectorAll('a');

    for (let index = 0; index < chat_hyperlinks.length; index++) {
        chat_hyperlinks[index].addEventListener('click', (event) => {
            if (isValidUrl(chat_hyperlinks[index].href)) {
                if (chat_hyperlinks[index].hostname === "www6.school-chat.us" || chat_hyperlinks[index].hostname === "localhost") {
                    null
                } else {
                    event.preventDefault();
                    disclaimer("You are leaving the School chat platform", default_leave_msg, chat_hyperlinks[index])
                };
            };
        });
    };
};

for (let index = 0; index < hyperlinks.length; index++) {
    hyperlinks[index].addEventListener('click', (event) => {
        if (isValidUrl(hyperlinks[index].href)) {
            if (hyperlinks[index].hostname === "www6.school-chat.us" || hyperlinks[index].hostname === "localhost") {
                null
            } else {
                event.preventDefault();
                disclaimer("You are leaving the School chat platform", default_leave_msg, hyperlinks[index])
            };
        };
    });
};

window.onload = () => {
    setTimeout(activate_hyperlinks, 100);
}

function renderChat(messages) {
    // console.log(messages)
    let newline = "<br>";
    let chatDiv = document.getElementById("chat");
    chatDiv["innerHTML"] = chatDiv["innerHTML"] + messages + newline;
    activate_hyperlinks();
}


function checkKey() {
    if (event.key === "Enter") {
        getMessage();
    }
}