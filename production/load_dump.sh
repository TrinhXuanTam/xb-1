#!/bin/bash
if [ "$#" -eq "0" ]
    then 
        echo "Please enter path to the dumpfile. For example:"
        echo "sh $0 2021-01-04_18:37.json"
        exit 1
else

    # Create database backup
    echo "Making database backup..."
    docker-compose exec web python manage.py dumpdata --all --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > "dumps/$(date +%F-%R).json"
    echo "Database backup finished"

    # Flush the database
    docker-compose exec web python manage.py reset_db

    # Load the dump file
    docker-compose exec web python manage.py loaddata xb1/dumps/$1

    # Migrate the database
    docker-compose exec web python manage.py migrate
fi
