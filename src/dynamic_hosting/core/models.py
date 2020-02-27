#!/usr/bin/env python3
from typing import Mapping, Text, Optional, Sequence, Any
from pathlib import Path
from pickle import load
from pandas import DataFrame
from os import path


class Model:
    def __init__(
            self,
            model_path: Path,
            method_name: Text,
            input_schema: Sequence[Mapping[Text, Any]],
            output_schema: Optional[Mapping[Text, Any]],
            metadata: Mapping[Text, Any]
    ):
        self.model_path: Path = model_path
        self.method_name: Text = method_name
        self.input_schema: Sequence[Mapping[Text, Any]] = input_schema
        self.output_schema: Optional[Mapping[Text, Any]] = output_schema
        self.metadata: Mapping[Text, Any] = metadata
        self.model_cache: Any = None

    def invoke(self, input_: DataFrame) -> Any:
        if self.model_cache is None:
            with self.model_path.open(mode='rb') as f:
                self.model_cache = load(f)
        return getattr(self.model_cache, self.method_name)(input_)


if __name__ == '__main__':
    test_model = Model(
        model_path=Path(path.abspath(__file__)).parent.parent.joinpath('models').joinpath('miniloandefault-svc.pkl'),
        method_name='predict',
        input_schema=None,
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
    input_data =DataFrame(
            columns=['creditScore', 'income', 'loanAmount', 'monthDuration', 'rate', 'yearlyReimbursement'],
            data=[[397, 5000, 570189, 240, 0.07, 57195]]
        )
    print(input_data)
    res = test_model.invoke(
        input_=input_data
    )
    print(res)
