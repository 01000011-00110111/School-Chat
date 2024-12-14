"""system.py: Backend functions for communicating with MongoDB.
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in app.py or the LICENSE file.
"""

from datetime import datetime

def format_system_msg(msg):
    """Format a message [SYSTEM] would send."""
    # return f'[SYSTEM]: <font color="#ff7f00">{msg}</font>'
    profile = "<img class='message_pfp' src='/static/favicon.ico'></img>"
    user_string = "<p style='color: #ff7f00;'>[SYSTEM]</p>"
    message_string = f"<p style='color: #ffffff;'>{msg}</p>"
    role_string = "<p style='background:\
#ff7f00; color: #ffffff;' class='badge'>System</p>"
    date_str = datetime.now().strftime("%a %I:%M %p ")
    return {
        'profile': profile,
        'user': user_string,
        'message': message_string,
        'badges': [role_string, None],
        'date': date_str
    }
