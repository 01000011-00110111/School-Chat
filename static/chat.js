// define socketio connection
const socket = io();

// add messages as they are recieved
socket.on("message_chat", (message) => {
  renderChat(message);
});

socket.on("reset_chat", (who) => {
  let chatDiv = document.getElementById("chat");
  if (who === "admin") {
    chatDiv["innerHTML"] = "[SYSTEM]: <font color='#ff7f00'>Chat reset by a admin.</font><br>"
  } else if (who === "auto") {
    chatDiv["innerHTML"] = "[SYSTEM]: <font color='#ff7f00'>Chat reset by automatic wipe system.</font><br>"
  }
});

// This function requests the server send it a full chat log
function loadChat() {
  ajaxGetRequest("/chat", loadChatStartup); 
}

// get specific cookie value
function getCookie(name) {
    name = name + "=";
    var cookies = document.cookie.split(';');
    for(var i = 0; i <cookies.length; i++) {
        var cookie = cookies[i];
        while (cookie.charAt(0)==' ') {
            cookie = cookie.substring(1);
        }
        if (cookie.indexOf(name) == 0) {
            return cookie.substring(name.length,cookie.length);
        }
    }
    return "";
}

// the startup for cookies after the first time
function runCheckStartup() {
  whichEvent(getCookie('theme'));
  access = getCookie("access");
  if (access === 'true') {
    runStartup();
    checkMsgBox();
    
  } else {
    // mush be here, otherwise popup could be bypased
    let message_box = document.getElementById('message');
    let send = document.getElementById('send');
    let sidenav = document.getElementById('topleft');
    sidenav.disabled = true;
    send.disabled = true;
    message_box.disabled = true;
  } // else DIE
}


// what happens if you don't agree to the rules
function runLimitedStartup() {
  runStartup();

  // lock the abbility to type in chat
  let message_box = document.getElementById('message');
  let send = document.getElementById('send');
  let sidenav = document.getElementById('topleft');
  sidenav.disabled = true;
  send.disabled = true;
  message_box.disabled = true;
  // let access = 'false'
  document.cookie = "access=" + access + "; path=/";
}

// stuff to run at startup and what happens when you do agree to the rules
function runStartup() {
  document.cookie = "access=" + access + "; path=/";
  socket.on("connect", () => {
    socket.send("John doe knows all");
  });
  // get commands/command definitions (never been used, probably never will)
  ajaxGetRequest("/commands", save_cmd_list);
  ajaxGetRequest("/cmdDef", save_cmd_def);
  // load previous chat messages
  loadChat();
  // add the username currently in a cookie unless there is none
  let userElement = document.getElementById("user"); 
  let user_color = document.getElementById("user_color");
  let message_color = document.getElementById("message_color");
  let role_color = document.getElementById("role_color");
  let roleElement = document.getElementById("role");
  user_color["value"] = getCookie("user_color");
  message_color["value"] = getCookie("message_color");
  role_color["value"] = getCookie("role_color");
  roleElement["value"] = getCookie("role");
  userElement["value"] = getCookie("username");
  // remove when popup is implemented
  whichEvent(getCookie("theme"));
}

function checkMsgBox() {
  // make sure message box is fine after accepting terms
  // makes sure that message box and send button are not disabled
  let message_box = document.getElementById('message');
  let send = document.getElementById('send');
  let sidenav = document.getElementById('topleft');
  sidenav.disabled = false;
  send.disabled = false;
  message_box.disabled = false;
}

function runCheckReset(message) {
  console.log(message)
  if (message === "[SYSTEM]: <font color='#ff7f00'>Chat reset by a admin.</font>") {
    let chatDiv = document.getElementById("chat");
    console.log("here")
    chatDiv["innerHTML"] = "[SYSTEM]: <font color='#ff7f00'>Chat reset by a admin.</font><br>"
    console.log(message)
    return "true";//
  } 
}

