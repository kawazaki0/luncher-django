Luncher
=======

Luncher from Hackathon

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django


:License: MIT

Getting started for development
-------------------------------

1. Run::

    docker-compose build
    docker-compose up

to build and run two containers `postgres` and `django`. The app should be available at http://0.0.0.0:8000/

2. You might want to prepare database::

    docker-compose run --rm django python manage.py migrate
    docker-compose run --rm django python manage.py createsuperuser

The created user can be used in http://0.0.0.0:8000/admin/ to provision database.

3. If you are want to run django outside the container, these commands will be useful::

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements/local.txt
    docker-compose up -d postgres
    python manage.py runserver

Where to find answers about this cookiecutter mess
--------------------------------------------------

Main page: https://cookiecutter-django.readthedocs.io/en/latest/index.html
