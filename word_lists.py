""" List of censored words, and any other lists we might need.
    Copyright (C) 2023  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""

with open('unbanned_words.txt', 'r') as file:
    whitelist_words = [word.strip() for word in file.readlines()]

censored = [
    'sh!t',
    'boobie',
]

banned_usernames = ('Admin', 'admin', '[admin]', '[ADMIN]', 'ADMIN', '[Admin]',
                    '[URL]', 'mod', 'Mod', '[mod]', '[Mod]', '[MOD]', 'MOD',
                    'SYSTEM', '[SYSTEM]', "SONG", "[Song]", "[SONG]", "[song]",
                    " ", "  ", "   ", "cseven", "cserver", 'system',
                    '[system]', '[System]', 'System')

approved_links = ('/settings', '/backup', "/admin")
