console.log("")

// This function requests the server send it a full chat log
function loadChat() {
  ajaxGetRequest("/chat", renderChat);
}

// This function sends the server the new message and receives
// the full chat log in response
function sendMessage(user_name){
  // Get an object representing the text box
  let messageElement = document.getElementById("message");
  // Save the message text 
  let message = messageElement["value"];
  // Let the user "see" the message was sent by clearing the textbox
  messageElement["value"] = "";

  if (message === "") {
    return
  } else if (message === " ") {
    return
  } else if (message === "  ") {
    return
  }
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
  chatDiv["innerHTML"] = chat;
}


function checkKey(user_name) {
  // Check if the enter key is pressed when typing
  
  if (event.key === "Enter") {
    sendMessage(user_name);
  }
}