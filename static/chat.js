// This function requests the server send it a full chat log
function loadChat() {
  ajaxGetRequest("/chat", renderChat); 
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


// stuff to run at startup
function runStartup() {
  // get commands/command definitions
  ajaxGetRequest("/commands", save_cmd_list);
  ajaxGetRequest("/cmdDef", save_cmd_def);
  // (should) scroll to the bottom (but doesen't prob because of timing with load_chat)
  window.scrollTo(0, document.body.scrollHeight);
  // set styles because we dont use style sheets for colors anymore (unless static colors)
  setInterval(loadChat,3000);
  // add the username currently in a cookie unless there is none
  whichEvent(getCookie("theme"));
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
  let unsafeMessage = messageElement["value"];
  let user_name = userElement["value"];
  let profile_picture = profileElement["value"]
  let role = roleElement["value"]
  let user_color = userColorElement["value"];
  let message_color = messageColorElement["value"];
  let role_color = roleColorElement["value"]
  let isMuted = is_user_muted(user_name);

  // just so nothing gets overritten in cookies, is has to be up here
  document.cookie = "username=" + user_name + "; path=/";
  document.cookie = "profile_picture=" + profile_picture + "; path=/";
  document.cookie = "user_color=" + user_color + "; path=/";
  document.cookie = "message_color=" + message_color + "; path=/";
  document.cookie = "role_color=" + role_color + "; path=/";
  document.cookie = "role=" + role + "; path=/";
  
  // stupid long replace tree that doesent even work atm // then get it working!!
  let message = unsafeMessage// .replace(/&/g, "&").replace(/</g, "<").replace(/>/g, ">").replace(/"/g, '"').replace(/'/g, "'");

  // good idea to escape js anyway from here
  let isCmd = is_cmd(message);
  let profile_img = "<img style='max-height:25px; max-width:25px; overflow: hidden' src='" + profile_picture + "'></img>";

  //for popup temp fix too tired to make it better
  if 
  //
  
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
  }

  // role Founder Cserver
  // role Founder C7
  // the stupid long user_name check
  // should be on server side to be honest, but then we have to parse the string
  // on the server side
  /*if (user_name === "") {
      user_name = "Anonymous";
  } else if  (user_name === "Owen ") {
      user_name = "Owen";
  } else if (user_name === "Owen") {
    return;
  } else if (user_name === "Admin" || user_name === "admin" || user_name === "[admin]" || user_name === "[admin]" || user_name === "[ADMIN]") {
    return;
  } else if  (user_name === "Dev EReal") {
      user_name = "Dev E";
  } else if  (user_name === "Dev E") {
    return;
  } else if  (user_name === "cserverReal") {
      user_name = "cserver";
  } else if  (user_name === "cserver") {
    return;
  } else if (user_name === "SYSTEM" || user_name === "[SYSTEM]") {
    return;
  }*/
  
  // Let the user "see" the message was sent by clearing the textbox
  messageElement["value"] = "";
  // We will send the message as a JSON encoding of an obejct.
  // This will simplify what is needed for future improvements
  // add this in later by changing message to user_color_name
  let user_color_name = "<font color='" + user_color + "'>" + user_name + "</font>";
  let message_color_send = "<font color='" + message_color + "'>" + message + "</font>";
  let role_color_send = "<font color='" + role_color + "'>" + role + "</font>";
  // add profile_picture before user_name after I figure out how to limit how big an image is // i know how
  // still need user chooseable colors, will add to github issue tracker
  if (role === "") {
    let toSend = {"message": profile_picture + user_color_name.toString() + " - " + message_color_send};
    jsonString = JSON.stringify(toSend);
    ajaxPostRequest("/send", jsonString, renderChat);
  } else {
    let toSend = {"message": profile_picture + user_color_name.toString() + " (" + role_color_send + ")" + " - " + message_color_send};
    jsonString = JSON.stringify(toSend);
    ajaxPostRequest("/send", jsonString, renderChat);
  }
}


// This is the callback function used for both ajax requests
// It will be called by JS automatically whenever we get a response from the server
function renderChat(jsonData) {
  // Store the HTML needed to move to the next line. This makes the coding easier to read
  let newline = "<br>";
  // Get an object representing the div displaying the chat
  let chatDiv = document.getElementById("chat");
  // Initialize our accumulator
  let chat = "";
  // Decode the JSON string the server sent to us
  let messages = JSON.parse(jsonData);
  // Loop through each message in the data sent from the server
  for (let messageObj of messages) {
    // Update our accumulator with the message's text
    chat = chat + messageObj["message"] + newline;
  }
  // Update the DIV to display all of the messages
  //if (chatDiv["innerHTML"] != chat) {
  //  window.scrollTo(0, document.body.scrollHeight);
  //}
  // untill i can figure out what breaks the autoscroll in chat (maybe photos?), itll only go to bottom on page load

  chatDiv["innerHTML"] = chat;
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
  }
}

//The message text color dropdown button

function DropdownTXTtheme() {
  document.getElementById("DropdownTXT").classList.toggle("showTXT");
}

window.onclick = function(event) {
  if (!event.target.matches('.dropbtnTXT')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('showTXT')) {
        openDropdown.classList.remove('showTXT');
      }
    }
  }
}
