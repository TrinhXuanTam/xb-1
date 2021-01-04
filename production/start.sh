docker-compose up -d
echo "Making database backup..."
docker-compose exec web python manage.py dumpdata --all --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > "dumps/$(date +%F-%R).json"
echo "Database backup finished"
echo "Server is running, to view server log enter: sh log.sh"
