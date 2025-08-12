# import re
from socketio_confg import sio
from user.database import update
from user.user import User

from better_profanity import profanity

def set_display_name(display_name):
    """Set the display name after filtering bad words."""
    censored = profanity.censor(display_name)
    if display_name != censored:
        return False, "display name contains bad words"
    if len(display_name) > 14:
        return False, "display name is too long (max 14 characters)"
    if ' ' in display_name:
        return False, "display name cannot contain spaces"
    if len(display_name) < 3:
        return False, "display name is too short (min 3 characters)"
    return True, censored

def set_role(role):
    """Set the role after filtering bad words."""
    censored = profanity.censor(role)
    if role != censored:
        return False, "role contains bad words"
    if len(role) > 24:
        return False, "role is too long (max 24 characters)"
    return censored

def check_color(color, reference_color):
    """Check if the color is too close to the background color."""
    if is_color_too_close(color, reference_color):
        return False, "color is too close to the background color"
    return True, None

def is_color_too_close(color1, color2):
    """Check if the two colors are too close."""
    # Example implementation assuming color is a hex string
    threshold = 80
    r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
    r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
    return (abs(r1-r2) < threshold and abs(g1-g2) < threshold and abs(b1-b2) < threshold)

@sio.on("save_settings")
async def save_settings(sid, data):
    """Handle the save settings event."""
    # Extract user settings from the data
    suuid = data.get("suuid")
    user = User.get_user(suuid)
    uuid = user.uuid
    display_name = data["formInfo"].get("displayName")
    role = data["formInfo"].get("role")
    username_color = data["formInfo"].get("usernameColor")
    role_color = data["formInfo"].get("roleColor")
    message_color = data["formInfo"].get("messageColor")

    errors = []
    edits = []


    if display_name:
        display_name_result = set_display_name(display_name)
        if not display_name_result[0]:
            errors.append(display_name_result)
        else:
            edits.append({"display_name": display_name_result[1]})

    if role:
        role_result = set_role(role)
        if not role_result[0]:
            errors.append(role_result)
        else:
            edits.append({"role": role_result})

    if username_color:
        username_color_result = check_color(username_color, "#000000")
        if not username_color_result[0]:
            errors.append(username_color_result)
        else:
            edits.append({"u_color": username_color})

    if role_color:
        role_color_result = check_color(role_color, "#000000")
        if not role_color_result[0]:
            errors.append(role_color_result)
        else:
            edits.append({"r_color": role_color})

    if message_color:
        message_color_result = check_color(message_color, "#000000")
        if not message_color_result[0]:
            errors.append(message_color_result)
        else:
            edits.append({"m_color": message_color})

    if errors:
        await sio.emit("settings", {"status": "error", "errors": errors}, room=sid)
    else:
        update(edits, uuid)
        user.update(edits)
        await sio.emit("settings", {"status": "success", "edits": edits}, room=sid)

@sio.on("get_settings")
async def get_settings(sid, suuid):
    """Handle the get settings event."""
    # suuid = data.get("suuid")
    user = User.get_user(suuid)
    if not user:
        await sio.emit("settings", {"status": "error", "error": "User not found"}, room=sid)
        return
    settings = {
        "displayName": user.display_name,
        "role": user.role,
        "usernameColor": user.u_color,
        "roleColor": user.r_color,
        "messageColor": user.m_color
    }
    
    await sio.emit("settings", {"status": "initial", "settings": settings}, room=sid)