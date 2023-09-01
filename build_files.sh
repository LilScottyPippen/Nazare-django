pip install -r requirements.txt
python3 manage.py collectstatic
redis-server & celery -A ZorkaDjango worker & py manage.py runserver