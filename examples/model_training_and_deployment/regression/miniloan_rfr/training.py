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
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, RandomizedSearchCV


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logger = logging.getLogger(__name__)

    names = ['name', 'creditScore', 'income', 'loanAmount', 'monthDuration', 'approval', 'rate', 'yearlyReimbursement']
    used_names = ['creditScore', 'income', 'loanAmount', 'monthDuration', 'rate', 'yearlyReimbursement']

    miniloan_file = Path(__file__).resolve().parents[4].joinpath('data').joinpath('miniloan-decisions-ls-10K.csv')

    data = pd.read_csv(
        miniloan_file,
        header=0,
        delimiter=r'\s*,\s*',
        engine='python',
        names=names,
        dtype={
            'name': np.object,
            'creditScore': np.int64,
            'income': np.float64,
            'loanAmount': np.float64,
            'monthDuration': np.float64,
            'approval': np.object,
            'rate': np.float64,
            'yearlyReimbursement': np.float64
        }
    ).replace(
        [np.inf, -np.inf], np.nan
    ).dropna().loc[:, used_names]

    train, test = train_test_split(data, random_state=7)

    logger.debug(f'training size: {len(train)}')
    logger.debug(f'validation size: {len(test)}')

    params = {
        'estimator': RandomForestRegressor(random_state=0),
        'cv': 3,
        'verbose': 0,
        'n_jobs': -1,
        'error_score': 'raise',
        'random_state': 42,
        'n_iter': 10,
        'param_distributions': {
            'criterion': ['mse'],
            'n_estimators': [int(x) for x in np.linspace(50, 1000, num=20)],
            'min_samples_split': [int(x) for x in np.linspace(2, 64, num=50)],
            'min_samples_leaf': [int(x) for x in np.linspace(1, 32, num=20)]
        }
    }

    parameter_estimator = RandomizedSearchCV(**params)

    x_train = train.loc[:, used_names[:-1]]
    y_train = train.loc[:, used_names[-1]]

    parameter_estimator.fit(x_train, y_train)
    best_estimator = RandomForestRegressor(
        random_state=42,
        **parameter_estimator.best_params_
    )

    best_estimator.fit(x_train, y_train)

    acc = best_estimator.score(test.loc[:, used_names[:-1]],
                               test.loc[:, used_names[-1]])
    logger.debug(f'coefficient of determination R^2: {acc}')

    with Path(__file__).resolve().parent.joinpath('miniloan-rfr-model.pkl').open(mode='wb') as fd:
        pickle.dump(
            obj=best_estimator,
            file=fd
        )


if __name__ == '__main__':
    main()