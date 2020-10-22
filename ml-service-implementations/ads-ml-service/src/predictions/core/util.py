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


from __future__ import annotations

import logging
import typing
import numpy as np
from logging import Logger
from pathlib import Path
from typing import Text, Any, Dict


def rmdir(
        directory: Path
) -> None:
    logger: Logger = logging.getLogger(__name__)
    for item in directory.iterdir():
        if item.is_dir():
            rmdir(item)
            logger.info('Removed file: <{item}>'.format(item=item))
        else:
            item.unlink()
    directory.rmdir()
    logger.info('Removed directory: <{directory}>'.format(directory=directory))


def to_dataframe_compatible(kv_pair: Dict[Text: Any]) -> Dict:
    return {
        key: [val]
        for key, val in kv_pair.items()
    }


def data_to_str(data: typing.Any) -> typing.Text:
    result: typing.Text
    if np.issubdtype(type(data), np.number):
        # numpy numbers to string: https://github.com/numpy/numpy/pull/9941
        result = repr(data)
    else:
        result = str(data)
    return result
