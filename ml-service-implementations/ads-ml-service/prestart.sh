#!/usr/bin/env bash

# Make sure DB is started
python3 "${OPS_HOME}"/app/backend_pre_start.py

# Init DB
python3 "${OPS_HOME}"/app/initial_data.py
