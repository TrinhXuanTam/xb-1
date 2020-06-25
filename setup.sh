#!/bin/bash

port_number=80
server_name=8.8.8.8
home_folder=/home/dev


echo "server {
    listen $port_number;
    server_name $server_name;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root $home_folder/xb1;
    }

    location / {
        include         uwsgi_params;
        uwsgi_pass      unix:$home_folder/xb1/xb1.sock;
    }
}" > nginx_conf

echo "[uwsgi]
project = xb1
base = $home_folder

chdir = %(base)/%(project)
home = %(base)/Env/%(project)
module = %(project).wsgi:application

master = true
processes = 5

socket = %(base)/%(project)/%(project).sock
chmod-socket = 666
vacuum = true
plugins = python3" > xb1.ini

#####################
# Setup django server
#####################

# Install python3
sudo apt-get update
sudo apt-get install python3-pip

# Upgrade pip
pip3 install --upgrade pip

# Install python virtualenv
sudo pip3 install virtualenv virtualenvwrapper

# Setup virtualenv wrapper
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export WORKON_HOME=~/Env
source /usr/local/bin/virtualenvwrapper.sh

# Create python virtualenv
mkvirtualenv xb1

# Install python required libraries
cd xb1/
pip3 install -r requirements.txt

####################
# Setup nginx server
####################

# Install nginx
sudo apt-get update
sudo apt-get install nginx

# Install uwsgi
sudo pip3 install uwsgi

# Move server configuration files to correct location in root directory
sudo mkdir -p /etc/nginx/sites-available
sudo mkdir -p /etc/uwsgi/sites
sudo mkdir -p /etc/systemd/system

sudo mv uwsgi.service /etc/systemd/system/uwsgi.service
sudo mv nginx_conf /etc/nginx/sites-available/xb1
sudo ln -s /etc/nginx/sites-available/xb1 /etc/nginx/sites-enabled
sudo mv xb1.ini /etc/uwsgi/sites/xb1.ini

# Restart nginx and uwsgi
sudo service nginx restart
sudo service uwsgi start
