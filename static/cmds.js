function sendCmd(cmd) {
    // this sends a cmd in the current room, privately
    let cmd_str = "$sudo " + cmd;
    sendMessage(cmd_str, true); // we do want it hidden
};

function open_admin() {
    document.getElementById('admin_menu').style.display = 'block';
};

function close_admin() {
    document.getElementById('admin_menu').style.display = 'none';
};