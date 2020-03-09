#!/usr/bin/env python3
import logging
from pathlib import Path
from typing import Mapping, Text, Any, Sequence, Dict

from pandas import DataFrame
from pydantic import BaseModel

from .model import Model


class ModelService(BaseModel):
    ml_models: Sequence[Model]
    storage_root: Path

    def invoke_from_dict(
            self,
            model_name: Text,
            model_version: Text,
            data: Dict
    ) -> Any:
        logger = logging.getLogger(__name__)
        logger.debug('Invoke ml model <{name}> version <{version}>'.format(name=model_name, version=model_version))

        model_map: Mapping[Text, Mapping[Text, Model]] = self.model_map()

        if not model_map.get(model_name):
            raise RuntimeError('Model <{name}> not found'.format(name=model_name))
        if not model_map[model_name].get(model_version):
            raise RuntimeError('Model <{name}> version  <{version}> not found'.format(
                name=model_name,
                version=model_version)
            )

        return model_map[model_name][model_version].invoke_from_dict(data_input=data)


    def invoke(
            self,
            model_name: Text,
            model_version: Text,
            data: DataFrame
    ) -> Any:
        logger = logging.getLogger(__name__)
        logger.debug('Invoke ml model <{name}> version <{version}>'.format(name=model_name, version=model_version))

        model_map: Mapping[Text, Mapping[Text, Model]] = self.model_map()

        if not model_map.get(model_name):
            raise RuntimeError('Model <{name}> not found'.format(name=model_name))
        if not model_map[model_name].get(model_version):
            raise RuntimeError('Model <{name}> version  <{version}> not found'.format(
                name=model_name,
                version=model_version)
            )

        return model_map[model_name][model_version].invoke(data_input=data)

    def add_model(
            self, model: Model
    ) -> None:
        model.save_to_disk(self.storage_root)
        self.reload_models()

    def remove_model(
            self,
            model_name: Text,
            model_version: Text = None
    ) -> None:
        Model.remove_from_disk(
            storage_root=self.storage_root,
            model_name=model_name,
            model_version=model_version
        )
        self.reload_models()

    def reload_models(self) -> None:
        self.ml_models = ModelService._load_models_from_disk(self.storage_root)

    @staticmethod
    def load_from_disk(
            storage_root: Path
    ) -> 'ModelService':
        logger = logging.getLogger(__name__)
        logger.info('Loading ML service from storage root: {storage_root}'.format(storage_root=storage_root))

        return ModelService(
            ml_models=ModelService._load_models_from_disk(storage_root=storage_root),
            storage_root=storage_root
        )

    @staticmethod
    def _load_models_from_disk(
            storage_root: Path
    ) -> Sequence[Model]:
        return [
            Model.load_from_disk(
                storage_root=storage_root,
                model_name=model_abspath.name,
                model_version=versioned_model_abspath.name)

            for model_abspath in storage_root.iterdir()
            if model_abspath.is_dir()
            for versioned_model_abspath in model_abspath.iterdir()
            if versioned_model_abspath.is_dir()
        ]

    def model_map(self) -> Mapping[Text, Mapping[Text, Model]]:
        return {
            model.name: {
                model.version: model
            }
            for model in self.ml_models
        }
