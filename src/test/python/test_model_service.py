#!/usr/bin/env python3

import logging
import sys

import pandas as pd
import numpy as np

from dynamic_hosting.core.model_service import ModelService
from pathlib import Path

from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def test():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logger = logging.getLogger(__name__)

    storage_root = Path(__file__).resolve().parents[1].joinpath('example_models')
    test_ml_service = ModelService.load_from_disk(storage_root=storage_root)

    col_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class_name']

    iris = load_iris()

    data = pd.DataFrame(
        data=np.c_[iris['data'], iris['target']],
        columns=col_names
    )

    data = data.replace([np.inf, -np.inf], np.nan).dropna()

    _, test_data = train_test_split(data, random_state=0)

    predicted = test_ml_service.invoke(
        model_name='iris-svc-RandomizedSearchCV',
        model_version='v0',
        data=test_data.loc[:, col_names[:-1]]
    )

    logger.info('accuracy_score of model {score}'.format(score=accuracy_score(test_data.loc[:, col_names[-1]], predicted)))


if __name__ == '__main__':
    test()
