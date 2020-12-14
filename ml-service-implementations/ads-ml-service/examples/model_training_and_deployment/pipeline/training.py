#!/usr/bin/env python3
#
# Copyright 2020 IBM
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.IBM Confidential
#


import logging
import pathlib
import pickle
import sys
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn.compose as skl_compose
import sklearn.ensemble as skl_ensemble
import sklearn.impute as skl_impute
import sklearn.pipeline as skl_pipeline
import sklearn.preprocessing as skl_preprocessing

UCI_REPO = 'http://archive.ics.uci.edu/ml/machine-learning-databases/adult'

DATA_NAME = 'adult.data'
TEST_NAME = 'adult.test'


def download():
    if not pathlib.Path(__file__).resolve().parent.joinpath(DATA_NAME).is_file():
        urllib.request.urlretrieve(f'{UCI_REPO}/{DATA_NAME}', DATA_NAME)
    if not pathlib.Path(__file__).resolve().parent.joinpath(TEST_NAME).is_file():
        urllib.request.urlretrieve(f'{UCI_REPO}/{TEST_NAME}', TEST_NAME)


def train():
    features = {
        'age': np.float,
        'workclass': str,
        'fnlwgt': np.float,
        'education': str,
        'education-num': np.float,
        'marital-status': str,
        'occupation': str,
        'relationship': str,
        'race': str,
        'sex': str,
        'capital-gain': np.float,
        'capital-loss': np.float,
        'hours-per-week': np.float,
        'native-country': str,
        'label': str
    }

    names = [*features]

    x_labels = names[:-1]
    y_label = names[-1]

    download()

    categorical_features = [name for name in x_labels if features[name] is str]
    numeric_features = [name for name in x_labels if name not in categorical_features]

    categorical_transformer = skl_pipeline.Pipeline(steps=[
        ('imputation', skl_impute.SimpleImputer(strategy='constant', fill_value='missing')),
        ('one_hot_encode', skl_preprocessing.OneHotEncoder(handle_unknown='ignore'))])
    numeric_transformer = skl_pipeline.Pipeline(
        steps=[
            ('imputation', skl_impute.SimpleImputer(strategy='mean'))
        ]
    )

    preprocessor = skl_compose.ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)]
    )

    data_train_path = Path(__file__).resolve().parent.joinpath(DATA_NAME)
    data_validation_path = Path(__file__).resolve().parent.joinpath(TEST_NAME)

    data_train = pd.read_csv(
        data_train_path,
        delimiter=r'\s*,\s*',
        engine='python',
        names=names,
        dtype=features,
        header=None
    ).replace(
        [np.inf, -np.inf], np.nan
    ).dropna()
    data_validation = pd.read_csv(
        data_validation_path,
        delimiter=r'\s*,\s*',
        engine='python',
        names=names,
        dtype=features,
        header=None,
        skiprows=[0]
    ).replace(
        [np.inf, -np.inf], np.nan
    ).dropna().replace(
        {
            'label': {
                '<=50K.': '<=50K',
                '>50K.': '>50K'
            }
        }
    )

    x_train = data_train.loc[:, x_labels]
    y_train = data_train.loc[:, y_label]
    x_validation = data_validation.loc[:, x_labels]
    y_validation = data_validation.loc[:, y_label]

    logger.info(f'Training size: {len(data_train)}')
    logger.info(f'Validation size: {len(data_validation)}')

    estimator = skl_pipeline.Pipeline(
        steps=[
            ('preprocessor', preprocessor),
            ('classifier', skl_ensemble.RandomForestClassifier(random_state=42))
        ]
    )
    estimator.fit(x_train, y_train)

    acc = estimator.score(x_validation, y_validation)
    logger.info(f'Accuracy: {acc}')

    with Path(__file__).resolve().parent.joinpath('model.pkl').open(mode='wb') as fd:
        pickle.dump(
            obj=estimator,
            file=fd
        )


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logger = logging.getLogger(__name__)
    train()
