import socket from "../../socket";

// function setupTimer(callback, interval) {
//     setInterval(callback, interval);
// }

function cx_create_template(user_name, profile_picture, user_role) {
    const user_template = `
    <div class='user_card_mini'>
        <img src=${profile_picture} alt='hi' className='user_profile_picture'/>
        <div class='userlist_user_details'>
            <p class='userlist_display_name'>${user_name}</p>
            <p class='userlist_role'>${cut_replace(user_role, 21)}</p>
        </div>
    </div>`
    return user_template
}

const cut_replace = (text, length) => {
    if (text == null) {
        return "";
    }
    if (text.length <= length) {
        return text;
    }
    text = text.substring(0, length);
    var last = text.lastIndexOf("");
    text = text.substring(0, last);
    return text + "...";
}

socket.on('online', (data) => {
    console.log(data["data"])
    const usl = document.getElementById("user_list")
    data["data"].map((element, index) => {
        console.log(JSON.stringify(element))
        usl.innerHTML += cx_create_template(element["displayName"], element["profile"], element["role"]);

        console.log(index)
        return 0;
    },[])
})

// setupTimer(() => {
//     rid = window.sessionStorage.getItem("roomid")
//     suuid = window.sessionStorage.getItem("suuid")
//     let status = document.hidden ? 'idle' : 'active';
//     socket.emit('heartbeat', status, rid, suuid);
// }, 30000);

export { }