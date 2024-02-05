function sendCmd(cmd) {
    // this sends a cmd in the current room, privately
    let cmd_str = "$sudo " + cmd;
    sendMessage(cmd_str, true); // we do want it hidden
}