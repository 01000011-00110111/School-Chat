[![Pylint](https://github.com/01000011-00110111/School-Chat/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/01000011-00110111/School-Chat/actions/workflows/pylint.yml)

# Class-Chat
This is a private chat made for chatting with friends. This chat has been made over our free time at highschool and is in no way made with the best ways you can doo stuff. The Database was ran using mongodb and the backend was python with a java script front end.
Read running.md for how to setup the server!

Also not done whatsoever, many things have to be done beforehand

Steps to make the chat run

- Make a keys.py file andf put your environ keys for mongo and the menus
- Make chat.txt and backup.txt file 
- Install all packages needed to run (will add more detail later)
- Run this command: gunicorn --bind 45.33.89.97:443 -k gevent --certfile 'school-chat.us.pem' --keyfile 'school-chat.us.key' -w 1 main:app

This was created by
  cserver, and C7
