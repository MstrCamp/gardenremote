# GardenRemote
Websteuerung der Lillerschen Gartenlaube

## Deployment
*work in progress*
### Requirements
Install and enable requirements: [apache2](https://wiki.ubuntuusers.de/Apache_2.4/), [mod-wsgi](https://wiki.ubuntuusers.de/Apache/mod_wsgi/) and libgpiod2  
```
sudo apt install apache2 libapache2-mod-wsgi-py3 libgpiod2
sudo a2enmod wsgi
```

### apache2 config
Put user www-data in group gpio
```
sudo usermod -a -G gpio www-data
```

Allow server access to log folder by executing:
```
sudo chown -R pi:www-data /home/pi/GardenRemote/log/
sudo chmod 775 /home/pi/GardenRemote/log/
```

allow acces to server directory in */etc/apache2/apache2.conf*
```apache
<Directory /home/pi/GardenRemote>
    Options Indexes FollowSymLinks
    AllowOverride None
    Require all granted
</Directory>
```

Create Server Config file
```
sudo touch /etc/apache2/sites-available/GardenRemote.conf
nano /etc/apache2/sites-available/GardenRemote.conf
```

*/etc/apache2/sites-available/GardenRemote.conf*
```apache
<VirtualHost *:80>
    ServerName pi2laube
    ServerAdmin yourmail@mail.com
    WSGIScriptAlias / /home/pi/GardenRemote/app/> group=%{GLOBAL} application-group=%{GLOBAL}
    <Directory /home/pi/GardenRemote/app/>
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>
    ErrorLog ${APACHE_LOG_DIR}/error.log
    LogLevel warn
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```
Enable the new Configuration and disable the old default one
```
sudo a2dissite 000-default.conf && sudo a2ensite GardenRemote.conf && sudo systemctl reload apache2
```

## Development
### Pycharm Remote Interpreter
Manually create venv, install requirements and place file inside */venv*:
```bash
#!/bin/bash
source /home/pi/GardenRemote/venv/bin/activate
python "$@"
```
Configure file as Remote Interpreter