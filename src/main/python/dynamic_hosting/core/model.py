#!/usr/bin/env python3

from __future__ import annotations

import base64
import json
import logging
import pickle
from datetime import datetime
from enum import Enum
from io import BytesIO
from logging import Logger
from pathlib import Path
from typing import Mapping, Text, Optional, Sequence, Any, Dict, Type, OrderedDict, NoReturn, List
from zipfile import ZipFile

from dynamic_hosting.core.feature import Feature
from dynamic_hosting.core.util import rmdir, base64_to_obj, obj_to_base64
from pandas import DataFrame
from pydantic import BaseModel, Field

MODEL_PICKLE_FILE_NAME: Text = 'archive.pkl'
MODEL_ARCHIVE_NAME: Text = 'archive.zip'
MODEL_CONFIG_FILE_NAME: Text = 'conf.json'


class MLType(str, Enum):
    classification: Text = 'CLASSIFICATION'
    regression: Text = 'REGRESSION'
    predict_proba: Text = 'PREDICT_PROBA'


class Metric(BaseModel):
    name: Text = Field(..., description='Name of metric')
    value: Text = Field(..., description='Value of metric')


class Metadata(BaseModel):
    description: Text = Field(..., description='Description of model')
    author: Text = Field(..., description='Author of model')
    trained_at: str = Field(..., description='Training date')
    metrics: List[Metric] = Field(..., description='Metrics for model')


class MetaMLModel(BaseModel):
    """Model independent information"""
    name: Text = Field(..., description='Name of model')
    version: Text = Field(..., description='Version of model')
    method_name: Text = Field(..., description='Name of method. (e.g predict, predict_proba)')
    type: MLType = Field(..., description='Output type of ml model')
    input_schema: Sequence[Feature] = Field(..., description='Input schema of ml model')
    output_schema: Optional[Mapping[Text, Any]] = Field(..., description='Output schema of ml model')
    metadata: Metadata = Field(..., description='Additional information for ml model')


class Model(MetaMLModel):
    """Internal representation of ML model"""
    model: Text = Field(..., description='Pickled model in base64 format')

    def get_ordered_column_name_vec(self) -> Sequence[Text]:
        return [item.get_name() for item in sorted(self.input_schema, key=lambda e: getattr(e, 'order'))]

    def get_feat_type_map(self) -> Mapping[Text, Type]:
        return {item.get_name(): item.get_type() for item in self.input_schema}

    def to_dataframe_compatible(self, kv_pair: OrderedDict[Text: Any]) -> Dict:
        data_frame_compatible_dict: Dict = dict()
        feature_map = self.get_feat_type_map()
        for key, val in kv_pair.items():
            if key in feature_map.keys():
                data_frame_compatible_dict[key] = [val]
        return data_frame_compatible_dict

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
        return getattr(base64_to_obj(self.model), self.method_name)(data_input)

    def get_model_attr(self, attr: Text) -> Any:
        model: Any = base64_to_obj(self.model)
        if hasattr(model, attr):
            return getattr(model, attr)
        else:
            TypeError('model dose not have attribute {att}'.format(att=attr))

    @staticmethod
    def load_from_disk(
            storage_root: Path,
            model_name: Text,
            model_version: Text
    ) -> Model:
        logger: Logger = logging.getLogger(__name__)
        model_dir: Path = storage_root.joinpath(model_name).joinpath(model_version)

        with model_dir.joinpath(MODEL_CONFIG_FILE_NAME).open() as model_config_file:
            model_config: Mapping[Text, Any] = json.load(model_config_file)

            logger.info('Loaded model from: {storage_root}/{model_name}/{model_version}'.format(
                storage_root=storage_root, model_name=model_name, model_version=model_version))
            model: 'Model' = Model(**model_config)
            return model

    @staticmethod
    def remove_from_disk(
            storage_root: Path,
            model_name: Text,
            model_version: Text = None
    ) -> None:
        logger: Logger = logging.getLogger(__name__)
        if model_version:
            logger.info(
                'Deleting model: name <{model_name}> version <{model_version}>'.format(
                    model_name=model_name,
                    model_version=model_version
                )
            )
            rmdir(storage_root.joinpath(model_name).joinpath(model_version))
        else:
            logger.info(
                'Deleting model: name <{model_name}> for all versions'.format(
                    model_name=model_name
                )
            )
            rmdir(storage_root.joinpath(model_name))

    def save_to_disk(
            self,
            storage_root: Path
    ) -> None:
        logger: Logger = logging.getLogger(__name__)

        model_dir: Path = storage_root.joinpath(self.name).joinpath(self.version)
        model_dir.mkdir(parents=True, exist_ok=True)

        # standard json library can not handle timestamp
        with model_dir.joinpath(MODEL_CONFIG_FILE_NAME).open(mode='w') as model_config_file:
            json.dump(
                fp=model_config_file,
                obj=json.loads(self.json())
            )

        logger.info('Storied model to: {storage_root}/{model_name}/{model_version}'.format(
            storage_root=storage_root, model_name=self.name, model_version=self.version))

    def to_archive(
            self,
            directory: Path,
            metadata_file_name: Text = MODEL_CONFIG_FILE_NAME,
            pickle_file_name: Text = MODEL_PICKLE_FILE_NAME,
            zip_file_name: Text = MODEL_ARCHIVE_NAME
    ) -> NoReturn:

        logger: Logger = logging.getLogger(__name__)

        directory.mkdir(parents=True, exist_ok=True)
        zipfile_path: Path = directory.joinpath(zip_file_name)

        model: bytes = base64.b64decode(self.model)
        conf_encoded: bytes = self.json(exclude={'model'}).encode(encoding='utf8')

        with ZipFile(str(zipfile_path), 'w') as zipFile:
            zipFile.writestr(zinfo_or_arcname=pickle_file_name, data=model)
            zipFile.writestr(zinfo_or_arcname=metadata_file_name, data=conf_encoded)

        logger.info('Added model archive: {archive}'.format(archive=zipfile_path))

    @staticmethod
    def from_archive(
            archive: bytes,
            model_file_name: Text = MODEL_PICKLE_FILE_NAME,
            conf_file_name: Text = MODEL_CONFIG_FILE_NAME
    ) -> Model:
        zp: ZipFile = ZipFile(BytesIO(archive))

        model_pkl: bytes = zp.read(name=model_file_name)

        model: Any = pickle.loads(model_pkl)
        conf: Dict = json.loads(zp.read(name=conf_file_name).decode(encoding='utf8'))

        return Model(
            model=obj_to_base64(model),
            **conf
        )

    def get_meta_model(self):
        return MetaMLModel(**self.dict())
