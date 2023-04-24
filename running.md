#Boot command:
gunicorn --bind 45.33.89.97:443 -k gevent --certfile 'school-chat.us.pem' --keyfile 'school-chat.us.key' -w 1 main:app