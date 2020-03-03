#!/usr/bin/env python3
import json
import logging
import pickle
from logging import Logger
from operator import getitem, itemgetter
from pathlib import Path
from typing import Mapping, Text, Optional, Sequence, Any, Dict

from pandas import DataFrame

from .util import rmdir

MODEL_CONFIG_FILE_NAME: Text = 'conf.json'


class MLModel:
    def __init__(
            self: 'MLModel',
            model: Any,
            name: Text,
            version: Text,
            method_name: Text,
            input_schema: Sequence[Mapping[Text, Any]],
            output_schema: Optional[Mapping[Text, Any]],
            metadata: Mapping[Text, Any]
    ) -> None:
        self.model: Any = model
        self.name: Text = name
        self.version: Text = version
        self.method_name: Text = method_name
        self.input_schema: Sequence[Mapping[Text, Any]] = input_schema
        self.output_schema: Optional[Mapping[Text, Any]] = output_schema
        self.metadata: Mapping[Text, Any] = metadata

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
            reindex(columns=[getitem(item, 'name') for item in sorted(self.input_schema, key=itemgetter('order'))]). \
            astype(
            {
                getitem(item, 'name'): getitem(item, 'type') for item in self.input_schema
            }
        )
        return self.invoke(data)

    def invoke(
            self: 'MLModel',
            data_input: DataFrame
    ) -> Any:
        return getattr(self.model, self.method_name)(data_input)

    @staticmethod
    def load_from_disk(
            storage_root: Path,
            model_name: Text,
            model_version: Text
    ) -> 'MLModel':
        logger: Logger = logging.getLogger(__name__)
        model_dir: Path = storage_root.joinpath(model_name).joinpath(model_version)

        with model_dir.joinpath(
                '{model_name}.{extension}'.format(
                    model_name=model_name, extension='pkl'
                )
        ).open(mode='rb') as model_file:
            model: Any = pickle.load(model_file)

        with model_dir.joinpath(MODEL_CONFIG_FILE_NAME).open() as model_config_file:
            model_config: Mapping[Text, Any] = json.load(model_config_file)

        logger.info('Loaded model from: {storage_root}/{model_name}/{model_version}'.format(
            storage_root=storage_root, model_name=model_name, model_version=model_version))

        return MLModel(
            model=model,
            name=model_name,
            version=model_version,
            method_name=model_config['method_name'],
            input_schema=model_config['input_schema'],
            output_schema=model_config['output_schema'],
            metadata=model_config['model_metadata']
        )

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

        with model_dir.joinpath('{model_name}.{extension}'.format(
                model_name=self.name, extension='pkl')).open(mode='wb') as model_file:
            pickle.dump(obj=self.model, file=model_file, fix_imports=False)

        with model_dir.joinpath(MODEL_CONFIG_FILE_NAME).open(mode='w') as model_config_file:
            json.dump(
                fp=model_config_file,
                obj={'method_name': self.method_name,
                     'input_schema': self.input_schema,
                     'output_schema': self.output_schema,
                     'model_metadata': self.metadata}
            )
        logger.info('Storied model to: {storage_root}/{model_name}/{model_version}'.format(
            storage_root=storage_root, model_name=self.name, model_version=self.version))
