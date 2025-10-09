#!/bin/sh

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

# Create superuser (only once)
python herbariet/herbariet/manage.py shell -c "
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
"

# Create default locale and Wagtail root page if needed
python herbariet/herbariet/manage.py shell -c "
from wagtail.models import Site, Page, Locale
from django.conf import settings

# Create default locale if it doesn't exist
locale, created = Locale.objects.get_or_create(
    language_code=settings.LANGUAGE_CODE,
    defaults={'language_code': settings.LANGUAGE_CODE}
)
if created:
    print(f'Default locale {settings.LANGUAGE_CODE} created')
else:
    print(f'Default locale {settings.LANGUAGE_CODE} already exists')

# Create root page if it doesn't exist
if not Page.objects.filter(depth=1).exists():
    root = Page.add_root(title='Root')
    try:
        from home.models import HomePage
        home = HomePage(title='Home', slug='home')
        root.add_child(instance=home)
        Site.objects.filter(is_default_site=True).update(root_page=home)
        print('Wagtail root page created')
    except ImportError:
        print('HomePage model not found, using basic Page')
        Site.objects.filter(is_default_site=True).update(root_page=root)
else:
    print('Wagtail pages already exist')
"

python herbariet/herbariet/manage.py collectstatic --no-input --clear

exec python herbariet/herbariet/manage.py runserver 0.0.0.0:8000