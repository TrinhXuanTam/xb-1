sudo docker-compose up -d
echo "Making database backup..."
sudo docker-compose exec web python manage.py dumpdata --exclude=auth --exclude=contenttypes > "dumps/$(date +%F_%R).json"
echo "Database backup finished"
