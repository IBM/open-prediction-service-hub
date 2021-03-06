#!/usr/bin/env python3
#
# Copyright 2020 IBM
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.IBM Confidential
#


import os

from multiprocessing import cpu_count


TRUE = ('TRUE', 'True', 'true', '1')


use_ssl = True if os.getenv('ENABLE_SSL') in TRUE else False
settings = os.getenv('SETTINGS')


# Gunicorn config variables
workers = int(os.getenv('GUNICORN_WORKER_NUM')) \
    if os.getenv('GUNICORN_WORKER_NUM') and int(os.getenv('GUNICORN_WORKER_NUM')) > 0 \
    else cpu_count() * 2 + 1
# Gunicorn needs to store its temporary file in memory (e.g. /dev/shm)
worker_tmp_dir = '/dev/shm'
# Container schedulers typically expect logs to come out on stdout/stderr, thus gunicorn is configured to do so
log_file = '-'
ssl_version = 'TLSv1_2'
bind = ':8080'
ca_certs = f'{settings}/ca.crt' if use_ssl else None
certfile = f'{settings}/server.crt' if use_ssl else None
keyfile = f'{settings}/server.key' if use_ssl else None
timeout = int(os.getenv('GUNICORN_TIMEOUT')) \
    if os.getenv('GUNICORN_TIMEOUT') and int(os.getenv('GUNICORN_TIMEOUT')) > 0 \
    else 30
