#!/usr/bin/env sh

set -o errexit
set -o nounset

# Initializing global variables and functions:
: "${FLASK_ENV:=development}"

# Fail CI if `FLASK_ENV` is not set to `development`:
if [ "$FLASK_ENV" != 'development' ]; then
  echo 'FLASK_ENV is not set to development. Running tests is not safe.'
  exit 1
fi

pyclean () {
  # Cleaning cache:
  find . \
  | grep -E '(__pycache__|\.perm|\.cache|\.static|\.py[cod]$)' \
  | xargs rm -rf
}

run_ci () {
  echo '[ci started]'
  set -x  # we want to print commands during the CI process.

  # Testing filesystem and permissions:
  touch .perm && rm -f .perm
  #touch '/var/www/django/media/.perm' && rm -f '/var/www/django/media/.perm'
  #touch '/var/www/django/static/.perm' && rm -f '/var/www/django/static/.perm'

  # Running tests:
  #pytest --dead-fixtures
  pytest

  set +x
  echo '[ci finished]'
}

# Remove any cache before the script:
pyclean

# Clean everything up:
trap pyclean EXIT INT TERM

# Run the CI process:
run_ci
