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
from typing import Mapping, Text, Optional, Sequence, Any, Dict, Type, List

from .feature import Feature
from .output_schema import OutputSchema
from pandas import DataFrame
from pydantic import BaseModel, Field


class Metric(BaseModel):
    name: Text = Field(..., description='Name of metric')
    value: Text = Field(..., description='Value of metric')


class Metadata(BaseModel):
    description: Text = Field(..., description='Description of model')
    author: Text = Field(..., description='Author of model')
    trained_at: Text = Field(..., description='Training date')
    class_names: Optional[Dict[int, Text]] = Field(
        None, description='Lookup table for class index <-> class name'
    )
    metrics: List[Metric] = Field(..., description='Metrics for model')


class MLSchema(BaseModel):
    """Model independent information"""
    name: Text = Field(..., description='Name of model')
    version: Text = Field(..., description='Version of model')
    method_name: Text = Field(..., description='Name of method. (e.g predict, predict_proba)')
    input_schema: Sequence[Feature] = Field(..., description='Input schema of ml model')
    output_schema: Optional[OutputSchema] = Field(..., description='Output schema of ml model')
    metadata: Metadata = Field(..., description='Additional information for ml model')


class Model(object):
    def __init__(self, info: MLSchema, model: Any):
        self.info: MLSchema = info
        self.model: Any = model

    def __get_ordered_column_name_vec(self) -> Sequence[Text]:
        return [item.name for item in sorted(self.info.input_schema, key=lambda e: getattr(e, 'order'))]

    def __get_feat_type_map(self) -> Mapping[Text, Type]:
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
            info=MLSchema(**conf),
            model=model,
        )
