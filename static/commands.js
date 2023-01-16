
function is_cmd(message) {
    // check if the text could match a cmd
    // MAKE SURE THIS ONLY MATCHES CMDS AND NOT A CHAT MESSAGE WITH THE WORD HELP AS AN EXAMPLE
    // for the chat lines cmd
    // ajaxGetRequest("/chat_count", chat_log_count)
    // the long if statement set lol
    if (message === "/lines") {
        ajaxGetRequest("/chat_count", chat_log_count);
        return true;
    } else {
        return false;
    }
}

// saves cmd list in cookie... idk but somewhere in the browser
function save_cmd_list(jsonData) {
    console.log(jsonData);
    document.cookie = "cmds=" + jsonData + "; path=/";
    return false;
}

// saves command definitions on loading
function save_cmd_def(jsonData) {
    console.log(jsonData);
    document.cookie = "cmd_def=" + jsonData + "; path=/";
    return false;
}
// use replit db instead of text files (note for later I'm on phone rn)
function help_cmd(cmd_list, cmd_def) {
    // send user_name as SYSTEM for these commands
}

// function that prints out chat logfile line count
function chat_log_count(jsonData) {
    // nothing needed here, itll just add it to the log file
    // in the future maybe add it to dev chat instead of main
    // or use it in someway here for some other function
    return;
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