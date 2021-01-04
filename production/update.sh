mkdir -p media
mkdir -p dumps
mkdir -p staticfiles

chgrp docker media
chgrp docker dumps
chgrp docker staticfiles

chmod g+w media
chmod g+w dumps
chmod g+w staticfiles

docker-compose up -d
echo "Making database backup..."
docker-compose exec web python manage.py dumpdata --all --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > "dumps/$(date +%F-%R).json"
echo "Database backup finished"
docker-compose stop
docker-compose pull web
docker-compose up --build -d
docker-compose exec web python manage.py migrate --no-input
docker-compose exec web python manage.py collectstatic --no-input --clear --user xb1
docker-compose stop
echo "Updating server has successfully finished."
