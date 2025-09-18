// Copyright (C) 2023-2025  cserver45, cseven, CastyiGlitchxz
// License info can be viewed in app.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat
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
        length: {
            online: 0,
            offline: 0,
        }
    });

    useEffect(() => {
        function get_numbers(usersObj) {
            let online_users = 0;
            let offline_users = 0;
    
            Object.values(usersObj["data"]).forEach((user) => {
                if (user["status"] === "active" || user["status"] === "idle") {
                    online_users++;
                } else {
                    offline_users++;
                }
            });
    
            return { online_users, offline_users };
        }
    
        function handleOnline(data) {
            const { online_users, offline_users } = get_numbers(data);
            
            if (data["update"] === "full" && data["data"] !== userData.data) {
                setUserData({
                    update_type: data["update"],
                    data: data["data"],
                    length: {
                        online: online_users,
                        offline: offline_users,
                    }
                });
            }
            
            if (data['update'] === 'partial') {
                setUserData(prev => prev, {
                    update_type: data["update"],
                    data: data["data"],
                    length: {
                        online: online_users,
                        offline: offline_users,
                    }
                });
            }
        }

        
        socket.on('online', handleOnline);
        return () => socket.off("online", handleOnline);
    }, [userData.data]);

    const sortedUsers = Object.entries(userData.data).sort(([, a], [, b]) => {
        const aOnline = a.status === "active" || a.status === "idle";
        const bOnline = b.status === "active" || b.status === "idle";
        return bOnline - aOnline;
    });

    return (
        <div className="user_list">
            <div id="user_count_container">
                <p id="online_users_count">Online Users: {userData.length.online}</p>
                <p id="offline_users_count">Offline Users: {userData.length.offline}</p>
            </div>

            <div id="user_list">
                {sortedUsers.map(([id, user], index) => (
                    <div key={id} className="userlist_user">
                        <img 
                            src={user.profile ? user.profile : "/icons/favicon.ico"} 
                            alt="profile" 
                            className={`userlist_picture ${status_conversion(user.status)}`} 
                            title={status_conversion(user)} 
                        />
                        <div className="userlist_info_container">
                            <p className="userlist_displayname">{user.displayName}</p>
                            <p className="userlist_role">{cut_replace(user.role, 50)}</p>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
}


socket.on('heartbeat', () => {
    if (!document.hidden) {
        socket.emit('beat', { status: 'active', suuid: window.sessionStorage.getItem("suuid") });
    } else {
        socket.emit('beat', { status: 'idle', suuid: window.sessionStorage.getItem("suuid") });
    }
});

window.addEventListener("beforeunload", (e) => {
    socket.emit('beat', { status: 'offline', suuid: window.sessionStorage.getItem("suuid") });
});