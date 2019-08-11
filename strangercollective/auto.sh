git pull
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
touch /var/www/www_strangercollective_com_wsgi.py