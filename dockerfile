FROM python:3.11-slim

RUN mkdir code
WORKDIR code

ADD . /code/
ADD .env.docker /code/.env

RUN pip install -r requirements.txt
RUN python3 manage.py collectstatic

# CMD gunicorn ZorkaDjango.wsgi:application -b 0.0.0.0:8000