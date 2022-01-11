release: python manage.py migrate
web: daphne api.routing:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channels --settings=config.settings -v2