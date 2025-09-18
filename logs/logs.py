"""logs/logs.py: manage logs for backend services 
    Copyright (C) 2023-2025  cserver45, cseven, CastyiGlitchxz
    License info can be viewed in app.py or the LICENSE file.
"""

from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    filename='logs/app.log', 
    filemode='a', 
    format='%(asctime)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

def log_message_sent(user_id, roomid, message):
    message_logger = logging.getLogger('message_logger')
    handler = logging.FileHandler('logs/messages.log')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    message_logger.addHandler(handler)
    message_logger.setLevel(logging.INFO)
    
    message_logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')} - [{roomid}]Message sent by {user_id}: {message}")
    
    message_logger.removeHandler(handler)
    handler.close()

def log_user_connected(user_id):
    logging.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')} - User connected: {user_id}")

def log_user_disconnected(user_id):
    logging.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')} - User disconnected: {user_id}")

def log_signup(email, username, display_name): #a very basic log for signup (all of logs.py needs improvements)
    logging.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')} - Account created named: {username}, displayname: {display_name}, and email: {email}")