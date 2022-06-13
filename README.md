# GardenRemote
Websteuerung der Lillerschen Gartenlaube

## Deployment
*work in progress*
### Requirements
Install and enable requirements: [apache2](https://wiki.ubuntuusers.de/Apache_2.4/), [mod-wsgi](https://wiki.ubuntuusers.de/Apache/mod_wsgi/), libgpiod2 and python3-venv  
```
sudo apt install apache2 libapache2-mod-wsgi-py3 libgpiod2 python3-venv
sudo a2enmod wsgi
```

### Installation
Clone the repository from GitHub
```
cd ~
git clone https://github.com/MstrCamp/gardenremote.git
```

Create a new python virtual environment inside the program directory and install the required packages
```
cd ~/gardenremote
python3 -m venv
source venv/bin/activate
pip install -r requirements.txt
```

Allow the apache server access to the log folder by executing:
```
sudo chown -R pi:www-data /home/pi/gardenremote/log/
sudo chmod 775 /home/pi/gardenremote/log/
```

### apache2 config
Put user www-data in group gpio
```
sudo usermod -a -G gpio www-data
```

allow acces to server directory in */etc/apache2/apache2.conf*
```apache
<Directory /home/pi/gardenremote>
    Options Indexes FollowSymLinks
    AllowOverride None
    Require all granted
</Directory>
```

Create Server Config file
```
sudo touch /etc/apache2/sites-available/gardenremote.conf
nano /etc/apache2/sites-available/gardenremote.conf
```

*/etc/apache2/sites-available/GardenRemote.conf*
```apache
<VirtualHost *:80>
    ServerName pi2laube
    ServerAdmin yourmail@mail.com
    WSGIScriptAlias / /home/pi/gardenremote/gardenremote.wsgi process-group=%{GLOBAL} application-group=%{GLOBAL}
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
sudo a2dissite 000-default.conf && sudo a2ensite gardenremote.conf && sudo systemctl reload apache2
```

## Development
### Pycharm Remote Interpreter
Manually create venv, install requirements and place file inside */venv*:
```bash
#!/bin/bash
source /home/pi/gardenremote/venv/bin/activate
python "$@"
```
Configure file as Remote Interpreter