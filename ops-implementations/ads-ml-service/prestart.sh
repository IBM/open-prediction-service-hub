#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Make sure DB is started
python3 "${__dir}"/app/backend_pre_start.py

# Init DB
python3 "${__dir}"/app/initial_data.py
