#!/usr/bin/env python3
import json
import logging

import fastapi

from logging import Logger
from pathlib import Path
from typing import Mapping, Text, Optional, Sequence, Any, Dict, List, Callable

from fastapi.openapi.utils import get_openapi
from pandas import DataFrame
from numpy import dtype
from pydantic import BaseModel

from .util import rmdir, base64_to_obj

MODEL_CONFIG_FILE_NAME: Text = 'conf.json'


class MLParam(BaseModel):
    name: Text = 'Feature name'
    order: int = 0
    value: Any = 'Feature value'


class MLRequest(BaseModel):
    model_name: Text = 'model_name'
    model_version: Text = 'model_version'
    params: List[MLParam] = list()

    @staticmethod
    def params_to_dict(ml_req: 'MLRequest') -> Dict[Text, Sequence]:
        return {
            feat_val.name: [feat_val.value]
            for feat_val in ml_req.params
        }


class MLResponse(BaseModel):
    model_output: Any
    model_output_raw: Text


class Feature(BaseModel):
    name: Text
    order: int
    type: Text


class OpenapiMLModelSchema(BaseModel):
    title: Text
    required: Sequence[Text]
    type: Text = 'object'
    properties: Mapping[Text, Mapping[Text, Any]]

    @staticmethod
    def get_property_map(model: 'MLModel') -> Mapping[Text,  Mapping[Text, Text]]:
        return {
            feat: {
                'title': '{model_name}-{model_version}.{feature_name}'.format(
                    model_name=model.name, model_version=model.version, feature_name=feat),
                'type': str(t)
            }
            for feat, t in model.get_feat_type_map().items()
        }

    @staticmethod
    def from_ml_model(model: 'MLModel') -> 'OpenapiMLModelSchema':

        return OpenapiMLModelSchema(
            title=model.name,
            required=model.get_ordered_column_name_vec(),
            properties=OpenapiMLModelSchema.get_property_map(model)
        )


class MLModel(BaseModel):
    model: Text  # pickled model in base64
    name: Text
    version: Text
    method_name: Text
    input_schema: Sequence[Feature]
    output_schema: Optional[Mapping[Text, Any]]
    metadata: Mapping
    additional_input_schema: Optional[OpenapiMLModelSchema] = None

    def get_ordered_column_name_vec(self) -> Sequence[Text]:
        return [getattr(item, 'name') for item in sorted(self.input_schema, key=lambda e: getattr(e, 'order'))]

    def get_feat_type_map(self) -> Mapping[Text, Text]:
        return {getattr(item, 'name'): dtype(getattr(item, 'type')) for item in self.input_schema}

    def invoke_from_dict(
            self: 'MLModel',
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
        return self.invoke(data)

    def invoke(
            self: 'MLModel',
            data_input: DataFrame
    ) -> Any:
        return getattr(base64_to_obj(self.model), self.method_name)(data_input)

    @staticmethod
    def load_from_disk(
            storage_root: Path,
            model_name: Text,
            model_version: Text
    ) -> 'MLModel':
        logger: Logger = logging.getLogger(__name__)
        model_dir: Path = storage_root.joinpath(model_name).joinpath(model_version)

        with model_dir.joinpath(MODEL_CONFIG_FILE_NAME).open() as model_config_file:
            model_config: Mapping[Text, Any] = json.load(model_config_file)

            logger.info('Loaded model from: {storage_root}/{model_name}/{model_version}'.format(
                storage_root=storage_root, model_name=model_name, model_version=model_version))
            model: 'MLModel' = MLModel(**model_config)
            model.additional_input_schema = OpenapiMLModelSchema.from_ml_model(model)
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
            self: 'MLModel',
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
