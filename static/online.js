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
        let perm_icon = icon_perm[onlineUser.perm] || '';
        let status_icon = visibility_icon[onlineUser.status] || '';
        let unread = '';
        if (onlineUser?.unread && onlineUser.unread.hasOwnProperty(DisplayName)) {
            unread = onlineUser.unread[DisplayName];
        }
        online += `<button id="online_buttons" onclick="openuserinfo('${onlineUser.username}')" style="color: ${theme['sidebar-text']};"><font color='red'>${unread}</font>${perm_icon}${onlineUser.username}${status_icon}</button><br>`;
    }
    for (let offlineUser of offlineList) {
        let perm_icon = icon_perm[offlineUser.perm] || '';
        let unread = '';
        if (offlineUser?.unread && offlineUser.unread.hasOwnProperty(DisplayName)) {
            unread = offlineUser.unread[DisplayName];
        }
        offline += `<button id="online_buttons" onclick="openuserinfo('${unread}${offlineUser.username}')" style="color: ${theme['sidebar-text']};">${perm_icon}${offlineUser.username}</button><br>`;
    }

    let final_online = `
        <div>
            <font size=5%>Online: ${online_count}</font>
            <br><br>
            ${online}
            <br><br>
            <font size=5%>Offline: ${offline_count}</font>
            <br><br>
            ${offline}
        </div>`;
    onlineDiv.innerHTML = final_online;
}

function getCurrentUserLists() {
    return users_list;
}

socket.on('update_list_full', (userStatuses) => {
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
    let { onlineList, offlineList } = getCurrentUserLists();

    if (updatedUser.status === 'active' || updatedUser.status === 'idle') {
        let isInOnlineList = onlineList.some(user => user.username === updatedUser.username);
        let isInOfflineList = offlineList.some(user => user.username === updatedUser.username);

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
        // Move to offline list
        onlineList = onlineList.filter(user => user.username !== updatedUser.username);
        offlineList.push(updatedUser);
    }

    users_list.onlineList = onlineList;
    users_list.offlineList = offlineList;

    updateUserList(onlineList, offlineList);
});
