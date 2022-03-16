#!/usr/bin/env sh

set -o errexit
set -o nounset


readonly cmd="$*"

postgres_ready() {
    (echo -n > /dev/tcp/db/5432) >/dev/null 2>&1
    return $?
}

until ! postgres_ready; do
    >&2 echo 'Starting postgres...'
    sleep 1
done

>&2 echo 'Postgres ready'
exec $cmd
