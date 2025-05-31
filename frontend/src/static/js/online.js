import { useEffect, useState } from "react";
import socket from "../../socket";

function status_conversion(status) {
    const status_map = {
        "active": "online",
        "offline": "offline",
        "idle": "idle",
    }

    for (const [key, value] of Object.entries(status_map)) {
        if (status === key) {
            return value;
        }
    }

    return status_map.offline;
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
    const [userData, setUserData] = useState({
        update_type: "",
        data: {},
    });

    socket.on('online', (data) => {
        if (data["update"] === "full" && data["data"] !== userData.data) {
            setUserData({
                update_type: data["update"],
                data: data["data"],
            });
        }
        
        if (data['update'] === 'partial') {
            setUserData({
                update_type: data["update"],
                data: data["data"],
            });
        }
    });

    return (
        <div className="user_list">
            <div id="user_count_container">
                <p id="online_users_count">Online Users: 0</p>
                <p id="offline_users_count">Offline Users: 0</p>
            </div>

            <div id="user_list">
                {Object.entries(userData.data).map((update, index, data) => (
                    <div key={index} className="userlist_user">
                        <img src={update[1]["profile"] ? update[1]["profile"] : "/icons/favicon.ico"} alt="profile" className={`userlist_picture ${status_conversion(update[1]["status"])}`}/>
                        <div className="userlist_info_container">
                            <p className="userlist_displayname">{update[1]["displayName"]}</p>
                            <p className="userlist_role">{cut_replace(update[1]["role"], 50)}</p>
                        </div>
                    </div>
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


export { show_profile_modal }