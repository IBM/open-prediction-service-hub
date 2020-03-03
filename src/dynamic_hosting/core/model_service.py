#!/usr/bin/env python3
import logging
from pathlib import Path
from typing import Mapping, Text, Any

from pandas import DataFrame

from .model import MLModel


class ModelService:
    def __init__(
            self,
            ml_models: Mapping[Text, Mapping[Text, MLModel]],
            storage_root: Path
    ):
        self.ml_models: Mapping[Text, Mapping[Text, MLModel]] = ml_models
        self.storage_root: Path = storage_root

    def invoke(
            self,
            model_name: Text,
            model_version: Text,
            data: DataFrame
    ) -> Any:
        logger = logging.getLogger(__name__)
        logger.debug('Invoke ml model <{name}> version <{version}>'.format(name=model_name, version=model_version))

        if not self.ml_models.get(model_name):
            raise RuntimeError('Model <{name}> not found'.format(name=model_name))
        if not self.ml_models[model_name].get(model_version):
            raise RuntimeError('Model <{name}> version  <{version}> not found'.format(
                name=model_name,
                version=model_version)
            )

        return self.ml_models[model_name][model_version].invoke(data_input=data)

    def add_model(
            self, model: MLModel
    ) -> None:
        model.save_to_disk(self.storage_root)
        self.reload_models()

    def remove_model(
            self,
            model_name: Text,
            model_version: Text = None
    ) -> None:
        MLModel.remove_from_disk(
            storage_root=self.storage_root,
            model_name=model_name,
            model_version=model_version
        )
        self.reload_models()

    def reload_models(self) -> None:
        self.ml_models = ModelService.__load_models_from_disk(self.storage_root)

    @staticmethod
    def load_from_disk(
            storage_root: Path
    ) -> 'ModelService':
        logger = logging.getLogger(__name__)
        logger.info('Loading ML service from storage root: {storage_root}'.format(storage_root=storage_root))

        return ModelService(
            ml_models=ModelService.__load_models_from_disk(storage_root=storage_root),
            storage_root=storage_root
        )

    @staticmethod
    def __load_models_from_disk(
            storage_root: Path
    ) -> Mapping[Text, Mapping[Text, MLModel]]:
        return {
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
