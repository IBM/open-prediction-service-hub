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
import pickle
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.svm import SVC


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logger = logging.getLogger(__name__)

    col_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'target']

    data = pd.DataFrame(
        data=np.c_[load_iris()['data'], load_iris()['target']],
        columns=col_names
    ).replace(
        [np.inf, -np.inf],
        np.nan
    ).dropna().replace(
        {
            'target': {
                i: val for i, val in enumerate(load_iris().target_names)
            }
        }
    )

    print(load_iris().target_names)

    train, test = train_test_split(data, random_state=7)

    logger.info(f'training size: {len(train)}')
    logger.info(f'validation size: {len(test)}')

    params = {
        'estimator': SVC(random_state=42),
        'cv': 3,
        'random_state': 21,
        'n_iter': 5e03,
        'scoring': 'accuracy',
        'error_score': 'raise',
        'param_distributions': {
            'C': [x for x in np.linspace(1e-5, 1.0, num=1000)],
            'tol': [x for x in np.linspace(1e-5, 5e-1, num=1000)],
            'kernel': ['linear', 'poly', 'rbf', 'sigmoid', 'rbf']
        },
        'verbose': bool(__debug__),
        'n_jobs': -1
    }

    parameter_estimator = RandomizedSearchCV(**params)

    x_train = train.loc[:, col_names[:-1]]
    y_train = train.loc[:, col_names[-1]]

    parameter_estimator.fit(x_train, y_train)
    best_estimator = SVC(
        random_state=42,
        **parameter_estimator.best_params_
    )

    best_estimator.fit(x_train, y_train)

    acc = best_estimator.score(test.loc[:, col_names[:-1]],
                               test.loc[:, col_names[-1]])
    logger.info(f'accuracy: {acc}')

    with Path(__file__).resolve().parent.joinpath('iris-model.pkl').open(mode='wb') as fd:
        pickle.dump(
            obj=best_estimator,
            file=fd
        )


if __name__ == '__main__':
    main()
