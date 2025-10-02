#!/bin/sh

echo "Sleeping 5 seconds to allow network/DNS to settle..."
sleep 5


# Wait for the database to be ready
while ! nc -z "$DB_HOST" "$DB_PORT"; do
  echo "Waiting for database connection at $DB_HOST:$DB_PORT..."
  sleep 1
done

echo "Database is up and running!"

python herbariet/herbariet/manage.py makemigrations
python herbariet/herbariet/manage.py makemigrations home
python herbariet/herbariet/manage.py migrate

echo "Wagtail setup completed."


python herbariet/herbariet/manage.py flush --no-input

echo "
import os
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_NAME')
password = os.environ.get('DJANGO_SUPERUSER_PASS')
usermail = os.environ.get('DJANGO_SUPERUSER_MAIL')
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, usermail, password)
    print('Superuser created')
else:
    print('Superuser already exists')
" | python herbariet/herbariet/manage.py shell

python herbariet/herbariet/manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_NAME')
password = os.environ.get('DJANGO_SUPERUSER_PASS')
usermail = os.environ.get('DJANGO_SUPERUSER_MAIL')
if not User.objects.filter(username=username).exists():
  User.objects.create_superuser(username, usermail, password)
  print('Superuser created')
else:
  print('Superuser already exists')
EOF

python herbariet/herbariet/manage.py collectstatic --no-input --clear

exec python herbariet/herbariet/manage.py runserver 0.0.0.0:8000
