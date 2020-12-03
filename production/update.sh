sudo docker-compose up -d
echo "Making database backup..."
sudo docker-compose exec web python manage.py dumpdata --exclude=auth --exclude=contenttypes > "dumps/$(date +%F_%R).json"
echo "Database backup finished"
sudo docker-compose stop
sudo docker-compose pull web
sudo docker-compose up --build -d
sudo docker-compose exec web python manage.py migrate --no-input
sudo docker-compose exec web python manage.py collectstatic --no-input --clear
sudo docker-compose stop
echo "Updating server has successfully finished."
