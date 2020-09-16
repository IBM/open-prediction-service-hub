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
import sys

import numpy as np
import pandas as pd
import sklearn.model_selection as model_selection
import xgboost

logger = logging.getLogger(__name__)
FILE_PATH = pathlib.Path(__file__).resolve()


def main():
    names = ['name', 'creditScore', 'income', 'loanAmount', 'monthDuration', 'approval', 'rate', 'yearlyReimbursement']
    used_names = ['creditScore', 'income', 'loanAmount', 'monthDuration', 'rate', 'approval']

    miniloan_file = FILE_PATH.parents[3].joinpath('data').joinpath(
        'miniloan-decisions-ls-10K.csv')

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

    x = data.loc[:, used_names[:-1]].to_numpy()
    y = data.loc[:, used_names[-1]].to_numpy()
    x_train, x_test, y_train, y_test = model_selection.train_test_split(x, y, random_state=7)

    logger.info(f'training size: {len(x_test)}')
    logger.info(f'validation size: {len(y_test)}')

    params = {
        'estimator': xgboost.XGBClassifier(random_state=42),
        'cv': 3,
        'verbose': 0,
        'n_jobs': -1,
        'random_state': 21,
        'n_iter': 5e02,
        'scoring': 'accuracy',
        'error_score': 'raise',
        'param_distributions': {
            'colsample_bytree': [x for x in np.linspace(1E-4, 1.0, num=1000)],
            'learning_rate': [x for x in np.linspace(1E-4, 1.0, num=1000)],
            'max_depth': [int(x) for x in np.linspace(3, 20, num=10)],
        },
    }

    parameter_estimator = model_selection.RandomizedSearchCV(**params)

    parameter_estimator.fit(x_train, y_train)
    best_estimator = xgboost.XGBClassifier(
        random_state=42,
        **parameter_estimator.best_params_
    )

    best_estimator.fit(x_train, y_train)

    logger.info(f'accuracy: {best_estimator.score(x_test, y_test)}')

    best_estimator.save_model(fname=FILE_PATH.parent.joinpath('model.bst').__str__())


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    main()
