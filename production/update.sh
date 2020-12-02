sudo docker-compose up -d
echo "Making database backup..."
sudo docker-compose exec web python manage.py dumpdata > "dumps/$(date +%F_%R).json"
echo "Database backup finished"
sudo docker-compose stop
sudo docker-compose pull web
sudo docker-compose build
sudo docker-compose exec web python manage.py migrate --no-input
sudo docker-compose exec web python manage.py collectstatic --no-input --clear
echo "Updating server has successfully finished."
