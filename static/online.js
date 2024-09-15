// Copyright (C) 2023, 2024  cserver45, cseven
// License info can be viewed in main.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat
const users_list = {
    onlineList: [],
    offlineList: []
};

function notifyStatusChange(status) {
    socket.emit('status_change', { status: status });
}

document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        notifyStatusChange('idle');
    } else {
        notifyStatusChange('active');
    }
});

const cut_replace = (text, length) => {
    if (text == null) {
        return "";
    }
    if (text.length <= length) {
        return text;
    }
    text = text.substring(0, length);
    last = text.lastIndexOf("");
    text = text.substring(0, last);
    return text + "...";
}

function updateUserList(onlineList, offlineList) {
    let online = '';
    let offline = '';
    let onlineDiv = document.getElementById('online_users');
    let online_count = onlineList.length;
    let offline_count = offlineList.length;
    let DisplayName = getCookie('DisplayName').replace(/"/g, '');

    for (let onlineUser of onlineList) {
        let indicator_color = "lime";
        let unread = '';
        if (onlineUser?.unread && onlineUser.unread.hasOwnProperty(DisplayName) && onlineUser.unread[DisplayName] > 0) {
                unread = onlineUser.unread[DisplayName];
        }
        if (onlineUser.status === "idle" && onlineUser.username !== DisplayName) {
            indicator_color = "yellow";
        }
        online += `
            <div class="onlineList_user_preview" id="onlineList_user" onclick="openuserinfo('${onlineUser.username}')" title="${onlineUser.username}">
                <img class="user_list_pfp" src="${onlineUser.profile}">
                <div style="display: grid; left: -10px; position: relative;">
                    <div style="display: grid; align-items: center;">
                        <h3>${cut_replace(onlineUser.username, 11)}</h3>
                        <p>${cut_replace(onlineUser.role, 11)}</p>
                    </div>
                </div>
                <div style="display: grid;">
                    <div style="background: ${indicator_color}; width: 10px; height: 10px; border-radius: 100px; right: 12px; position: relative;">

                    </div>
                </div>
            </div>
        `;
    }
    for (let offlineUser of offlineList) {
        let indicator_color = "red";
        let unread = '';
        if (offlineUser?.unread && offlineUser.unread.hasOwnProperty(DisplayName) && offlineUser.unread[DisplayName] > 0) {
            unread = offlineUser.unread[DisplayName];
        }
        offline += `
            <div class="onlineList_user_preview" id="onlineList_user" onclick="openuserinfo('${offlineUser.username}')" title="${offlineUser.username}">
                <img class="user_list_pfp" src="${offlineUser.profile}">
                <div style="display: grid; left: -10px; position: relative;">
                    <div style="display: grid; align-items: center;">
                        <h3>${cut_replace(offlineUser.username, 11)}</h3>
                        <p>${cut_replace(offlineUser.role, 11)}</p>
                    </div>
                </div>
                <div style="display: grid;">
                    <div style="background: ${indicator_color}; width: 10px; height: 10px; border-radius: 100px; right: 12px; position: relative;">

                    </div>
                </div>
            </div>
        `;
    }

    let final_online = `
        <div>
            <font id="online" style="color: ${theme['online-color']};" size=5%>Online: ${online_count}</font> <font id="offline" style="color: ${theme['offline-color']};" size=5%>Offline: ${offline_count}</font>
            <br><br> 
            ${online}
            ${offline}
        </div>`;
    onlineDiv.innerHTML = final_online;
    // console.log('done online')
}

function getCurrentUserLists() {
    return users_list;
}

socket.on('update_list_full', (userStatuses) => {
    users_list.onlineList = [];
    users_list.offlineList = [];
    let onlineList = [];
    let offlineList = [];

    for (let username in userStatuses) {
        if (userStatuses[username].status === 'active' || userStatuses[username].status === 'idle') {
            onlineList.push(userStatuses[username]);
        } else {
            offlineList.push(userStatuses[username]);
        }
    }
    
    users_list.onlineList = onlineList;
    users_list.offlineList = offlineList;
    
    updateUserList(onlineList, offlineList);
});


socket.on("update_list", (updatedUser) => {
    handleUserUpdate(updatedUser)
});

function handleUserUpdate(updatedUser) {
        let { onlineList, offlineList } = getCurrentUserLists();
        let isInOnlineList = onlineList.some(user => user.username === updatedUser.username);
        let isInOfflineList = offlineList.some(user => user.username === updatedUser.username);

        if (updatedUser.status === 'active' || updatedUser.status === 'idle') {
            if (isInOnlineList) {
                // Update user in online list
                onlineList = onlineList.map(user => user.username === updatedUser.username ? updatedUser : user);
            } else if (isInOfflineList) {
                // Move from offline to online list
                offlineList = offlineList.filter(user => user.username !== updatedUser.username);
                onlineList.push(updatedUser);
            } else {
                // Add to online list
                onlineList.push(updatedUser);
            }
        } else {
            if (isInOfflineList) {
                // Update user in offline list
                offlineList = offlineList.map(user => user.username === updatedUser.username ? updatedUser : user);
            } else {
                // Move to offline list
                onlineList = onlineList.filter(user => user.username !== updatedUser.username);
                offlineList.push(updatedUser);
            }
        }

        users_list.onlineList = onlineList;
        users_list.offlineList = offlineList;

        updateUserList(onlineList, offlineList);
}