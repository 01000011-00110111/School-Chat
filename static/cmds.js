socket.on("cmd", ({cmd}) => {
    if (cmd === 'refreshusr') {
        refreshUsers();
    } else if (cmd === 'reset') {
        reset_chat();
    } else if (cmd === 'lock') {
        lock_chat();
    } else if (cmd === 'unlock') {
        unlock_chat();
    } else if (cmd === 'stats') {
        getStats();
    } else if (cmd === 'linect') {
        
    }
});