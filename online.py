from flask_socketio import emit

import database

socketids = {}
users_list = {}

def get_scoketid(uuid):
    return  socketids[uuid]

def update_userlist(_, data, uuid):
    for key, value in data.items():
        users_list[uuid][key] = value
    # send_users_list = users_list[uuid]
    # send_users_list.pop('unread', None)

    emit('update_list', users_list[uuid], namespace='/', broadcast=True)
    #later ill advabce ui to be able to send to only one user
    return users_list[uuid]


def add_unread(recipient, sender):
    displayName = users_list[recipient]['username']
    users_list.setdefault(sender, {'unread': {}}).setdefault('unread', {}).setdefault(displayName, 0)
    users_list[sender]['unread'][displayName] += 1
    # print(users_list[recipient], '\n', recipient)
    if 'offline' not in users_list[sender]['status']:
        emit('update_list', users_list[sender], namespace='/', to=socketids[recipient])


def clear_unread(recipient, sender):
    displayName = users_list[recipient]['username']
    users_list.setdefault(sender, {'unread': {}}).setdefault('unread', {}).setdefault(displayName, 0)
    users_list[sender]['unread'][displayName] = 0
    # print(users_list[recipient], '\n', recipient)
    if 'offline' not in users_list[sender]['status']:
        emit('update_list', users_list[sender], namespace='/', to=socketids[recipient])


def get_all_offline():
    offline = []
    for user in users_list:
        if user['status'] in ['offline','offline-locked']:
            offline.append(user['username'])
    return offline

for user in database.get_all_offline():
    # print(user)
    perm = 'dev' if user['perm'][0] == 'Debugpass' else 'admin' if\
        user['perm'][0] == 'adminpass' else 'mod'\
            if user['perm'][0] == 'modpass' else None
    
    status = 'offline' if user['status'] != 'offlne-locked' else 'offline-locked'
            
    users_list[user['userid']] = {'username': user['displayName'],
                                  'status': status, 'perm': perm, 'unread': {}}
    
"""
unread = Private.get_unread(
    format_userlist(self.uuid, key.uuid))
if isinstance(unread, dict):
    unread = 0 if key.uuid == self.uuid else unread.get(self.uuid, 0)
else:
    unread = 0    
"""# for future us will rework