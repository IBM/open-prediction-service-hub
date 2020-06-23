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
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.svm import LinearSVC


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logger = logging.getLogger(__name__)

    names = ['name', 'creditScore', 'income', 'loanAmount', 'monthDuration', 'approval', 'rate', 'yearlyReimbursement']
    used_names = ['creditScore', 'income', 'loanAmount', 'monthDuration', 'rate', 'approval']

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
        'estimator': LinearSVC(random_state=42, dual=False),
        'cv': 3,
        'verbose': 0,
        'n_jobs': -1,
        'random_state': 21,
        'n_iter': 5e03,
        'scoring': 'accuracy',
        'error_score': 'raise',
        'param_distributions': {
            'penalty': ['l1'],
            'loss': ['squared_hinge'],
            'tol': [x for x in np.linspace(1e-5, 5e-1, num=1000)],
            'C': [x for x in np.linspace(1e-5, 1.0, num=1000)]
        },
    }

    parameter_estimator = RandomizedSearchCV(**params)

    x_train = train.loc[:, used_names[:-1]]
    y_train = train.loc[:, used_names[-1]]

    parameter_estimator.fit(x_train, y_train)
    best_estimator = LinearSVC(
        random_state=42,
        dual=False,
        **parameter_estimator.best_params_
    )

    best_estimator.fit(x_train, y_train)

    acc = best_estimator.score(test.loc[:, used_names[:-1]],
                               test.loc[:, used_names[-1]])
    logger.debug(f'accuracy: {acc}')

    with Path(__file__).resolve().parent.joinpath('miniloan-linear-svc-model.pkl').open(mode='wb') as fd:
        pickle.dump(
            obj=best_estimator,
            file=fd
        )


if __name__ == '__main__':
    main()
