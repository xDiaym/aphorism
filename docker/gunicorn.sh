#!/usr/bin/env sh

flask db upgrade

gunicorn aphorism.wsgi:application -w 4
