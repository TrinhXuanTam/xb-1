echo "Making database backup..."
sudo docker-compose exec web python manage.py dumpdata > "dumps/$(date +%F_%R).json"
echo "Database backup finished"
sudo docker-compose up
