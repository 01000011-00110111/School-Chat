import database
# from user import U
socketids = {}
users_list = {}

def update_userlist(sid, data, uuid):
    for key, value in data.items():
        users_list[uuid][key] = value
    return users_list[uuid]


def get_all_offline():
    offline = []
    for user in users_list:
        if user['status'] in ['offline','offline-locked']:
            offline.append(user['username'])
    return offline
    
    

# def status_change(data):
#     status = data['status']
#     # if username:
#     user_statuses[username] = status
#     emit('status_update', {'username': username, 'status': status['status'], 'permission': status['permission']}, broadcast=True)


# # def handle_request_user_list():
# #     emit('full_status_update', user_statuses)


# # def handle_ping_user(data):
# #     target_username = data['target_username']
# #     target_sid = user_sockets.get(target_username)
# #     if target_sid:
# #         emit('ping', {}, room=target_sid)
# #test code for unread messages later

for user in database.get_all_offline():
    perm = 'dev' if user['SPermission'][0] == 'Debugpass' else 'mod' if\
        user['SPermission'][0] == 'adminpass' else 'mod'\
            if user['SPermission'][0] == 'modpass' else None
    
    status = 'offline' if user['status'] != 'offlne-locked' else 'offline-locked'
            
    users_list[user['userid']] = {'username': user['displayName'],
                                  'status': status, 'perm': perm}
    
print(users_list)