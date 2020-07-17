#!/usr/bin/env bash


__dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Make sure DB is started
python3 "${__dir}"/src/predictions/backend_pre_start.py

# Init DB
python3 "${__dir}"/src/predictions/initial_data.py
