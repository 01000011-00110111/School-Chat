import socket from "../../socket";


let user_data = {};

// let status_conversion = {
//     "active": "lime",
//     "offline": "red",
//     "idle": "yellow",
// }

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

const show_profile_modal = (user, role, pfp) => {
    const profile_modal = document.getElementsByClassName("background_blur")[0];
    const close_modal_button = document.getElementsByClassName("close_modal_button")[0];

    /** Repsonsible for setting modals options correctly */
    const profile_modal_button = document.getElementsByClassName("profile_modal_button")[1];
    const modal_user_name = document.getElementById("modal_user_name");
    const modal_user_role = document.getElementById("modal_user_role");
    const modal_user_picture = document.getElementById("modal_user_picture");
    /** End of code */

    if (!profile_modal.classList.contains('show_modal')) {
        profile_modal.classList.add('show_modal');
        profile_modal_button.setAttribute('click', `opendms("${user}")`)
        modal_user_name.innerHTML = user;
        modal_user_role.innerHTML = role;
        modal_user_picture.src = pfp ? pfp : "/icons/favicon.ico";
    }
    
    close_modal_button.addEventListener('click', () => { 
        profile_modal.classList.remove('show_modal');
    });
}

const fetch_user = (user_name, role, profile_picture) => {
    console.log(`${user_name} : ${role} : ${profile_picture}`)
    show_profile_modal(user_name, role, profile_picture)
}

const SetUsersList = ({user_name, profile_picture, user_role, index, status}) => {
    return (
        <div className="user_card_mini" onClick={() => fetch_user(user_name, user_role, profile_picture)}>
            <img src={profile_picture ? profile_picture : "/icons/favicon.ico"} alt="hi" className="user_profile_picture"/>
            <div className="userlist_user_details">
                <p className="userlist_display_name" key={index}>{user_name}</p>
                <p className="userlist_role" key={index}>{cut_replace(user_role, 21)}</p>
            </div>
            <div className="status_indicator" style={{background: status}}>{status}</div>
        </div>
    )
}

socket.on('online', (data) => {
    user_data = data;
    if (data['update'] === 'full') {
        const userListElement = document.getElementById("user_list");
        userListElement.innerHTML = ""; // Clear the existing content
        for (let key in data['data']) {
            const userListElementHtml = SetUsersList(data['data'][key]);
            userListElement.appendChild(userListElementHtml); // Append the new content
        }
    } else {
        const userListElementHtml = SetUsersList(data['data']);
        document.getElementById("user_list").appendChild(userListElementHtml);
    }
})

function notifyStatusChange(status) {
    socket.emit('update', { status: status, suuid: window.sessionStorage.getItem("suuid") });
}

document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        notifyStatusChange('idle');
    } else {
        notifyStatusChange('active');
    }

function notifyStatusChange(status) {
const setupTimer = (cb, delay) => {
    let id = setInterval(cb, delay);
    return () => clearInterval(id);
}
setupTimer(() => {
    let rid = window.sessionStorage.getItem("roomid");
    let suuid = window.sessionStorage.getItem("suuid");
    let status = document.hidden ? 'idle' : 'active';
    socket.emit('heartbeat', status, rid, suuid);
}, 30000);
export { SetUsersList, user_data, show_profile_modal }
