[![Pylint](https://github.com/01000011-00110111/School-Chat/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/01000011-00110111/School-Chat/actions/workflows/pylint.yml)

[![Ruff](https://github.com/01000011-00110111/School-Chat/actions/workflows/ruff.yml/badge.svg?branch=main)](https://github.com/01000011-00110111/School-Chat/actions/workflows/ruff.yml)

# School-Chat
This is a private chat made for chatting with friends. This chat has been made over our free time at highschool and is in no way made with the best ways you can do stuff. We use MongoDB for the database, with the backend written in python and a javascript front end. (while using nginx as a reverse proxy)

This chat is always gettings updated so keep updated on our work!

# **Setup**:

### Requirements
- Put your mongodb authentication string and other data into `cores/config/example.keys.conf`
- Rename `example.keys.conf` to `keys.conf`
- In the data base make 2 databases named `Accounts` and `Rooms`
- Inside of Accounts make 3 collections named `Accounts`, `Customization`, and `Permission`
- Inside of Rooms make 4 collections named `Rooms`, `Permission`, `Messages`, and `Private`

## No systemd service (easy route)
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
- Paste this config file into the `sites-available` directory where you have nginx installed (usually its somthing like `/etc/nginx`), and name it what your domain name is called:
  - change `yourdomain` to what your domain name is called
  - for the ssl keys and certs, replace `yourdomain` with whatever you named them, if its not your domain name.
  - change `<where your files are stored>` to where you have this downloaded to.
```nginx
server {
    listen 80;
    server_name www.yourdomain;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name www.yourdomain;

    # SSL certificate paths (adjust to your actual cert files)
    ssl_certificate         /etc/ssl/yourdomain.pem;
    ssl_certificate_key     /etc/ssl/yourdomain.key;

    # React build directory
    root /home/<account_name>/<chat_dir>/frontend/build;
    index index.html;

    # Main frontend route handler (React)
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Serve static assets (CSS, JS, etc.)
    location /static/ {
        root /home/<account_name>/<chat_dir>/frontend/build;
        expires 30d;
        access_log off;
    }

    # Handle WebSocket and API routes through Sanic (via Gunicorn)
    location /socket.io {
        proxy_pass http://127.0.0.1:5000/socket.io;
        proxy_http_version 1.1;
        proxy_buffering off;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:5000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    #error_page 404 /index.html;
}
```
- enable and run nginx with this command:
```bash
sudo systemctl enable --now nginx.service
```
- Run this command while in the venv to start the chat server, after nginx starts: 
```bash
sanic app:app --host=127.0.0.1 --port=5000 --workers=1
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
- Next, place that file inside the `/etc/systemd/system` directory (create this if it does not exist)
> (this must be run under a user that has root privlages)
- run (under the user you intend to run this):
```bash
systemctl daemon-reload
```
- After nginx is running then, run:
```bash
systemctl enable --now chatserverd.service
```
- it should just start working

### This was created by:
- [**cserver45**](https://github.com/cserver45) and [**C7**](https://github.com/01000011-00110111)

### Contributors:
-  [**CastyiGlitchxz**](https://github.com/CastyiGlitchxz)