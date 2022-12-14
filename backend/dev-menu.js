  // Dev menu js code to keep chat.js cleaner //

// send message as the user [SYSTEM]
function systemmessage() {
  // just bits and pieces from sendMessage
  let messageElement = document.getElementById("systemsendT");

  message = '<font color="#ff7f00">' + messageElement["value"] + '</font>'
  messageElement["value"] = "";
  let toSend = {"message": "[SYSTEM]: " + message};
  jsonString = JSON.stringify(toSend);
  // Send the JSON string to the server
  ajaxPostRequest("/force_send", jsonString, renderChat);
}

//the force send code need a better info here
function FsendMessage() {
  let messageElement = document.getElementById('fsendT');
  // 100% CPU usage lol on tablet lol
  //console.log(document.getElementById("user_name"));
  let toSend = {"message": "[Admin]: " + messageElement.value};
  jsonString = JSON.stringify(toSend);

  messageElement.value = "";
  // we use a diffrent endpoint, so it doesen't get blocked by the add_message function on the server end
  // also gets rid of a lot of checks inside add_message
  ajaxPostRequest("/force_send", jsonString, renderChat);
} 

// take a img url, and convert it into a img html tag
function sendImage() {
  let messageElement = document.getElementById("imagesendT")
  let toSend = {"message": "<img href='" + messageElement["value"] + "'></img>"};
  jsonString = JSON.stringify(toSend);

  messageElement["value"] = "";
  
  ajaxPostRequest("/send", jsonString, renderChat);
}

// get stats from the replit instance
function getStats() {
  ajaxGetRequest("/stats", dummyajax);
}

// lock/unlock chat helper functions
function lock_chat() {
  ajaxPostRequest("/lock", "1", dummyajax);
}

// unlocks chat
function unlock_chat() {
  ajaxPostRequest("/lock", "0", dummyajax);
}

// see comment inside function
function dummyajax(jsonData) {
  // dummy function so ajaxPostRequest doesent error out from no function callback
  return;
}
