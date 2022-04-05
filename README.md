# GardenRemote
Websteuerung der Lillerschen Gartenlaube


## Requirements
```sudo apt install libgpiod2```

## apache2 config
put user www-data in group gpio

install and enable mod-wsgi for apache

allow acces to server directory in apache2.conf
```
<Directory /home/pi/GardenRemote>
    Options Indexes FollowSymLinks
    AllowOverride None
    Require all granted
</Directory>
```

```
sudo touch /etc/apache2/sites-available/GardenRemote.conf
vim /etc/apache2/sites-available/GardenRemote.conf
```

```
<VirtualHost *:80>
    ServerName pi2laube
    ServerAdmin yourmail@mail.com
    WSGIScriptAlias / /home/pi/GardenRemote/app/>
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

```
sudo a2ensite GardenRemote.conf
sudo a2dissite 000-default.conf
sudo systemctl reload apache2
```