function is_cmd(message, cmd_list) {
  // check if the text could match a cmd
  // MAKE SURE THIS ONLY MATCHES CMDS AND NOT A CHAT MESSAGE WITH THE WORD HELP AS AN EXAMPLE
  // for the help cmd
  // let cmd_def = ajaxGetRequest('/cmdDef', processCmdDef);
  
  return false;
}
// saves cmd list in cache? cookie? idk but somewhere in the browser
function save_cmd_list(jsonData) {
  console.log(jsonData);
  return false;
}

// saves command definitions on loading
function save_cmd_def(jsonData) {
  console.log(jsonData);
  return false;
}

// get the command list from wherever it is
function get_cmd_list() {
  return false;
}

function processCmdDef(jsonData) {
  // return a 
  return false;
}
// use replit db instead of text files (note for later I'm on phone rn)

function help_cmd(cmd_list, cmd_def) {
  // send user_name as SYSTEM for these commands
  
}

// Mute cmd list and checks

function mute_cmd(user) {
  // take the user provided and add them to the muted.txt file
}

function unmute_cmd(user) {
  // remove the user provided from te muted.txt file
}

function is_user_muted(user) {
  // check if user is in muted.txt
  return false;
}