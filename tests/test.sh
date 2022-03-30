#!/usr/bin/env sh

set -o errexit
set -o nounset

docker-compose -f docker-compose.yml \
    -f docker-compose.override.yml config --quiet

docker-compose build
docker-compose run --user=root --rm web ./docker/ci.sh
