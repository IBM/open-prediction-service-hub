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


import json
import logging
import pickle
import sys
import pathlib

import numpy as np
import pandas as pd
import sklearn.model_selection as model_selection
import sklearn.ensemble as skl_ensemble


def main():
    names = ['name', 'creditScore', 'income', 'loanAmount', 'monthDuration', 'approval', 'rate', 'yearlyReimbursement']
    used_names = ['creditScore', 'income', 'loanAmount', 'monthDuration', 'rate', 'approval']

    miniloan_file = pathlib.Path(__file__).resolve().parents[3].joinpath('data').joinpath('miniloan-decisions-ls-10K.csv')

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

    train, test = model_selection.train_test_split(data, random_state=7)

    logger.info(f'Training size: {len(train)}')
    logger.info(f'Validation size: {len(test)}')

    x_train = train.loc[:, used_names[:-1]]
    y_train = train.loc[:, used_names[-1]]

    # parameter_estimator = model_selection.RandomizedSearchCV(
    #     **{
    #         'estimator': skl_ensemble.RandomForestClassifier(random_state=42),
    #         'cv': 3,
    #         'verbose': 1,
    #         'n_jobs': -1,
    #         'random_state': 7,
    #         'n_iter': 1000,
    #         'error_score': 'raise',
    #         'param_distributions': {
    #             'criterion': ['gini'],
    #             'n_estimators': [int(x) for x in np.linspace(50, 1000, num=20)],
    #             'min_samples_split': [int(x) for x in np.linspace(2, 64, num=50)],
    #             'min_samples_leaf': [int(x) for x in np.linspace(1, 32, num=20)]
    #         }
    #     }
    # )
    # parameter_estimator.fit(x_train, y_train)
    # logger.info(f'Best parameters: {parameter_estimator.best_params_}')
    # estimator = parameter_estimator.best_estimator_

    # Uncomment lines above to activate HPO
    estimator = skl_ensemble.RandomForestClassifier(
        random_state=42,
        n_estimators=650,
        min_samples_split=2,
        min_samples_leaf=1
    )

    estimator.fit(x_train, y_train)

    acc = estimator.score(test.loc[:, used_names[:-1]],
                          test.loc[:, used_names[-1]])
    logger.info(f'Accuracy: {acc}')

    with pathlib.Path(__file__).resolve().parent.joinpath('model.pkl').open(mode='wb') as fd:
        pickle.dump(
            obj=estimator,
            file=fd
        )

    with pathlib.Path(__file__).resolve().parent.joinpath('deployment_conf.json').open(mode='r') as fd:
        configs = json.load(fd)
    class_names = estimator.classes_.tolist()
    configs['model']['metadata']['additional'] = {'names': class_names}
    with pathlib.Path(__file__).resolve().parent.joinpath('deployment_conf.json').open(mode='w') as fd:
        json.dump(configs, fd)


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logger = logging.getLogger(__name__)
    main()
