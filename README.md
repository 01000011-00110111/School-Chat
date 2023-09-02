[![Pylint](https://github.com/01000011-00110111/School-Chat/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/01000011-00110111/School-Chat/actions/workflows/pylint.yml)

# Class-Chat
This is a private chat made for chatting with friends. This chat has been made over our free time at highschool and is in no way made with the best ways you can do stuff. We use MongoDB for the database, with the backend written in python, (while using nginx as a reverse proxy) and a javascript front end.

Also not done whatsoever, many things have to be done beforehand

Steps to make the chat run

## Requirements to run (The chat data)
- Put your mongodb authentication string and other strings and your keys for mod and dev into `example.keys.py`
- Rename `example.keys.py` to `keys.py`
- in the data base make a database named `Chat` and add 3 collections named `Accounts`, `Online`, `rooms`
- inside of rooms add 4 documents to the database
```
"roomid":"ilQvQwgOhm9kNAOrRqbr",
"generatedBy":"[SYSTEM]",
"generatedAt":"2022-10-24T20:00:00",
"roomName":"add your room name",
"canSend":"everyone",
"whitelisted":"everyone",
"blacklisted":"empty",
"locked":"false",
"messages":[]
```

```
"roomid":"jN7Ht3giH9EDBvpvnqRB",
"generatedBy":"[SYSTEM]",
"mods":"",
"generatedAt":"2023-07-29T21:30:00",
"roomName":"add your room name",
"canSend":"devonly",
"whitelisted":"devonly",
"blacklisted":"empty",
"locked":"false",
"messages":[]
```

```
"roomid":"wTZOyPgelLPWTittBAjj",
"generatedBy":"[SYSTEM]",
"mods":"",
"generatedAt":"2023-08-25T11:20:00",
"roomName":"add your room name",
"canSend":"modonly",
"whitelisted":"modonly",
"blacklisted":"empty",
"locked":"false",
"messages":[]
```

```
"roomid":"zxMhhAPfWOxuZylxwkES",
"generatedBy":"[SYSTEM]",
"mods":"",
"generatedAt":"2023-07-1T21:53:00",
"roomName":"add your room name",
"canSend":"everyone",
"whitelisted":"lockedonly",
"blacklisted":"empty",
"locked":"false",
"messages":[]
```
## No systemd service (easy route)
#### NOTE: `$sudo shutdown` and `$sudo restart` will NOT work if you do not use systemd!
- create a venv (and install packages via poetry inside that venv)
- Make `Chat-backup.txt`, `chat-rooms_log.txt`, `permission.txt`, `accounts.txt`, and `command_log.txt` inside the folder named backend
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


## Systemd route (auto restart and other nice features)
- do the above, but also copy the `example.chatserverd.service` file and edit anywhere it mentions:
 - `<dir_path>` to where the files are stored
 - `<user>` for what user this is running under
 - rename the file to chatserverd.service
- Next, place that file inside the `~/.config/systemd/user` directory (create this if it does not exist)
- Run this command to allow your user to run systemd services when not logged in (to start on startup) `sudo loginctl enable-linger <user>` (this must be run under a user that has root privlages)
- run (under the user you intend to run this) `systemctl --user daemon-reload`
- then, run `systemctl --user enable --now chatserverd.service` after nginx is running
- it should just start working

This was created by
  cserver and C7
