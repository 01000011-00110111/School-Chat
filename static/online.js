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

const icon_perm = {
    "dev": '🔧',
    'admin': "⚒️",
    'mod': "🛡️",
    null: ""
}
const visibility_icon = {
    'active': '',
    'idle': '💤',
}

function updateUserList(onlineList, offlineList) {
    let online = '';
    let offline = '';
    let onlineDiv = document.getElementById('online_users');
    let online_count = onlineList.length;
    let offline_count = offlineList.length;
    let DisplayName = getCookie('DisplayName').replace(/"/g, '');

    for (let onlineUser of onlineList) {
        let status_icon = ''
        let perm_icon = icon_perm[onlineUser.perm] || '';
        let ProfilePicure = getCookie('Profile');
        let indicator_color = "";
        if (DisplayName !== onlineUser.username) {status_icon = visibility_icon[onlineUser.status] || '';}
        let unread = '';
        if (onlineUser?.unread && onlineUser.unread.hasOwnProperty(DisplayName) && onlineUser.unread[DisplayName] > 0) {
                unread = onlineUser.unread[DisplayName];
        }
        if (onlineUser) {
            indicator_color = "lime";
        }
        online += `
            <div class="onlineList_user_preview" id="onlineList_user" onclick="openuserinfo('${onlineUser.username}')">
                <img class="message_pfp" src="${ProfilePicure}">
                <div style="display: grid;">
                    <div style="display: flex; align-items: center;">
                        <h3>${onlineUser.username}</h3>
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
        let perm_icon = icon_perm[offlineUser.perm] || '';
        let ProfilePicure = getCookie('Profile');
        let indicator_color = "";
        let unread = '';
        if (offlineUser?.unread && offlineUser.unread.hasOwnProperty(DisplayName) && offlineUser.unread[DisplayName] > 0) {
            unread = offlineUser.unread[DisplayName];
        }
        if (offlineUser) {
            indicator_color = "red";
        }
        offline += `
            <div class="onlineList_user_preview" id="onlineList_user" onclick="openuserinfo('${offlineUser.username}')">
                <img class="message_pfp" src="${ProfilePicure}">
                <div style="display: grid;">
                    <div style="display: flex; align-items: center;">
                        <h3>${offlineUser.username}</h3>
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
            <font id="online" style="color: ${theme['online-color']};" size=5%>Online: ${online_count}</font>
            <br><br>
            ${online}
            <br><br>
            <font id="offline" style="color: ${theme['offline-color']};" size=5%>Offline: ${offline_count}</font>
            <br><br>
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

// const updating = false

// socket.on('updated_display', (oldUserData, newUserData) => {
//     updating = true
//     let { onlineList, offlineList } = getCurrentUserLists();

//     // Helper function to update a user in a list
//     const updateUserInList = (list, oldUsername, newUser) => {
//         return list.map(user =>
//             user.username === oldUsername ? { ...user, ...newUser } : user
//         );
//     };

//     // Update the global user lists
//     users_list.onlineList = onlineList;
//     users_list.offlineList = offlineList;
//     // users_list.offlineList = offlineList;
//     updating = false
//     handleUserUpdate(updatedUser)
// });


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