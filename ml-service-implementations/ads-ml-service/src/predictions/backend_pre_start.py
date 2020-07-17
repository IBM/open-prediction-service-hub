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


import logging
from typing import NoReturn

from predictions.db.session import SessionLocal
from tenacity import before_log, after_log, retry, stop_after_attempt, wait_fixed


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 10  # 10 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.INFO)
)
def init() -> NoReturn:
    try:
        db = SessionLocal()
        db.execute('SELECT 1')
    except Exception as e:
        logger.error(e)
        raise e


def main() -> NoReturn:
    logger.info('Service init starting')
    init()
    logger.info('Service init finished')


if __name__ == '__main__':
    main()
