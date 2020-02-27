#!/usr/bin/env python3
import json
import pickle
from typing import Mapping, Text, Optional, Sequence, Any
from pathlib import Path
from pandas import DataFrame
from os import path

MODEL_CONFIG_FILE_NAME: Text = 'conf.json'


class Model:
    def __init__(
            self,
            model: Any,
            name: Text,
            version: Text,
            method_name: Text,
            input_schema: Sequence[Mapping[Text, Any]],
            output_schema: Optional[Mapping[Text, Any]],
            metadata: Mapping[Text, Any]
    ):
        self.model: Any = model
        self.name: Text = name
        self.version: Text = version
        self.method_name: Text = method_name
        self.input_schema: Sequence[Mapping[Text, Any]] = input_schema
        self.output_schema: Optional[Mapping[Text, Any]] = output_schema
        self.metadata: Mapping[Text, Any] = metadata

    def invoke(self, data_input: DataFrame) -> Any:
        return getattr(self.model, self.method_name)(data_input)

    @staticmethod
    def load_from_disk(storage_root: Path, model_name: Text, model_version: Text) -> 'Model':
        model_dir: Path = storage_root.joinpath(model_name).joinpath(model_version)

        with model_dir.joinpath('{model_name}{extension}'.format(
                model_name=model_name, extension='pkl')).open(mode='rb') as model_file:
            model = pickle.load(model_file)
        with model_dir.joinpath(MODEL_CONFIG_FILE_NAME).open() as model_config_file:
            model_config = json.load(model_config_file)
            method_name = model_config['method_name']
            input_schema = model_config['input_schema']
            output_schema = model_config['output_schema']
            model_metadata = model_config['model_metadata']

        return Model(
            model=model,
            name=model_name,
            version=model_version,
            method_name=method_name,
            input_schema=input_schema,
            output_schema=output_schema,
            metadata=model_metadata
        )

    def save_to_disk(self, storage_root: Path):
        model_dir: Path = storage_root.joinpath(self.name).joinpath(self.version)
        model_dir.mkdir(parents=True, exist_ok=True)

        with model_dir.joinpath('{model_name}{extension}'.format(
                model_name=self.name, extension='pkl')).open(mode='wb') as model_file:
            pickle.dump(model_file, self.model, fix_imports=False)

        with model_dir.joinpath(MODEL_CONFIG_FILE_NAME).open(mode='w') as model_config_file:
            json.dump(
                fp=model_config_file,
                obj={'method_name': self.method_name,
                     'input_schema': self.input_schema,
                     'output_schema': self.output_schema,
                     'model_metadata': self.metadata}
            )


if __name__ == '__main__':
    model_path = Path(path.abspath(__file__)).parent.parent.joinpath('models').joinpath('miniloandefault-svc.pkl')
    with model_path.open(mode='rb') as f:
        model_cache = pickle.load(f)
    test_model = Model(
        name='miniloandefault-svc',
        version='v1',
        model=model_cache,
        method_name='predict',
        input_schema=[
            {
                'name': "creditScore",
                'order': 0,
                'type': 'float'
            },
            {
                'name': "income",
                'order': 1,
                'type': 'float'
            },
            {
                'name': "loanAmount",
                'order': 2,
                'type': 'float'
            },
            {
                'name': "monthDuration",
                'order': 3,
                'type': 'float'
            },
            {
                'name': "rate",
                'order': 4,
                'type': 'float'
            },
            {
                'name': "yearlyReimbursement",
                'order': 5,
                'type': 'float'
            }
        ],
        output_schema=None,
        metadata={
            'name': 'loan payment default classification',
            'author': 'Pierre Feillet',
            'date': '2020-01-28T15:45:00CEST',
            'metrics': {
                'accuracy': 0.5
            }
        }
    )
    input_data = DataFrame(
        columns=['creditScore', 'income', 'loanAmount', 'monthDuration', 'rate', 'yearlyReimbursement'],
        data=[[397, 5000, 570189, 240, 0.07, 57195]]
    )
    print(input_data)
    res = test_model.invoke(
        data_input=input_data
    )
    print(res)
