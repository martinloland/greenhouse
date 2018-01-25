# greenhouse
A django driven automatic smart greenhouse

## General preperations

### Upgrade debian
```
sudo apt-get update
sudo apt-get upgrade
```

### Change python version
```
find /usr/bin -name "python*" -print # find the installed versions of python
sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.5 2
```
To verify, `python --version` prints the version in use.

### Virtual enviorment
```
sudo pip install virtualenv virtualenvwrapper
# mkdir ~/.virtualenvs maybye not needed?
export WORKON_HOME=~/.virtualenvs
nano ~/.bashrc # add and save:
source ~/.local/bin/virtualenvwrapper.sh
```
To verify, the command `workon` should now work.



## Installation of django, nginx, uWSGI

### Clone git and create env
```
git clone https://github.com/martinloland/greenhouse.git
cd greenhouse/
mkvirtualenv greenhouse
pip install -r requirements.txt
```

### Configure static ip
https://www.modmypi.com/blog/how-to-give-your-raspberry-pi-a-static-ip-address-update
```
sudo nano /etc/dhcpcd.conf
```

add one or multiple snippets to end:
```
interface eth0

static ip_address=192.168.0.10/24
static routers=192.168.0.1
static domain_name_servers=192.168.0.1

interface wlan0

static ip_address=192.168.0.189/24
static routers=192.168.0.1 #Default gateway
static domain_name_servers=192.168.0.1
```
Run `ifconfig` and it should show that ip address under inet
Port forward on the router:
![alt tag](https://raw.githubusercontent.com/martinloland/greenhouse/master/port_forward.PNG)
The global IP address can be found on the router

### uwsgi and nginx
```
sudo pip install uwsgi
sudo apt-get install nginx
sudo ln -s ~/greenhouse/mysite/mysite_nginx.conf /etc/nginx/sites-enabled/
sudo /etc/init.d/nginx restart
```

### Test
```
python manage.py collectstatic
uwsgi --ini ~/greenhouse/mysite/mysite_uwsgi.ini
```
Should displat the webpage in the browser

### Deployment
```
deactivate
sudo pip install uwsgi # system wide installation
uwsgi --ini ~/greenhouse/mysite/mysite_uwsgi.ini
```

### Emperor mode
```
# create a directory for the vassals
sudo mkdir /etc/uwsgi
sudo mkdir /etc/uwsgi/vassals
# symlink from the default config directory to your config file
sudo ln -s /home/pi/greenhouse/mysite/mysite_uwsgi.ini /etc/uwsgi/vassals/
```

### Give permissions
```
sudo usermod -a -G www-data pi
sudo chgrp www-data /home/pi/greenhouse/mysite
sudo chmod g+rwxs /home/pi/greenhouse/mysite
```


## Logging installation
```
deactivate
mkvirtualenv logging
pip install -r requirements_logging.txt
```



## Start at boot
```
sudo nano /etc/rc.local # and add:
/home/pi/.virtualenvs/logging/bin/python /home/pi/greenhouse/mysite/log_and_manage.py debug &
sudo uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data
```

Alternatively, save output from rc.local to file, add this rc.local before the above.
```
exec 2> /tmp/rc.local.log      # send stderr from rc.local to a log file
exec 1>&2                      # send stdout to the same log file
```

## Practical commands:
```
sudo /etc/init.d/nginx restart
sudo shutdown -r now
```