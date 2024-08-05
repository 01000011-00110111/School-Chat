// Copyright (C) 2023, 2024  cserver45, cseven
// License info can be viewed in main.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat

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