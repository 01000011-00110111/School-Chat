"""accounting.py: Checks on accounts and sends emails
    Stuff to handle accounts
    Copyright (C) 2023, 2024  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
import configparser
import hashlib
import re
import smtplib
import uuid
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from better_profanity import profanity

import database
import word_lists

# from user import inactive_users
from online import users_list

config = configparser.ConfigParser()
config.read('config/keys.conf')

# Get our custom whitelist words (that should not be banned in the first place)
profanity.load_censor_words(whitelist_words=word_lists.whitelist_words)
profanity.add_censor_words(word_lists.blacklist_words)

def send_email(receiver_email, subject, message_body):
    """Sends a email to the user."""
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = config["backend"]['email']
    sender_password = config["backend"]['password']

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    message_id = f"<{uuid.uuid4()}@{config['backend']['URL']}>"
    msg.add_header('Message-ID', message_id)

    msg.attach(MIMEText(message_body, 'html'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
    finally:
        server.quit()

def load_email_template(template_name):
    """loads proper email template."""
    with open(f'templates/emails/{template_name}', "r", encoding="UTF-8") as f:
        return f.read()

def send_verification_email(username, email, verification_code, userid):
    """Sends the vericfacation email to user."""
    url = config["backend"]['URL']
    subject = f'Verification of {username}!'
    message_body = load_email_template('email_temp.html')
    message_body = message_body.replace("[Recipient's Name]", username)
    message_body = message_body.replace(
        "[Verification Link]",
        f'{url}/verify/{userid}/{verification_code}'
    )
    send_email(email, subject, message_body)

def send_password_reset_email(username, email, reset_code, userid):
    """Sends the password reset email to user."""
    url = config["backend"]['URL']
    subject = 'Password Reset Request'
    message_body = load_email_template('password_email_temp.html')
    message_body = message_body.replace("[Recipient's Name]", username)
    message_body = message_body.replace(
        "[Reset Link]",
        f'{url}/reset/{userid}/{reset_code}'
    )
    send_email(email, subject, message_body)

# def is_account_expired(permission_str):
#     """Checks if the account is expired."""
#     parts = permission_str.split(' ')
#     if len(parts) == 3 and parts[0] == 'locked':
#         expiration_time_str = ' '.join(parts[1:])
#         expiration_time = datetime.strptime(expiration_time_str,
#                                             "%Y-%m-%d %H:%M:%S")
#         current_time = datetime.now()
#         return current_time >= expiration_time
    # return False

def run_regex_signup(username, role, displayname):
    """Runs all the regex checks for the signup page."""
    flagged = False
    error = None
    if bool(re.search(r'[\s\[,"\'<>{\]]', displayname)) is True:
        flagged = True
        error = 'The display name contains a space or a special character.'
    elif bool(re.search(r'[\s[,"\'<>{\]]', username)) is True:
        flagged = True
        error = 'The username contains a space or a special character.'
    elif bool(re.search(r'[\s[,"\'<>{\]]', role)) is True:
        flagged = True
        error = 'The Role contains a space or a special character.'
    check = r'^[A-Za-z]{3,12}$'
    user_allowed = re.match(check, username)
    desplayname_allowed = re.match(check, displayname)
    if re.match(r'^[A-Za-z]{3,18}$', role) is True:
        flagged = True
        error = 'That Role name is too long. Must be between 1-18 letters.'

    if user_allowed == 'false' or desplayname_allowed == 'false':
        flagged = True
        error = 'That Username/Display name is too long. Must be between 1-12 letters.'

    if profanity.contains_profanity(username):
        flagged = True
        error = 'Your Username Contains Profanity, please remove.'
    elif profanity.contains_profanity(displayname):
        flagged = True
        error = 'Your Display Name Contains Profanity, please remove.'
    elif profanity.contains_profanity(role):
        flagged = True
        error = 'Your Role Contains Profanity, please remove.'

    if bool(re.search(r'[<>]', username)) is True:
        flagged = True
        error = 'HTML Elements are not allowed in your username!'
    elif bool(re.search(r'[<>]', displayname)) is True:
        flagged = True
        error = 'HTML Elements are not allowed in your display name!'
    elif bool(re.search(r'[<>]', role)) is True:
        flagged = True
        error = 'HTML Elements are not allowed in your role!'

    return (flagged, error)

def load_disposable_domains():
    """Loads and retuns the domains file."""
    with open('backend/domains.txt', 'r', encoding="utf-8") as file:
        return {line.strip() for line in file.readlines()}


def check_if_disposable_email(email):
    """Checks if the email used is a disposable email."""
    if '@' not in email:
        return 1

    email_domain = email.split('@')[1]
    disposable_domains = load_disposable_domains()

    if email_domain in disposable_domains:
        return 2
    return 0

def create_verification_code(user):
    """Creates and returns a verification code."""
    username_hash = hashlib.sha224(bytes(user['username'], 'utf-8')).hexdigest()
    email_hash = hashlib.sha224(bytes(user['email'], 'utf-8')).hexdigest()
    combined_hashes = username_hash + email_hash + user['password'] + (
        config["backend"]['secret_key'])
    verification_code = hashlib.sha224(bytes(combined_hashes, 'utf-8')).hexdigest()
    return verification_code

def create_user(username: str, passwd: str, email: str, role: str,
                displayname: str):
    """Adds the new user's data to the database."""
    while True:
        userid = str(uuid.uuid4())
        if userid not in database.distinct_userids():
            break
    current_time = datetime.now()
    time = current_time + timedelta(hours=10)
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S")
    database.add_accounts(
    {"username": username,
    "password": hashlib.sha384(bytes(passwd, 'utf-8')).hexdigest(),
    "userid": userid,
    "email": email,
    "role": role,
    "displayname": displayname,
    "locked": True,
    "formatted_time": formatted_time}
    )
    send_verification_email(
        username, email,
        create_verification_code({
            "username": username,
            "password": hashlib.sha384(bytes(passwd, 'utf-8')).hexdigest(),
            "email": email,
        }), userid)
    users_list[userid] = {'username': displayname, 'status': 'offline', 'perm': None}

def password(user):
    """Creates the verification email for the new user."""
    reset_code = create_verification_code(user)
    send_password_reset_email(user['username'], user["email"], reset_code,
                              user['userId'])
