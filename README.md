1. set up [nginx](config_files/nginx.conf)

2. create [service](config_files/gunicorn)

3. enable service (so it runs on boot)
    `sudo systemctl enable dashboard`
    `sudo systemctl status dashboard`

4. `sudo nano /etc/systemd/system/dashboard.service`



