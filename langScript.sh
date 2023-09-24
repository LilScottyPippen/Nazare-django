set -e

django-admin makemessages --all --ignore venv

msgfmt -o locale/en_US/LC_MESSAGES/django.mo locale/en_US/LC_MESSAGES/django.po