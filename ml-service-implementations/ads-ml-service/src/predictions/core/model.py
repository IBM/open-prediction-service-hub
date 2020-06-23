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
import pickle
from logging import Logger
from typing import Any, Sequence, Dict, Text, Type

from pandas import DataFrame

from .. import schemas


class Model(object):
    def __init__(self, info: schemas.model.MLSchema, model: Any):
        self.info: schemas.model.MLSchema = info
        self.model: Any = model

    def __get_ordered_column_name_vec(self) -> Sequence[Text]:
        return [item.name for item in sorted(self.info.input_schema, key=lambda e: getattr(e, 'order'))]

    def __get_feat_type_map(self) -> Dict[Text, Type]:
        return {item.name: item.get_type() for item in self.info.input_schema}

    # TODO: better management for conversion error
    def invoke(
            self,
            data_input: Dict
    ) -> Any:
        logger: Logger = logging.getLogger(__name__)

        logger.debug('Received input dict <{input_dict}>'.format(input_dict=data_input))

        data: DataFrame = DataFrame.from_dict(
            data=data_input,
            orient='columns'
        ). \
            reindex(
            columns=self.__get_ordered_column_name_vec()
        ). \
            astype(
            dtype=self.__get_feat_type_map(),
            errors='ignore'
        )
        return getattr(self.model, self.info.method_name)(data)

    @staticmethod
    def from_pickle(
            pickle_file: bytes,
            model_name: Text = 'model',
            metadata_name: Text = 'model_config'
    ) -> Model:
        archive: Dict = pickle.loads(pickle_file)
        model: Model = archive.get(model_name)
        conf: Dict = archive.get(metadata_name)
        return Model(
            info=schemas.model.MLSchema(**conf),
            model=model,
        )
