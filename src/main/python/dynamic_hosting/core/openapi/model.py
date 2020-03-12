#!/usr/bin/env python3

from __future__ import annotations

import json
import logging
from logging import Logger
from pathlib import Path
from typing import Mapping, Text, Optional, Sequence, Any, Dict, Type, OrderedDict

import numpy as np
from dynamic_hosting.core.openapi.request import RequestMetadata
from dynamic_hosting.core.util import rmdir, base64_to_obj
from fastapi.utils import get_model_definitions
from pandas import DataFrame
from pydantic import BaseModel, create_model, Field, validator

MODEL_CONFIG_FILE_NAME: Text = 'conf.json'


class ResponseBody(BaseModel):
    """Ml output configuration"""
    model_output: Optional[Any] = Field(
        None,
        description='Structured model output. Its format is parameterized by output schema'
    )
    model_output_raw: Text = Field(..., description='String representation of output')


class Feature(BaseModel):
    """Ml input element"""
    name: Text = Field(..., description='Feature name')
    order: int = Field(..., description='Position of feature')
    type: Text = Field(..., description='Numpy type of feature')

    @classmethod
    @validator('type')
    def name_must_contain_space(cls, t):
        if not getattr(np, t):
            raise ValueError('must contain a space')
        return t


class InputSchema(BaseModel):
    pass


class Model(BaseModel):
    """Internal representation of ML model"""
    model: Text = Field(..., description='Pickled model in base64 format')
    name: Text = Field(..., description='Name of model')
    version: Text = Field(..., description='Version of model')
    method_name: Text = Field(..., description='Name of method. (e.g predict, predict_proba)')
    input_schema: Sequence[Feature] = Field(..., description='Input schema of ml model')
    output_schema: Optional[Mapping[Text, Any]] = Field(..., description='Output schema of ml model')
    metadata: Mapping[Text, Any] = Field(..., description='Additional information for ml model')

    # TODO: Add better type casting for openapi schema
    def input_schema_t(self) -> Type[BaseModel]:
        fields_dict: Dict[Text, Any] = dict()

        for feature_name, numpy_type in self.get_feat_type_map().items():
            fields_dict[feature_name] = (numpy_type, ...)

        return create_model(
            '{model_name}-{model_version}'.format(
                model_name=self.name,
                model_version=self.version
            ),
            **fields_dict,
            __base__=InputSchema
        )

    def input_schema_definition(self) -> Dict[Text, Any]:
        model: Type[BaseModel] = self.input_schema_t()
        return get_model_definitions(
            flat_models={model},
            model_name_map={
                model: '{model_name}-{model_version}'.format(
                    model_name=self.name,
                    model_version=self.version
                ),
                RequestMetadata: 'RequestMetadata'
            }
        )

    def get_ordered_column_name_vec(self) -> Sequence[Text]:
        return [getattr(item, 'name') for item in sorted(self.input_schema, key=lambda e: getattr(e, 'order'))]

    def get_feat_type_map(self) -> Mapping[Text, np.dtype]:
        return {getattr(item, 'name'): getattr(np, getattr(item, 'type')) for item in self.input_schema}

    def transform_internal_dict(self, kv_pair: OrderedDict[Text: Any]) -> Dict:
        data_frame_compatible_dict: Dict = dict()
        feature_map = self.get_feat_type_map()
        for key, val in kv_pair.items():
            if key in feature_map.keys():
                data_frame_compatible_dict[key] = [val]
        return data_frame_compatible_dict

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
            dtype=self.get_feat_type_map()
        )
        return self.__invoke__(data)

    def __invoke__(
            self,
            data_input: DataFrame
    ) -> Any:
        return getattr(base64_to_obj(self.model), self.method_name)(data_input)

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

        with model_dir.joinpath(MODEL_CONFIG_FILE_NAME).open(mode='w') as model_config_file:
            json.dump(
                fp=model_config_file,
                obj=self.dict()
            )

        logger.info('Storied model to: {storage_root}/{model_name}/{model_version}'.format(
            storage_root=storage_root, model_name=self.name, model_version=self.version))
