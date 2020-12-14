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

    logger.info(f'Training size: {len(y_train)}')
    logger.info(f'Validation size: {len(y_test)}')

    # parameter_estimator = model_selection.RandomizedSearchCV(
    #     **{
    #         'estimator': xgboost.XGBClassifier(random_state=42),
    #         'cv': 3,
    #         'verbose': 1,
    #         'n_jobs': -1,
    #         'random_state': 7,
    #         'n_iter': 1000,
    #         'error_score': 'raise',
    #         'param_distributions': {
    #             'colsample_bytree': [x for x in np.linspace(1E-4, 1.0, num=100)],
    #             'learning_rate': [x for x in np.linspace(1E-4, 1.0, num=100)],
    #             'max_depth': [int(x) for x in np.linspace(2, 20, num=10)]
    #         }
    #     }
    # )
    # parameter_estimator.fit(x_train, y_train)
    # logger.info(f'Best parameters: {parameter_estimator.best_params_}')
    # estimator = parameter_estimator.best_estimator_

    # Uncomment lines above to activate HPO
    estimator = xgboost.XGBClassifier(
        max_depth=6,
        learning_rate=0.6667,
        colsample_bytree=0.8686999999999999
    )

    estimator.fit(x_train, y_train)

    logger.info(f'Accuracy: {estimator.score(x_test, y_test)}')

    estimator.save_model(fname=FILE_PATH.parent.joinpath('model.bst').__str__())


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    main()
