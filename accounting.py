"""Stuff to handle accounts
    Copyright (C) 2023  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
import hashlib
import os
import re
import smtplib
import uuid
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from better_profanity import profanity

import word_lists

# get our custom whitelist words (that should not be banned in the first place)
profanity.load_censor_words(whitelist_words=word_lists.whitelist_words)
profanity.add_censor_words(word_lists.censored)


def email_var_account(username, email, verification_code, userid):
    # Email configuration
    URL = os.environ['URL']
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = os.environ['EMAIL']
    sender_password = os.environ['PASSWORD']
    receiver_email = email
    subject = f'Verification of {username}!'

    # Create the email content
    for _ in range(1):  # Send 1 emails (you can adjust the number as needed)
        verification_code_list = {username: verification_code}
        with open('templates/email_temp.html', "r", encoding="UTF-8") as f:
            message_body = f.read()
            print(message_body)

    message_body = message_body.replace("[Recipient's Name]", username)
    message_body = message_body.replace(
        "[Verification Link]",
        f'https://{URL}/verify/{userid}/{verification_code}')

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    message_id = f"<{uuid.uuid4()}@{URL}>"
    msg.add_header('Message-ID', message_id)

    msg.attach(MIMEText(message_body, 'html'))

    # Connect to the SMTP server
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, receiver_email, msg.as_string())

    finally:
        server.quit()

    return verification_code_list


def is_account_expired(permission_str):
    """Checks if the account has ran out of time before being deleted."""
    parts = permission_str.split(' ')
    if len(parts) == 3 and parts[0] == 'locked':
        expiration_time_str = ' '.join(parts[1:])
        expiration_time = datetime.strptime(expiration_time_str,
                                            "%Y-%m-%d %H:%M:%S")
        current_time = datetime.now()
        return current_time >= expiration_time


def run_regex_signup(SUsername, SRole, SDisplayname):
    """Run Checks on the username."""
    flagged = False
    error = None
    if bool(re.search(r'[\s\[,"\'<>{\]]', SUsername)) is True:
        flagged = True
        error = 'The display name contains a space or a special character.'
    elif bool(re.search(r'[\s[,"\'<>{\]]', SUsername)) is True:
        flagged = True
        error = 'The username contains a space or a special character.'
    elif bool(re.search(r'[\s[,"\'<>{\]]', SRole)) is True:
        flagged = True
        error = 'The Role contains a space or a special character.'
    check = r'^[A-Za-z]{3,12}$'
    user_allowed = re.match(check, SUsername)
    desplayname_allowed = re.match(check, SDisplayname)
    if re.match(r'^[A-Za-z]{3,18}$', SRole) is True:
        flagged = True
        error = 'That Role name is too long. Must be between 1-18 letters.'

    if user_allowed == 'false' or desplayname_allowed == 'false':
        flagged = True
        error = 'That Username/Display name is too long. Must be between 1-12 letters.'

    # check for profanity
    if profanity.contains_profanity(SUsername):
        flagged = True
        error = 'Your Username Contains Profanity, please remove.'
    elif profanity.contains_profanity(SDisplayname):
        flagged = True
        error = 'Your Display Name Contains Profanity, please remove.'
    elif profanity.contains_profanity(SRole):
        flagged = True
        error = 'Your Role Contains Profanity, please remove.'

    # simple check for html in signup elements
    if bool(re.search(r'[<>]', SUsername)) is True:
        flagged = True
        error = 'HTML Elements are not allowed in your username!'
    elif bool(re.search(r'[<>]', SDisplayname)) is True:
        flagged = True
        error = 'HTML Elements are not allowed in your display name!'
    elif bool(re.search(r'[<>]', SRole)) is True:
        flagged = True
        error = 'HTML Elements are not allowed in your role!'

    return (flagged, error)


# email checks
def load_disposable_domains():
    with open('backend/domains.txt', 'r') as file:
        return {line.strip() for line in file.readlines()}


def check_if_disposable_email(email):
    if '@' not in email:
        return 1

    email_domain = email.split('@')[1]
    disposable_domains = load_disposable_domains()

    if email_domain in disposable_domains:
        return 2
    else:
        return 0


def create_verification_code(user):
    """Creates the user's verification code."""

    # this creaets a SHA384 hash of the person's username, password, and email
    # along with a secret we add in an env var
    # we can't use the secret flask uses because it gets regnerated on server restart
    # to generate the verification code added on to the end of the url
    username_hash = hashlib.sha224(bytes(user['username'],
                                         'utf-8')).hexdigest()
    email_hash = hashlib.sha224(bytes(user['email'], 'utf-8')).hexdigest()
    combined_hashes = username_hash + email_hash + user[
        'password'] + os.environ['SECRET_KEY']
    verification_code = hashlib.sha224(bytes(combined_hashes,
                                             'utf-8')).hexdigest()
    return verification_code
