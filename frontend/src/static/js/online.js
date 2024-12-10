import socket from "../../socket";

// function setupTimer(callback, interval) {
//     setInterval(callback, interval);
// }

socket.on('online', (data) => {
    console.log(data);
})

// setupTimer(() => {
//     rid = window.sessionStorage.getItem("roomid")
//     suuid = window.sessionStorage.getItem("suuid")
//     let status = document.hidden ? 'idle' : 'active';
//     socket.emit('heartbeat', status, rid, suuid);
// }, 30000);

export { }