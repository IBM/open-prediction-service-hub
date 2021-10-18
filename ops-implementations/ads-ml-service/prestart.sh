#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

function init_rev() {
  echo "Initiating alembic revision"
  python3 -m alembic stamp "9c64c3521fc1"
}

function db_migration() {
  echo "Upgrading alembic revision to head"
  python3 -m alembic upgrade head
}

# Make sure DB is started
python3 "${__dir}"/app/backend_pre_start.py

# Run migrations
if python3 -m alembic current | grep -m 1 -o -q -E "[^[:space:]]{12}" - ; then
  db_migration
else
  init_rev
  db_migration
fi



# Init DB
python3 "${__dir}"/app/initial_data.py
