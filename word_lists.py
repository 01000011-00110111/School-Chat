"""word_lists.py: List of censored words, and any other lists we might need.
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
from better_profanity import profanity

profanity.CENSOR_CHAR = '#'
whitelist_words = []
blacklist_words = []

def start():
    """sets the whitlisted and blacklisted words."""
    with open('backend/unbanned_words.txt', 'r', encoding="utf-8") as file:
        whitelist = list(file.read().splitlines())

    with open('backend/banned_words.txt', 'r', encoding="utf-8") as file:
        blacklist = list(file.read().splitlines())

    return whitelist, blacklist

banned_usernames = ('Admin', 'admin', '[admin]', '[ADMIN]', 'ADMIN', '[Admin]',
                    '[URL]', 'mod', 'Mod', '[mod]', '[Mod]', '[MOD]', 'MOD',
                    'SYSTEM', '[SYSTEM]', "SONG", "[Song]", "[SONG]", "[song]",
                    " ", "  ", "   ", "cseven", "cserver", 'system',
                    '[system]', '[System]', 'System')

approved_links = ('/settings', '/backup', "/dev", "/admin", "/mod", "/projects")
