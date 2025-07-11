from socketio_confg import sio
from user.user import User
from user import database
import re

@sio.on("signup")
async def signup(sid, data):
    """
    This function is called when a client sends a signup request to the server.
    """
    print(data)
    username = data.get("username", "").strip()
    password = data.get("password", "")
    email = data.get("email", "").strip()

    # Validate input
    if not username or not password or not email:
        await sio.emit("signup", {'suuid': False, 'status': 'failed', 'reason': 'missing_fields'}, to=sid)
        print("Missing fields in signup data")
        return
    
    # Check if the user is didn't check the box
    if not data.get("agreeToTerms"):
        await sio.emit("signup", {'suuid': False, 'status': 'failed', 'reason': 'checkbox_required'}, to=sid)
        print("User did not agree to terms")
        return

    # Validate email format
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        await sio.emit("signup", {'suuid': False, 'status': 'failed', 'reason': 'invalid_email'}, to=sid)
        print("Invalid email format")
        return

    # Check if username already exists
    if database.username_exists(username):
        await sio.emit("signup", {'suuid': False, 'status': 'failed', 'reason': 'username_taken'}, to=sid)
        print("Username already taken")
        return

    # Check username format (example: alphanumeric, 3-10 characters)
    if not re.match(r'^[a-zA-Z0-9]{3,10}$', username):
        await sio.emit("signup", {'suuid': False, 'status': 'failed', 'reason': 'invalid_username'}, to=sid)
        print("Invalid username format")
        return

    # Check password strength (example: at least 8 characters, one uppercase, one lowercase, one number)
    if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'[0-9]', password):
        await sio.emit("signup", {'suuid': False, 'status': 'failed', 'reason': 'weak_password'}, to=sid)
        print("Weak password")
        return

    # Check if email already exists
    if database.email_exists(email):
        await sio.emit("signup", {'suuid': False, 'status': 'failed', 'reason': 'email_taken'}, to=sid)
        print("Email already taken")
        return
    

    # Add account to the database
    database.add_accounts(data)
    await sio.emit("signup", {'suuid': True, 'status': 'successful'}, to=sid)
