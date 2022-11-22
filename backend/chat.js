  // This function requests the server send it a full chat log
function loadChat() {
  ajaxGetRequest("/chat", renderChat);
}

// This function sends the server the new message and receives
// the full chat log in response
function sendMessage(){
  // Get an object representing the text box (where we get the user and msg to get sent)
  let messageElement = document.getElementById("message");
  let userElement = document.getElementById("user");
  // Save the message text 
  let message = messageElement["value"];
  let user_name = userElement["value"];
  let isCmd = is_cmd(message)
  let isMuted = is_user_muted(user_name);

  // check for blank lines and muted members
  if (isMuted === true) {
    return
  } else if (user_name === "blank") {
    user_name = ""
  } else if (isCmd === true) {
    return
  } else if (user_name === "") {
    user_name = "NO NUTTY NOVEMBER"
  } else if (message === "") {
    return
  } else if (message === "") {
    return
  } else if (message === " ") {
    return
  } else if (message === "  ") {
    return
  } else if (message === "p") {
    return
  } else if (message === "P") {
    return
  //} else if (user_name === "user_name") {
    //user_name = "<FONT COLOR="#d4af37">user_name</FONT>"

  // Let the user "see" the message was sent by clearing the textbox
  messageElement["value"] = "";
  
  // We will send the message as a JSON encoding of an obejct.
  // This will simplify what is needed for future improvements
  let toSend = {"message": user_name.toString() + ": " + message};
  jsonString = JSON.stringify(toSend);
  // Send the JSON string to the server
  ajaxPostRequest("/send", jsonString, renderChat)
}
// This is the callback function used for both ajax requests
// It will be called by JS automatically whenever we get a response from the server
function renderChat(jsonData) {
  // Store the HTML needed to move to the next line. This makes the coding easier to read 
  let newline = "<br>";
  // Get an object representing the div displaying the chat (Connor add dumbed down version)
  let chatDiv = document.getElementById("chat");
  // Initialize our accumulator (Connor add dumbed down version)
  let chat = "";
  // Decode the JSON string the server sent to us
  let messages = JSON.parse(jsonData);
  // Loop through each message in the data sent from the server (Connor add dumbed down version)
  for (let messageObj of messages) {
    // Update our accumulator with the message's text (Connor add dumbed down version)
    chat = chat + messageObj["message"] + newline;
  }
  // Update the DIV to display all of the messages
  if (chatDiv["innerHTML"] != chat) {
    window.scrollTo(0, document.body.scrollHeight);
  }

  chatDiv["innerHTML"] = chat;
}


function checkKey() {
  // Check if the enter key is pressed when typing
  
  if (event.key === "Enter") {
    sendMessage();
  }
}