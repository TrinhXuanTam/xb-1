#!/bin/bash

# Activate virtual enviroment
source xb1_env/bin/activate;

# Run server
cd xb1;
python manage.py runserver  0.0.0.0:8000;
