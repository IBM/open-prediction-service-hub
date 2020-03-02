#!/usr/bin/env python3
import logging

from typing import Mapping, Text, Optional, Sequence, Any, MutableMapping
from pathlib import Path

from pandas import DataFrame

from .model import MLModel


class ModelService:
    def __init__(self, ml_models: Mapping[Text, Mapping[Text, MLModel]]):
        self.ml_models: Mapping[Text, Mapping[Text, MLModel]] = ml_models

    def invoke(self, model_name: Text, model_version: Text, data: DataFrame) -> Any:
        logger = logging.getLogger(__name__)
        logger.info('Invoke ml model <{name}> version <{version}>'.format(name=model_name, version=model_version))

        if not self.ml_models.get(model_name):
            raise RuntimeError('Model <{name}> not found'.format(name=model_name))
        if not self.ml_models[model_name].get(model_version):
            raise RuntimeError('Model <{name}> version  <{version}> not found'.format(
                name=model_name,
                version=model_version)
            )

        return self.ml_models[model_name][model_version].invoke(data_input=data)

    @staticmethod
    def load_from_disk(storage_root: Path) -> 'ModelService':
        logger = logging.getLogger(__name__)
        logger.info('Loading ML service from storage root: {storage_root}'.format(storage_root=storage_root))

        ml_models: Mapping[Text, Mapping[Text, MLModel]] = {
            model_abspath.name:
                {
                    versioned_model_abspath.name:
                        MLModel.load_from_disk(
                            storage_root=storage_root,
                            model_name=model_abspath.name,
                            model_version=versioned_model_abspath.name)
                }
            for model_abspath in storage_root.iterdir()
            if model_abspath.is_dir()
            for versioned_model_abspath in model_abspath.iterdir()
            if versioned_model_abspath.is_dir()
        }

        return ModelService(ml_models)
