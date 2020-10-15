#!/bin/bash

home_folder=/home/dev

############################################################################
# Script downloads latest master commit from git repository and deploys it #
############################################################################


# Make backup of the database
mkdir -p $home_folder/db_backups
cp $home_folder/SP1/xb1/xb1/db.sqlite3 $home_folder/db_backups/$(date +%F_%R)_db.sqlite3

# Make backup of media files
mkdir -p $home_folder/media_backups
