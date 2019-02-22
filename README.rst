Luncher
=======

Luncher from Hackathon

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django


:License: MIT

Getting started for development
-------------------------------

1. Run

    .. code-block:: bash

        docker-compose build
        docker-compose up

  to build and run two containers `postgres` and `django`. The app should be available at http://0.0.0.0:8000/

2. You might want to prepare database

    .. code-block:: bash

        docker-compose run --rm django python manage.py migrate
        docker-compose run --rm django python manage.py createsuperuser

  The created user can be used in http://0.0.0.0:8000/admin/ to provision database.

3. If you are want to run django outside the container, these commands will be useful

    .. code-block:: bash

        docker-compose up -d postgres
        ./tools/local_venv.sh
        source .venv/bin/activate
        python manage.py migrate
        ./tools/createsuperuser.sh admin admin@admin.com secretpassword
        python manage.py runserver 0.0.0.0:8000

Where to find answers about this cookiecutter mess
--------------------------------------------------

Main page: https://cookiecutter-django.readthedocs.io/en/latest/index.html


Continuous Integration
======================

We use GitLab runners for CI, so please see `.gitlab-ci.yml`.

See directory `provision` for more info about setting up Gitlab runners.
