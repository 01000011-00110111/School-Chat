let room = {}
socket.on("room_data", (room_data) => {
    // console.log(room_data)
    room = room_data
    document.getElementById('room-name').value = room_data.name;
    document.getElementById('mods').value = room_data.mods;
    document.getElementById('whitelisted').value = room_data.whitelisted;
    document.getElementById('blacklisted').value = room_data.blacklisted;
    document.getElementById('can-send').value = room_data.canSend;
    document.getElementById('room-locked').value = room_data.locked ? "true" : "false";
    document.getElementById('muted').value = room_data.muted;
    document.getElementById('banned').value = room_data.banned;
})

document.getElementById("chat-room-settings").onsubmit = function(event) {
    event.preventDefault();
    
    const roomName = document.getElementById("room-name").value;
    const mods = document.getElementById("mods").value;
    const whitelisted = document.getElementById("whitelisted").value;
    const blacklisted = document.getElementById("blacklisted").value;
    const canSend = document.getElementById("can-send").value;
    const roomLocked = document.getElementById("room-locked").value === "true";
    // const muted = document.getElementById("muted").value;
    // const banned = document.getElementById("banned").value;

    const updatedRoom = {
        roomid: room.vid,
        name: roomName,
        mods,
        whitelisted,
        blacklisted,
        canSend,
        locked: roomLocked,
    };
    socket.emit('update_room', updatedRoom);
    
};

document.querySelector(".delete-room").onclick = function() {
    if (confirm("Are you sure you want to delete this room?")) {
        socket.emit('delete_room', room.vid);
    }
};

document.querySelector("#room-select").onchange = function() {
    const selectedRoom = document.querySelector("#room-select").value;
    socket.emit('get_room_data', selectedRoom);
};