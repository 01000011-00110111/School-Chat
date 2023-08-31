"""Stuff to handle accounts
    Copyright (C) 2023  cserver45, cseven
    License info can be viewed in main.py or the LICENSE file.
"""
import os
import re
import smtplib
import uuid
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def email_var_account(username, email, verification_code):
    # Email configuration
    URL = os.environ['URL']
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = os.environ['email']
    sender_password = os.environ['password']
    receiver_email = email
    subject = f'Verification of {username}!'

    # Create the email content
    for i in range(1):  # Send 1 emails (you can adjust the number as needed)
        verification_code_list = {username: verification_code}
        message_body = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {
                    font-family: Arial, sans-serif;
                }
                .container {
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    background-color: #f8f8f8;
                }
                .button {
                    display: inline-block;
                    padding: 10px 20px;
                    background-color: #007bff;
                    color: #ffffff;
                    text-decoration: none;
                    border-radius: 5px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Account Verification</h2>
                <p>Dear [Recipient's Name],</p>
                <p>To complete the verification process and gain access to all chat rooms, please click the button below:</p>
                <p><a class="button" href="[Verification Link]">Verify My Account</a></p>
                <p>If you did not request this verification, please ignore this email.</p>
                <p>Thank you for choosing our service!</p>
                <p>Sincerely,</p>
                <p>The BTG Team</p>
            </div>
        </body>
        </html>
        """

    message_body = message_body.replace("[Recipient's Name]", username)
    message_body = message_body.replace(
        "[Verification Link]", f'https://{URL}/verify/{verification_code}')

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    # message_id = f"<{uuid.uuid4()}@{URL}>"
    # msg['Message-ID'] = message_id

    message_id = f"<{uuid.uuid4()}@{URL}>"
    # print(message_id)
    msg.add_header('Message-ID', message_id)

    msg.attach(MIMEText(message_body, 'html'))
    # print(msg.as_string())

    # Connect to the SMTP server
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, receiver_email, msg.as_string())
        # print('Email sent successfully!')

    except Exception as e:
        print('An error occurred:', e)

    finally:
        server.quit()
        return verification_code_list


def is_account_expired(permission_str):
    """checks if the user's time matches the time (idk you explain it better to me please)"""
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
        error = 'That Role name is too long. It must be at least 1 letter long or under 18.'

    if user_allowed == 'false' or desplayname_allowed == 'false':
        flagged = True
        error = 'That Username/Display name is too long. It must be at least 1 letter long or 12 and under'

    return (flagged, error)