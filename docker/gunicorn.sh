#!/usr/bin/env sh

alembic upgrade head

gunicorn aphorism.wsgi:application -w 4
