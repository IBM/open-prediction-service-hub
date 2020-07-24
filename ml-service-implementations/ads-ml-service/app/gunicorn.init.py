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
ssl_settings = os.getenv('SSL_SETTINGS')


# Gunicorn config variables
workers = cpu_count() * 2 + 1
# Gunicorn needs to store its temporary file in memory (e.g. /dev/shm)
worker_tmp_dir = '/dev/shm'
# Container schedulers typically expect logs to come out on stdout/stderr, thus gunicorn is configured to do so
log_file = '-'
ssl_version = 'TLSv1_2'
bind = ':8080'
ca_certs = f'{ssl_settings}/ca.crt' if use_ssl else None
certfile = f'{ssl_settings}/server.crt' if use_ssl else None
keyfile = f'{ssl_settings}/server.key' if use_ssl else None
