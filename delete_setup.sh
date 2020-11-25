#!/bin/bash

port_number=80
server_name=8.8.8.8
home_folder=/home/dev


# echo "server {
#     listen $port_number;
#     server_name $server_name;

#     location = /favicon.ico { access_log off; log_not_found off; }
#     location /static/ {
#         root $home_folder/xb1;
#     }
    
#     location /media/ {
#         root /home/ridzodan/xb1/xb1;
#     }

#     location / {
#         include         uwsgi_params;
#         uwsgi_pass      unix:$home_folder/xb1/xb1.sock;
#     }
# }" > $home_folder/nginx_conf

echo "server {
  listen 80;
  server_name ikarie.sic.cz;
  return 301 https://ikarie.sic.cz$request_uri;
}

server {
    listen       443 ssl http2 default_server;                                                      
    server_name  ikarie.sic.cz;
    
    client_max_body_size 10M

    ssl_certificate "/etc/ssl/ikarie.sic.cz.crt";                                                                                          
    ssl_certificate_key "/etc/ssl/ikarie.sic.cz.key";       
    ssl_session_cache shared:SSL:1m;                                                                     
    ssl_session_timeout  10m;                                                                            
    ssl_ciphers HIGH:!aNULL:!MD5;                                                                        
    ssl_prefer_server_ciphers on;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/ridzodan/xb1;
    }

    location /media/ {
        root /home/ridzodan/xb1/xb1;
    }

    location / {
        proxy_set_header Host $http_host;                                                                
        proxy_set_header X-Real-IP $remote_addr;                                                         
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;                                     
        proxy_set_header X-Forwarded-Proto $scheme;
        include          uwsgi_params;
        uwsgi_pass       unix:/home/ridzodan/xb1/xb1.sock;
    }

    error_page 404 /404.html;                                                                            
        location = /40x.html {                                                                           
    }                                                                                                    
                                                                                                             
    error_page 500 502 503 504 /50x.html;                                                                
        location = /50x.html {                                                                           
    }
}" > $home_folder/nginx_conf

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
plugins = python3" > $home_folder/xb1.ini

#####################
# Setup django server
#####################

# Install python3
sudo apt-get update
sudo apt-get install python3-pip

# Move server source files to correct location
mv requirements.txt xb1/requirements.txt
mv xb1 $home_folder
mv uwsgi.service $home_folder/uwsgi.service
cd $home_folder
chmod 777 xb1

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
cd xb1
pip3 install -r requirements.txt

# Setup django db
python3 manage.py migrate
echo "Creating django superuser, please enter your login data."
python3 manage.py createsuperuser
python3 manage.py loaddata groups.json
python3 manage.py collectstatic
mkdir -p static
mv xb1/staticRoot/* static/
cd ..

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
