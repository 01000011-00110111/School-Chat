[![Pylint](https://github.com/01000011-00110111/School-Chat/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/01000011-00110111/School-Chat/actions/workflows/pylint.yml)

# Class-Chat
This is a private chat made for chatting with friends. This chat has been made over our free time at highschool and is in no way made with the best ways you can do stuff. We use MongoDB for the database, with the backend written in python, (while using nginx as a reverse proxy) and a javascript front end.

Also not done whatsoever, many things have to be done beforehand

Steps to make the chat run

- Put your mongodb authentication string into `keys.py`
- create a venv (and install packages via poetry inside that venv)
- Make `chat.txt`, `Chat-backup.txt`, `chat-rooms_log.txt`, and `command_log.txt` inside the folder named backend
- Add your ssl pem and key into nginx and change them to your domain name
- Paste this config file into the `sites-enabled` directory where you have nginx installed (usually its somthing like `/etc/nginx`), and name it what your domain name is called:
  - change `yourdomain` to what your domain name is called
  - for the ssl keys and certs, replace `yourdomain` with whatever you named them, if its not your domain name.
  - change `<where your files are stored>` to where you have this downloaded to.
```
server {
    listen 80;
    listen [::]:80;
    server_name yourdomain www.yourdomain;
    return 302 https://$server_name$request_uri;
}


server {
    server_name yourdomain www.yourdomain;

    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    # The security headers, to try and prevent XSS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header Referrer-Policy "same-origin" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header Permissions-Policy "microphone=(), camera=(), usb=(), picture-in-picture=(), payment=(), web-share=()" always;
    add_header Content-Security-Policy "default-src 'self' 'unsafe-inline'; img-src *; script-src 'self' cdnjs.cloudflare.com 'unsafe-inline'" always;
    # SSL certs go here
    ssl_certificate         /etc/ssl/yourdomain.pem;
    ssl_certificate_key     /etc/ssl/yourdomain.key;
#    need to enable this in cloudflare dashboard, so we can confirm they are going through cloudflare, and not directly to the server
#    ssl_client_certificate  /etc/ssl/cloudflare.crt;
#    ssl_verify_client on;

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:5000;
    }

    location /static/ {
        alias <where your files are stored>/static/;
        expires 30d;
    }

    location /socket.io {
        include proxy_params;
        proxy_http_version 1.1;
        proxy_buffering off;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_pass http://127.0.0.1:5000/socket.io;
    }
}
```
- enable and run nginx with this command `sudo systemctl enable --now nginx.service`
- Run this command while in the venv to start the chat server, after nginx starts: `gunicorn --bind 127.0.0.1:5000 --worker-class eventlet --threads 10 -w 1 main:app`

This was created by
  cserver, and C7