// This function sends the server the new message and receives
// the full chat log in response
function sendMessage() {
  // Get an object representing the text box (where we get the user and msg to get sent)
  let messageElement = document.getElementById("message");
  let userElement = document.getElementById("user");
  let profileElement = document.getElementById("profile_picture");
  let roleElement = document.getElementById("role")
  let messageColorElement = document.getElementById("message_color");
  let roleColorElement = document.getElementById("role_color");
  let userColorElement = document.getElementById("user_color");  
  
  // Save the message text 
  let message = messageElement["value"];
  let user_name = userElement["value"];
  let profile_picture = profileElement["value"]
  let role = roleElement["value"]
  let user_color = userColorElement["value"];
  let message_color = messageColorElement["value"];
  let role_color = roleColorElement["value"]        
  let isMuted = is_user_muted(user_name);


  //if (theme === 'light' && )
  if (user_color === "#000000") {
    user_color = "#ffffff"
  }
  if (message_color === "#000000") {
    message_color = "#ffffff"
  }
  if (role_color === "#000000") {
    role_color = "#ffffff"
  }

  // just so nothing gets overritten in cookies, is has to be up here
  document.cookie = "username=" + user_name + "; path=/";
  document.cookie = "profile_picture=" + profile_picture + "; path=/";
  document.cookie = "user_color=" + user_color + "; path=/";
  document.cookie = "message_color=" + message_color + "; path=/";
  document.cookie = "role_color=" + role_color + "; path=/";
  document.cookie = "role=" + role + "; path=/";

  // good idea to escape js anyway from here
  let isCmd = is_cmd(message);
    let profile_img = "<img style='max-height:25px; max-width:25px; overflow: hidden' src='" + profile_picture + "'></img>";
  
  
  if (isMuted === true) {
    return;
  } else if (isCmd === true) {
    messageElement["value"] = "";
    return;
  } else if (message === "") {
    return;
  } else if (message === " ") {
    return;
  } else if (message === "  ") {
    return;
  } else if  (user_name === "Shatla") {
      role = 'Cool Owen GF';
  } else if (role === 'Cool Owen' || role === 'cool owen' || role === 'Cooler Owen' || role === 'cooler owen' || role === 'Coolish Owen' || role === 'coolish owen') {
    role = 'Lameish Owen'
  }

  // role Founder Cserver
  // role Founder C7
  // the stupid long user_name check
  // now implemented on server side
  // took much longer than it should have
  // Let the user "see" the message was sent by clearing the textbox
  messageElement["value"] = "";
  // We will send the message as a JSON encoding of an obejct.
  // This will simplify what is needed for future improvements
  // add this in later by changing message to user_color_name
  // console.log(user_color)
  let user_color_name = "<font color='" + user_color + "'>" + user_name + "</font>";
  let message_color_send = "<font color='" + message_color + "'>" + message + "</font>";
  let role_color_send = "<font color='" + role_color + "'>" + role + "</font>";
  // add profile_picture before user_name after I figure out how to limit how big an image is // i know how
  // still need user chooseable colors, will add to github issue tracker
  if (role === "") {
    let toSend = profile_img + user_color_name.toString() + " - " + message_color_send
    socket.emit('message_chat', toSend);
    return;
  } else {
    let toSend = profile_img + user_color_name.toString() + " (" + role_color_send + ")" + " - " + message_color_send
    socket.emit('message_chat', toSend);
    return;
  }
}

// ran at startup so you get previous messages
function loadChatStartup(jsonString) {
  let newline = "<br>";
  // Get an object representing the div displaying the chat
  let chatDiv = document.getElementById("chat");
  let chat = "";
  let messages = JSON.parse(jsonString);
  // Loop through each message in the data sent from the server
  for (let messageObj of messages) {
    // Update our accumulator with the message's text
    chat = chat + messageObj["message"] + newline;
  }

  chatDiv["innerHTML"] = chat;
  window.scrollTo(0, document.body.scrollHeight);
}

// This is the callback function used for both ajax requests
// It will be called by JS automatically whenever we get a response from the server
function renderChat(messages) {
  // Store the HTML needed to move to the next line. This makes the coding easier to read
  let newline = "<br>";
  // Get an object representing the div displaying the chat
  let chatDiv = document.getElementById("chat");

  chatDiv["innerHTML"] = chatDiv["innerHTML"] + messages + newline;
}


function checkKey() {
  // Check if the enter key is pressed when typing
  if (event.key === "Enter") {
    sendMessage();
  }
}

  // Nav menu //
 //set the size of the Nav
function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {          
  document.getElementById("mySidenav").style.width = "0";
}

function devopenNav() {
  document.getElementById("devSidenav").style.width = "550px";
  document.getElementById("devSidenav").style.paddingLeft = "5%";
}

function devcloseNav() {          
  document.getElementById("devSidenav").style.width = "0";
  document.getElementById("devSidenav").style.paddingLeft = "0";
}

/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function dropdownTheme() {
  document.getElementById("myDropdown").classList.toggle("show");
}

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
  } else if (!event.target.matches('.mySidenav')) {
    // whenever i can get sidenav-content (hidden element) implemented in css
    // simillar to dropdown-content, but with some widths changed and other stuff
    //var dropdowns = document.getElementsByClassName("dropdown-content");
    //var i;
    //for (i = 0; i < dropdowns.length; i++) {
    //  var openDropdown = dropdowns[i];
    //  if (openDropdown.classList.contains('show')) {
    //    openDropdown.classList.remove('show');
    //  }
    //}
  } /*else if (!event.target.matches('.dropbtnTXT')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('showTXT')) {
        openDropdown.classList.remove('showTXT');
      }
    }
  } */ //do we need this?
}

//The message text color dropdown button

function DropdownTXTtheme() {
  document.getElementById("DropdownTXT").classList.toggle("showTXT");
}
