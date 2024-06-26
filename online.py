from flask_socketio import emit
import database
# from user import U
socketids = {}
users_list = {}

def update_userlist(sid, data, uuid):
    for key, value in data.items():
        users_list[uuid][key] = value
    emit('update_list', users_list[uuid], namespace='/', broadcast=True) #later ill advabce ui to be able to send to only one user
    return users_list[uuid]


def get_all_offline():
    offline = []
    for user in users_list:
        if user['status'] in ['offline','offline-locked']:
            offline.append(user['username'])
    return offline

for user in database.get_all_offline():
    perm = 'dev' if user['SPermission'][0] == 'Debugpass' else 'mod' if\
        user['SPermission'][0] == 'adminpass' else 'mod'\
            if user['SPermission'][0] == 'modpass' else None
    
    status = 'offline' if user['status'] != 'offlne-locked' else 'offline-locked'
            
    users_list[user['userid']] = {'username': user['displayName'],
                                  'status': status, 'perm': perm}
    
"""
unread = Private.get_unread(
    format_userlist(self.uuid, key.uuid))
if isinstance(unread, dict):
    unread = 0 if key.uuid == self.uuid else unread.get(self.uuid, 0)
else:
    unread = 0    
"""# for future us will rework