#!/usr/bin/env bash

# Make sure DB is started
python3 "${OPS_HOME}"/src/app/backend_pre_start.py

# Init DB
python3 "${OPS_HOME}"/src/app/initial_data.py
