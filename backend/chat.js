// This function requests the server send it a full chat log
function loadChat() {
  ajaxGetRequest("/chat", renderChat);
}
// stuff to run at startup
function runStartup() {
  ajaxGetRequest("/commands", save_cmd_list);
  ajaxGetRequest("/cmdDef", save_cmd_def);
  window.scrollTo(0, document.body.scrollHeight);
  setInterval(loadChat,3000);
}
// This function sends the server the new message and receives
// the full chat log in response
function sendMessage() {
  // Get an object representing the text box (where we get the user and msg to get sent)
  let messageElement = document.getElementById("message");
  let userElement = document.getElementById("user");
  // Save the message text 
  let cmd_list = get_cmd_list();
  let message = messageElement["value"];
  let user_name = userElement["value"];
  let isCmd = is_cmd(message, cmd_list);
  let isMuted = is_user_muted(user_name);

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
      message = '<font color="#25C178">' + message + "</font>"
  } else if  (user_name === "Steven W") {
      message = '<font color="#13D2CA">' + message + "</font>"
  }

  if (user_name === "") {
    user_name = "Anonymes"
  } else if  (user_name === "T🅾️〰️📧🇳") {
    user_name = "🅾️〰️📧🇳"
  } else if (user_name === "🅾️〰️📧🇳") {
    return
  } else if  (user_name === "Adm!n") {
    user_name = "Admin"
  } else if (user_name === "Admin") {
    return
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
  console.log(chat);
  console.log(chatDiv["innerHTML"])
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
// set the size of the Nav
//function openNav() {
// document.getElementById("mySidenav").st//yle.width = "250px";
//}
//function closeNav() {
  
// document.getElementById("mySidenav").style.width = "0";
//}

// checks if escape key is pressed when nav is open
//function checkKey() {
  //if (event.key === "escape") {
  //  closeNav();
 // }
//}