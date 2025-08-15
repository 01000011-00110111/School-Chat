import { useState } from "react";
import socket from "../../socket";
let freeze = false

function status_conversion(status) {
    const status_map = {
        "active": "online",
        "offline": "offline",
        "offline": "offline-locked",
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

function notifyStatusChange(status) {
    socket.emit('update', { status: status, suuid: window.sessionStorage.getItem("suuid") });
}

document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        notifyStatusChange('idle');
    } else {
        // socket.emit('status', window.sessionStorage.getItem("suuid"));
        notifyStatusChange('active');
    }
});


export function UserList() {
    const [userData, setUserData] = useState({
        update_type: "",
        data: {},
        length: {
            online: 0,
            offline: 0,
        }
    });

    socket.on('online', (data) => {
        function get_numbers() {
            let online_users = 0;
            let offline_users = 0;

            Object.entries(data["data"]).map((update, index, data) => {
                // console.log("Update:", update[1]["status"])
                if (update[1]["status"] === "active" || update[1]["status"] === "idle") {
                    online_users += 1;
                } else if (update[1]["status"] === "offline") {
                    offline_users += 1;
                }
            });

            return {online_users, offline_users};
        }

        if (data["update"] === "full" && data["data"] !== userData.data) {
            setUserData({
                update_type: data["update"],
                data: data["data"],
                length: {
                    online: get_numbers().online_users,
                    offline: get_numbers().offline_users,
                }
            });
        }
        
        if (data['update'] === 'partial') {
            setUserData({
                update_type: data["update"],
                data: data["data"],
                length: {
                    online: get_numbers().online_users,
                    offline: get_numbers().offline_users,
                }
            });
        }
    });

    return (
        <div className="user_list">
            <div id="user_count_container">
                <p id="online_users_count">Online Users: {userData.length.online}</p>
                <p id="offline_users_count">Offline Users: {userData.length.offline}</p>
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
    } else {
        socket.emit('beat', { status: 'idle', suuid: window.sessionStorage.getItem("suuid") });
    }
});

window.addEventListener("beforeunload", (e) => {
    socket.emit('beat', { status: 'offline', suuid: window.sessionStorage.getItem("suuid") });
});