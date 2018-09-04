release: python manage.py migrate
web: gunicorn -c feed_app/gunicorn_server.py feed_app.wsgi --log-file -
