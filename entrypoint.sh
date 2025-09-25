#!/bin/sh

echo "Sleeping 5 seconds to allow network/DNS to settle..."
sleep 5

echo "DB_HOST=$DB_HOST"
echo "DB_PORT=$DB_PORT"
echo "DB_USER=$DB_USER"
echo "DB_PASSWORD=$DB_PASSWORD"

while ! nc -z "$DB_HOST" "$DB_PORT"; do
  echo "Waiting for database connection at $DB_HOST:$DB_PORT..."
  sleep 1
done

echo "Database is up and running!"

python herbariet/manage.py migrate
python herbariet/manage.py makemigrations

echo "Django setup completed."

python herbariet/manage.py flush --no-input

python herbariet/manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
username = '${DJANGO_SUPERUSER_USERNAME:}';
password = '${DJANGO_SUPERUSER_PASSWORD:}';
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, password)
    print('Superuser created')
else:
    print('Superuser already exists')
"

python herbariet/manage.py collectstatic --no-input --clear

exec python herbariet/manage.py runserver 0.0.0.0:8000