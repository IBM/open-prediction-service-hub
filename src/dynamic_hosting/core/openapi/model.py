#!/usr/bin/env python3
from __future__ import annotations

import json
import logging
from logging import Logger
from pathlib import Path
from typing import Mapping, Text, Optional, Sequence, Any, Dict, Type, OrderedDict

import numpy as np
from dynamic_hosting.core.openapi.request import RequestMetadata, BaseRequestBody
from dynamic_hosting.core.util import rmdir, base64_to_obj
from fastapi.utils import get_model_definitions
from pandas import DataFrame
from pydantic import BaseModel, create_model

MODEL_CONFIG_FILE_NAME: Text = 'conf.json'


class ResponseBody(BaseModel):
    model_output: Any
    model_output_raw: Text


class Feature(BaseModel):
    name: Text
    order: int
    type: Text


class Model(BaseModel):
    model: Text  # pickled model in base64
    name: Text
    version: Text
    method_name: Text
    input_schema: Sequence[Feature]
    output_schema: Optional[Mapping[Text, Any]]
    metadata: Mapping

    def input_schema_model(self) -> Type[BaseModel]:
        fields_dict = {
            name: (t, ...)
            for name, t in self.get_feat_type_map().items()
        }
        return create_model(
            '{model_name}-{model_version}'.format(
                model_name=self.name,
                model_version=self.version
            ),
            **fields_dict,
            __base__=BaseModel
        )

    def input_schema_definition(self) -> Dict[Text, Any]:
        model: Type[BaseModel] = self.input_schema_model()
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

    # TODO: Add better type casting
    def get_feat_type_map(self) -> Mapping[Text, Type]:
        m: Dict[Text, Type] = {}
        for item in self.input_schema:
            if np.issubdtype(np.dtype(getattr(item, 'type')), np.number):
                m[getattr(item, 'name')] = np.float64
            else:
                m[getattr(item, 'name')] = np.unicode
        return m

    def transform_internal_dict(self, kv_pair: OrderedDict[Text: Any]) -> Dict:
        data_frame_compatible_dict: Dict = dict()
        feature_map = self.get_feat_type_map()
        for key, val in kv_pair.items():
            if key in feature_map.keys():
                data_frame_compatible_dict[key] = [val]
        return data_frame_compatible_dict

    def invoke_from_dict(
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
        return self.invoke(data)

    def invoke(
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
