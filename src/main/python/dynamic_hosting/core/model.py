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

import base64
import json
import logging
import pickle
from io import BytesIO
from logging import Logger
from pathlib import Path
from typing import Mapping, Text, Optional, Sequence, Any, Dict, Type, List
from zipfile import ZipFile

from dynamic_hosting.core.feature import Feature
from dynamic_hosting.core.util import base64_to_obj, obj_to_base64
from dynamic_hosting.openapi.output_schema import OutputSchema
from pandas import DataFrame
from pydantic import BaseModel, Field, validator

MODEL_PICKLE_FILE_NAME: Text = 'archive.pkl'
MODEL_ARCHIVE_NAME: Text = 'archive.zip'
MODEL_CONFIG_FILE_NAME: Text = 'conf.json'


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


class Model(MLSchema):
    """Internal representation of ML model"""
    model: Text = Field(..., description='Pickled model in base64 format')

    @validator('model', always=True)
    def type_check(cls, m) -> Type:
        if base64_to_obj(m) is not None:
            return m
        else:
            raise ValueError(f'Model not supported: {m}')

    def get_ordered_column_name_vec(self) -> Sequence[Text]:
        return [item.name for item in sorted(self.input_schema, key=lambda e: getattr(e, 'order'))]

    def get_feat_type_map(self) -> Mapping[Text, Type]:
        return {item.name: item.get_type() for item in self.input_schema}

    def has_attr(self, attr: Text) -> bool:
        return hasattr(base64_to_obj(self.model), attr)

    def get_attr(self, attr: Text) -> Any:
        return getattr(base64_to_obj(self.model), attr)

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
            columns=self.get_ordered_column_name_vec()
        ). \
            astype(
            dtype=self.get_feat_type_map(),
            errors='ignore'
        )
        return self.__invoke__(data)

    def __invoke__(
            self,
            data_input: DataFrame
    ) -> Any:
        actual_model: Any = base64_to_obj(self.model)
        return getattr(actual_model, self.method_name)(data_input)

    def to_archive(
            self,
            directory: Path,
            metadata_file_name: Text = MODEL_CONFIG_FILE_NAME,
            pickle_file_name: Text = MODEL_PICKLE_FILE_NAME,
            zip_file_name: Text = MODEL_ARCHIVE_NAME
    ) -> Path:
        logger: Logger = logging.getLogger(__name__)

        directory.mkdir(parents=True, exist_ok=True)
        zipfile_path: Path = directory.joinpath(zip_file_name)

        model: bytes = base64.b64decode(self.model)
        conf_encoded: bytes = self.json(exclude={'model'}).encode(encoding='utf8')

        with ZipFile(str(zipfile_path), 'w') as zipFile:
            zipFile.writestr(zinfo_or_arcname=pickle_file_name, data=model)
            zipFile.writestr(zinfo_or_arcname=metadata_file_name, data=conf_encoded)

        logger.info('Added model archive: {archive}'.format(archive=zipfile_path))

        return zipfile_path

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
            model=obj_to_base64(model),
            **conf
        )

    @staticmethod
    def from_archive(
            archive: bytes,
            model_file_name: Text = MODEL_PICKLE_FILE_NAME,
            conf_file_name: Text = MODEL_CONFIG_FILE_NAME
    ) -> Model:
        with ZipFile(BytesIO(archive)) as zp:
            model_pkl: bytes = zp.read(name=model_file_name)
            conf: Dict = json.loads(zp.read(name=conf_file_name).decode(encoding='utf8'))

        return Model(
            model=obj_to_base64(pickle.loads(model_pkl)),
            **conf
        )

    def get_meta_model(self) -> MLSchema:
        return MLSchema(**self.dict())
