find . -path "*/migrations/*.py" -not -name "__init__.py" -delete 
find . -path "*/migrations/*.pyc"  -delete

./manage.py makemigrations
./manage.py migrate

# create admin:admin
DJANGO_SUPERUSER_PASSWORD=admin \
DJANGO_SUPERUSER_USERNAME=admin \
DJANGO_SUPERUSER_EMAIL=admin@nonexist.com \
./manage.py createsuperuser \
--no-input