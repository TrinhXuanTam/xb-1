#!/bin/bash

# Install python3 and pip3 if does not exist
LINUX_REQUIREMENTS=('git' 'build-essential' 'python3' 'python3-pip' 'nginx');
echo "Checking linux requirements...";
for package in "${LINUX_REQUIREMENTS[@]}"
    do
        echo "Installing '$package'...";
        apt-get -y install $package;
        if [ $? -ne 0 ]; then
            echo "Error occured when installing '$package'";
            exit 1;
        fi
    done

# Installing python requirements
PYTHON_REQUIREMENTS=('virtualenv');
for package in "${PYTHON_REQUIREMENTS[@]}"
    do
        echo "Installing '$package'..."
        yes | pip3 install $package
        if [ $? -ne 0 ]; then
            echo "Error occured when installing '$package'"
            exit 1
        fi
    done


# Start virtual enviroment
virtualenv --python=/usr/bin/python3 xb1_env;
source xb1_env/bin/activate || exit 1;

# Upgrade pip
yes | pip3 install --upgrade pip

# Install project requirements
yes | pip3 install -r requirements.txt;

# Turn on project
cd xb1;
timeout 5 python3 manage.py runserver;

# Migrate database
python3 manage.py migrate;

# Collect static files
python3 manage.py collectstatic;

# Run server
python3 manage.py runserver  0.0.0.0:8000;
