
FROM python:3.9-alpine3.16


COPY requirements.txt /temp/requirements.txt
COPY ZorkaDjango /ZorkaDjango
WORKDIR /ZorkaDjango
EXPOSE 8000

COPY . /code/
COPY .env.docker /code/.env

RUN pip install -r /temp/requirements.txt