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
import sklearn.datasets as skl_datasets
import sklearn.model_selection as skl_model_selection
import sklearn.pipeline as skl_pipeline
import sklearn.preprocessing as skl_preprocessing
import sklearn.svm as skl_svm


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logger = logging.getLogger(__name__)

    col_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'target']

    data = pd.DataFrame(
        data=np.c_[skl_datasets.load_iris()['data'], skl_datasets.load_iris()['target']],
        columns=col_names
    ).replace(
        [np.inf, -np.inf],
        np.nan
    ).dropna().replace(
        {
            'target': {
                i: val for i, val in enumerate(skl_datasets.load_iris().target_names)
            }
        }
    )

    train, test = skl_model_selection.train_test_split(data, random_state=7)

    logger.info(f'Training size: {len(train)}')
    logger.info(f'Validation size: {len(test)}')

    steps = [('scale', skl_preprocessing.StandardScaler()),
             ('model', skl_svm.SVC(random_state=42))]
    pipeline = skl_pipeline.Pipeline(steps)

    x_train = train.loc[:, col_names[:-1]]
    y_train = train.loc[:, col_names[-1]]

    parameter_estimator = skl_model_selection.RandomizedSearchCV(
        **{
            'estimator': pipeline,
            'cv': 3,
            'verbose': 1,
            'n_jobs': -1,
            'random_state': 7,
            'n_iter': 5000,
            'error_score': 'raise',
            'param_distributions': {
                'model__C': [x for x in np.linspace(1e-5, 1.0, num=1000)],
                'model__tol': [x for x in np.linspace(1e-5, 1.0, num=1000)],
                'model__kernel': ['linear', 'poly', 'rbf', 'sigmoid', 'rbf']
            }
        }
    )

    parameter_estimator.fit(x_train, y_train)
    best_estimator = parameter_estimator.best_estimator_

    acc = best_estimator.score(test.loc[:, col_names[:-1]],
                               test.loc[:, col_names[-1]])
    logger.info(f'Accuracy: {acc}')

    with Path(__file__).resolve().parent.joinpath('model.pkl').open(mode='wb') as fd:
        pickle.dump(
            obj=best_estimator,
            file=fd
        )


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    main()
