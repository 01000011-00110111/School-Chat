socket.on("cmd", ({cmd}) => {
    if (cmd === 'refreshusr') {
        refreshUsers();
    // } else if (cmd === 'enable ai') {
    //     document.title = "Class Chat AI";
    //     window.sessionStorage.setItem("ai", "true");
    // } else if (cmd === 'disable ai') {
    //     document.title = "OCD wleb Potato man Skill Issue!!!1!";
    //     window.sessionStorage.setItem("ai", "false");
    } else if (cmd === 'reset') {
        reset_chat();
    } else if (cmd === 'lock') {
        lock_chat();
    } else if (cmd === 'unlock') {
        unlock_chat();
    } else if (cmd === 'stats') {
        getStats();
    } else if (cmd === 'linect') {
        ajaxGetRequest("/chat_count", dummyajax);
    } else if (cmd === 'make me a sandwich') {
        let toSend = "<img src='" + 'data:image/jpeg;base64,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' + "'></img>"
        socket.emit('admin_message', toSend);
    }
});