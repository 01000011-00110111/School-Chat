
// This function requests the server send it a full chat log
function loadChat() {
  ajaxGetRequest("/chat", renderChat); 
}

// get specific cookie value
function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      console.log(c.substring(name.length, c.length));
      return c.substring(name.length, c.length);
    }
  }
  return "";
}


// stuff to run at startup
function runStartup() {
  ajaxGetRequest("/commands", save_cmd_list);
  ajaxGetRequest("/cmdDef", save_cmd_def);
  window.scrollTo(0, document.body.scrollHeight);
  // set styles because we dont use style sheets for colors anymore (unless static colors)
  whichEvent();
  setInterval(loadChat,3000);
  let userElement = document.getElementById("user");
  console.log(getCookie("username"));
 // userElement["value"] = getCookie("username") 
}

// This function sends the server the new message and receives
// the full chat log in response
function sendMessage() {
  // Get an object representing the text box (where we get the user and msg to get sent)
  let messageElement = document.getElementById("message");
  let userElement = document.getElementById("user");
  // Save the message text 
  let unsafeMessage = messageElement["value"];
  let user_name = userElement["value"];
  let isMuted = is_user_muted(user_name);

  // just so nothing gets overritten in cookies, is has to be up here
  document.cookie = "username=" + user_name + "; path=/";

  // stupid long replace tree that doesent even work atm
  let message = unsafeMessage.replace(/&/g, "&").replace(/</g, "<").replace(/>/g, ">").replace(/"/g, '"').replace(/'/g, "'");

  // good idea to escape js anyway from here
  let isCmd = is_cmd(message);

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
  } else if  (user_name === "💲♓️🅰️ⓨ👢🅰") {
      message = '<font color="#db1690">' + "Cool Owen's GF- " + '</font>' + '<font color="#25C178">' + message + "</font>";
  } else if  (user_name === "Steven W") {
      message = '<font color="#1788E8">' + 'Aperture Scientist- ' + '</font>' + '<font color="#13D2CA">' + message + "</font>";
  } else if  (user_name === "🅾️〰️📧🇳 ") {
    message = '<font color="#1abd2d">' + 'Cool Owen- ' + '</font>' + '<font color="#ffd700">' + message + "</font>";
  } else if  (user_name === "Dev EReal") {
     message = '<font color="#ff8800">' + 'Founder C7- ' + '</font>' + '<font color="#08ff83">' + message + "</font>";
  } else if (user_name === "cserverReal") {
    message =  '<font color="#ff7f00">' + 'Founder Cserver- ' + '</font>' + '<font color="#ff430a">' + message + "</font>";
  }
  
  if (user_name === "") {
      user_name = "Anonymes";
  } else if  (user_name === "🅾️〰️📧🇳 ") {
      user_name = "🅾️〰️📧🇳";
  } else if (user_name === "🅾️〰️📧🇳") {
    return;
  } else if  (user_name === "Adm!n") {
      user_name = "Admin";
  } else if (user_name === "Admin") { //|| user_name === "admin") {
    return;
  } else if  (user_name === "Dev EReal") {
      user_name = "Dev E";
  } else if  (user_name === "Dev E") {
    return;
  } else if  (user_name === "cserverReal") {
      user_name = "cserver";
  } else if  (user_name === "cserver") {
    return;
  }
  
  // Let the user "see" the message was sent by clearing the textbox
  messageElement["value"] = "";
  // We will send the message as a JSON encoding of an obejct.
  // This will simplify what is needed for future improvements
  console.log(document.getElementById("user_name"));
  //let user_color = document.getElementById("user_color").style.color;
  //let user_color_name = "<font color='" + user_color + "'>" + user_name.toString() + "</font>";
  let toSend = {"message": user_name.toString() + ": " + message};
  jsonString = JSON.stringify(toSend);
  // Send the JSON string to the server
  ajaxPostRequest("/send", jsonString, renderChat);
}
  //the force send code need a better info here
function FsendMessage() {
  let messageElement = document.getElementById("message");
  let isCmd = is_cmd(message);
  messageElement["value"] = "";
  //console.log(document.getElementById("user_name"));
  let toSend = {"message": message};
  jsonString = JSON.stringify(toSend);
  ajaxPostRequest("/send", jsonString, renderChat);
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
  } else if (event.key === "Escape") {
    closeNav();
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

// checks if escape key is pressed when nav is open
// does not currently work, idk why
//function ESCkey() {
//  if (event.key === "Escape") {
   // closeNav();
  //}
//}

/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function myFunction() {
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