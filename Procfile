web: daphne -b 0.0.0.0 -p $PORT norouzyteam.asgi:application
worker: python manage.py runworker channels --settings=norouzyteam.settings -v2
