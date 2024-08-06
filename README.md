[![Pylint](https://github.com/01000011-00110111/School-Chat/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/01000011-00110111/School-Chat/actions/workflows/pylint.yml)

[![Ruff](https://github.com/01000011-00110111/School-Chat/actions/workflows/ruff.yml/badge.svg?branch=main)](https://github.com/01000011-00110111/School-Chat/actions/workflows/ruff.yml)

# School-Chat
This is a private chat made for chatting with friends. This chat has been made over our free time at highschool and is in no way made with the best ways you can do stuff. We use MongoDB for the database, with the backend written in python and a javascript front end. (while using nginx as a reverse proxy)

This chat is always gettings updated so keep updated on our work!

# **Setup**:

### Requirements
- Put your mongodb authentication string and other data into `example.keys.conf`
- Rename `example.keys.conf` to `keys.conf`
- In the data base make 2 databases named `Accounts` and `Rooms`
- Inside of Accounts make 3 collections named `Accounts`, `Customization`, and `Permission`
- Inside of Rooms make 4 collections named `Rooms`, `Permission`, `Messages`, and `Private`

## No systemd service (easy route)
#### NOTE: `$sudo shutdown` and `$sudo restart` will NOT work if you do not use systemd! (commands are removed at this time)
- Create a venv by running:
```bash
python -m venv venv
```
- To activate your venv run:
```bash
source venv/bin/activate
```
- To install the requirements run:
```bash
pip install -r requirements.txt
```
- Add your ssl pem and key into nginx and change them to your domain name
- Paste this config file into the `sites-enabled` directory where you have nginx installed (usually its somthing like `/etc/nginx`), and name it what your domain name is called:
  - change `yourdomain` to what your domain name is called
  - for the ssl keys and certs, replace `yourdomain` with whatever you named them, if its not your domain name.
  - change `<where your files are stored>` to where you have this downloaded to.
```nginx
# /etc/nginx/sites-enabled/yourdomain
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
    add_header Content-Security-Policy "default-src 'self'; style-src 'self' https://cdnjs.cloudflare.com/ 'unsafe-inline'; script-src 'self' cdnjs.cloudflare.com 'unsafe-inline';font-src 'self' https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.3.0/webfonts/;img-src *;";
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
- enable and run nginx with this command:
```bash
sudo systemctl enable --now nginx.service
```
- Run this command while in the venv to start the chat server, after nginx starts: 
```bash
python main.py
```


## Systemd route (auto restart and other nice features)
- make sure you have the optional systemd dependency installed run:
```bash
poetry install --extras "systemd"
```
- do the above, but also copy the `example.chatserverd.service` file and edit anywhere it mentions:
 - `<dir_path>` to where the files are stored
 - `<user>` for what user this is running under
 - rename the file to chatserverd.service
- Next, place that file inside the `~/.config/systemd/user` directory (create this if it does not exist)
- Run this command to allow your user to run systemd services when not logged in (to start on startup):
```bash
sudo loginctl enable-linger <user>
```
> (this must be run under a user that has root privlages)
- run (under the user you intend to run this):
```bash
systemctl --user daemon-reload
```
- After nginx is running then, run:
```bash
systemctl --user enable --now chatserverd.service
```
- it should just start working

### This was created by:
- [**cserver45**](https://github.com/cserver45) and [**C7**](https://github.com/01000011-00110111)

### Contributors:
-  [**CastyiGlitchxz**](https://github.com/CastyiGlitchxz)