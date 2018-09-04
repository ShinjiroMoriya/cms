release: python manage.py migrate
web: gunicorn -c feed/gunicorn_server.py feed.wsgi --log-file -
