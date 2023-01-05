  // Dev menu js code to keep chat.js cleaner and easy to read and find what you need//

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
  let messageElement = document.getElementById("sendimgT");
  let toSend = {"message": "<img src='" + messageElement["value"] + "'></img>"};
  jsonString = JSON.stringify(toSend);

  messageElement["value"] = "";
  
  ajaxPostRequest("/send", jsonString, renderChat);
}

// send a bunch of black lines to chat system
function testChatGC() {
  let toSend = {"message": '[SYSTEM]: <font color="#ff7f00">nothing to see here \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nnothing to see here\n</font>'};
  jsonString = JSON.stringify(toSend);
  ajaxPostRequest("/send", jsonString, renderChat);
}
//{"message": '[SYSTEM]: <font color="#ff7f00">nothing to see here \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n nothing to see here\n</font>'};

function EsendMessage() {
  // just bits and pieces from sendMessage
  let messageElement = document.getElementById("EventMSGT");

  message = '<font color="e54e40">' + messageElement["value"] + '</font>' + "</h3>"
  messageElement["value"] = "";
  let toSend = {"message": "<h3> [Event]: " + message};
  jsonString = JSON.stringify(toSend);
  // Send the JSON string to the server
  ajaxPostRequest("/event_send", jsonString, renderChat);
}


// get stats from the replit instance
function getStats() {
  ajaxGetRequest("/stats", dummyajax);
}

// lock/unlock chat helper functions
function lock_chat() {
  ajaxGetRequest("/lock", dummyajax);
}

// unlocks chat
function unlock_chat() {
  ajaxGetRequest("/unlock", dummyajax);
}

function mute() {
  
}

function unmute() {
  
} 

function ban() {
//document.cookie = "=" + user_name + "; path=/";
}

// see comment inside function
function dummyajax(jsonData) {
  // dummy function so ajaxPostRequest doesent error out from no function callback
  return;
}
