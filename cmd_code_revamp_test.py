class Debug:
    def status(self):
        return "Debug Status"

    def pstats(self):
        return "Debug PStats"

    def line_count(self):
        return "Debug Line Count"

class Online:
    def appear_offline(self):
        return "Appear Offline"

    def appear_online(self):
        return "Appear Online"

class Moderation:
    def globalock(self):
        return "Global Lock"

    def lock(self):
        return "Lock"

    def unlock(self):
        return "Unlock"

class Room:
    def reset_chat_user(self):
        return "Reset Chat User"

class PerformAction:
    def debug_ping(self):
        return "Debug Ping"

debug = Debug()
online = Online()
moderation = Moderation()
room = Room()
perform_action_obj = PerformAction()

actions_permissions_mapping = {
    ('status', 'dev'): debug.status,
    ('pstats', 'dev'): debug.pstats,
    ('lines', 'dev'): debug.line_count,
    ('appear_offline', 'dev'): online.appear_offline,
    ('appear_online', 'dev'): online.appear_online,
    ('globalock', 'dev'): moderation.globalock,
    ('lock', 'dev'): moderation.lock,
    ('unlock', 'dev'): moderation.unlock,
    ('rc', 'dev'): room.reset_chat_user,
    ('ping', 'dev'): perform_action_obj.debug_ping,
    ('lock', 'admin'): moderation.lock,
    ('unlock', 'admin'): moderation.unlock,
}

def perform_action(action, user_perm):
    key = (action, user_perm)
    if key in actions_permissions_mapping and callable(actions_permissions_mapping[key]):
        return actions_permissions_mapping[key]()
    else:
        return "Invalid action or permission level"

action_to_perform_dev = 'ping'
user_permission_dev = 'dev'
result_dev = perform_action(action_to_perform_dev, user_permission_dev)
print(result_dev)

action_to_perform_admin = 'ping'
user_permission_admin = 'admin'
result_admin = perform_action(action_to_perform_admin, user_permission_admin)
print(result_admin)


# class CommandArray:
#     def __init__(self):
#         self.actions_permissions_mapping = {
#             ('status', 'dev'): debug.status,
#             ('pstats', 'dev'): debug.pstats,
#             ('lines', 'dev'): debug.line_count,
#             ('appear_offline', 'dev'): online.appear_offline,
#             ('appear_online', 'dev'): online.appear_online,
#             ('globalock', 'dev'): moderation.globalock,
#             ('lock', 'dev'): moderation.lock, 
#             ('unlock', 'dev'): moderation.unlock,
#             ('rc', 'dev'): room.reset_chat_user,
#             ('ping', 'dev'): perform_action_obj.debug_ping,
#             ('lock', 'admin'): moderation.lock,
#             ('unlock', 'admin'): moderation.unlock,
#             ('ping', 'admin'): perform_action_obj.debug_ping,
#         }

#     def perform_action(self, action, user_perm):
#         key = (action, user_perm)
#         if key in self.actions_permissions_mapping and callable(self.actions_permissions_mapping[key]):
#             return self.actions_permissions_mapping[key]()
#         else:
#             return "Invalid action or permission level"

# command_array = CommandArray()

# action_to_perform_dev = 'lock'
# user_permission_dev = 'dev'
# result_dev = command_array.perform_action(action_to_perform_dev, user_permission_dev)
# print(result_dev)

# action_to_perform_admin = 'lock'
# user_permission_admin = 'admin'
# result_admin = command_array.perform_action(action_to_perform_admin, user_permission_admin)
# print(result_admin)
