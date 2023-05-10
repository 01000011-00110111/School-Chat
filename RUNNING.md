Steps to make the chat run

- Make a keys.py file andf put your environ keys for mongo and the menus
- Make chat.txt and backup.txt file 
- Install all packages needed to run (will add more detail later)
- Run this command: gunicorn --bind 45.33.89.97:443 -k gevent --certfile 'school-chat.us.pem' --keyfile 'school-chat.us.key' -w 1 main:app