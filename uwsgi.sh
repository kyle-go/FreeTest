uwsgi --socket 127.0.0.1:9002 --chdir mysite --wsgi-file flask_app.py --callable app --pidfile /home/ft/pidfile.pid --master --processes 2 --threads 2
