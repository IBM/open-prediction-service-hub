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

import connexion
import argparse
from openapi_server import encoder


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p',
        '--port',
        action='store',
        dest='port',
        help='port of your choice to run the app',
        default=8080,
        metavar=8080
    )
    args = parser.parse_args()
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Open Prediction Service'}, pythonic_params=True)
    app.run(port=args.port)


if __name__ == '__main__':
    main()
