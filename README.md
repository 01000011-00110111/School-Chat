[![Pylint](https://github.com/01000011-00110111/School-Chat/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/01000011-00110111/School-Chat/actions/workflows/pylint.yml)

# Class-Chat
This is a private chat made for chatting with friends. This chat has been made over our free time at highschool and is in no way made with the best ways you can do stuff. The Database was ran using MongoDB, with the backend python and a javascript front end.

Also not done whatsoever, many things have to be done beforehand

Steps to make the chat run

- Make a keys.py file andf put your environ keys for MongoDB and the menus
- create a venv (and install packages via poetry inside that venv)
- Make chat.txt and Chat-backup.txt files inside a folder named backend
- Add your ssl pem and key in the chats main folder
- Run this command while in the venv: gunicorn --bind YourServerIP:443 -k gevent --certfile 'example.com.pem' --keyfile 'example.com.key' -w 1 main:app
  - Change the 'yourserverip' to the ip of your server, that is accesible via whatever network you are on
  - Change the 'example.com' to whatever you domain names are, or whatever your .pem and .key files are named

This was created by
  cserver, and C7
