import { useState } from "react";
import socket from "../../socket";

// Full user data - All users sent from backend;
let user_data = {};

// Partial user data;
let par_user = {};

let status_conversion = {
    "active": "lime",
    "offline": "red",
    "idle": "orange",
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

// const SetUsersList = ({user_name, profile_picture, user_role, index, status}) => {
//     console.log(status, user_name)
//     return (
//         <li className="user_card_mini" onClick={() => fetch_user(user_name, user_role, profile_picture)}>
//             <img src={profile_picture ? profile_picture : "/icons/favicon.ico"} alt="hi" className="user_profile_picture"/>
//             <div className="userlist_user_details">
//                 <p className="userlist_display_name" key={index}>{user_name}</p>
//                 <p className="userlist_role" key={index}>{cut_replace(user_role, 21)}</p>
//             </div>
//             <div className="status_indicator" style={{background: status_conversion[status]}}></div>
//         </li>
//     )
// }

socket.on('online', (data) => {
    par_user = data
    if (data['update'] === 'partial') {
        par_user = data;
    } else {
        user_data = data["data"];
    }
    // console.log(user_data);
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
});

export function UserList() {
    return (
        <div className='user_list'>
            <input type='text' placeholder='Search for a user' id='user_search_input'/>
            <div id='user_list'>
                {[Object.entries(user_data), Object.entries(par_user)].map((user, index) => (
                    <li className="user_card_mini" key={index}>
                        <p>{console.log(user, index)}</p>
                        <img src={user[1]["profile"] ? user[1]["profile"] : "/icons/favicon.ico"} alt="hi" className="user_profile_picture"/>
                        <div className="userlist_user_details">
                            <p className="userlist_display_name">{user[1]["displayName"]}</p>
                            <p className="userlist_role">{cut_replace(user[1]["role"], 21)}</p>
                            <div className="status_indicator" style={{background: status_conversion[user[1]["status"]]}}></div>
                        </div>
                    </li>
                ))}
            </div>
        </div>
    )
}

// const setupTimer = (cb, delay) => {
//     let id = setInterval(cb, delay);
//     return () => clearInterval(id);
// }

socket.on('heartbeat', () => {
    console.log("Heartbeat received:");
    if (!document.hidden) {
        socket.emit('beat', { status: 'active', suuid: window.sessionStorage.getItem("suuid") });
    } else if (document.hidden) {
        socket.emit('beat', { status: 'idle', suuid: window.sessionStorage.getItem("suuid") });
    } else {
        socket.emit('beat', { status: 'offline', suuid: window.sessionStorage.getItem("suuid") });
    }
});

window.addEventListener("beforeunload", (e) => {
    socket.emit('beat', { status: 'offline', suuid: window.sessionStorage.getItem("suuid") });
});


export { user_data, show_profile_modal, par_user }