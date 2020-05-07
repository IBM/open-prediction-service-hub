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
import os
import pickle
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Any

import numpy as np
import pandas as pd
from dynamic_hosting.core.model import Model
from dynamic_hosting.core.util import obj_to_base64
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, RandomizedSearchCV

DEFAULT_STORAGE_ROOT: Path = Path(__file__).resolve().parents[4].joinpath('examples', 'models')

DATA = pd.read_csv(
    Path(__file__).resolve().parents[4].joinpath(
        'data', 'decisions-on-spark', 'data', 'miniloan', 'miniloan-decisions-ls-10K.csv'
    ),
    header=0,
    delimiter=r'\s*,\s*',
    engine='python',
    names=['name', 'creditScore', 'income', 'loanAmount', 'monthDuration', 'approval', 'rate', 'yearlyReimbursement'],
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
).replace([np.inf, -np.inf], np.nan).dropna()

INPUT_SCHEMA: List[Any] = [
    {
        'name': "creditScore",
        'order': 0,
        'type': 'int64'
    },
    {
        'name': "income",
        'order': 1,
        'type': 'float64'
    },
    {
        'name': "loanAmount",
        'order': 2,
        'type': 'float64'
    },
    {
        'name': "monthDuration",
        'order': 3,
        'type': 'float64'
    },
    {
        'name': "rate",
        'order': 4,
        'type': 'float64'
    }
]


def miniloan_lr_zip() -> Path:
    logger = logging.getLogger(__name__)

    des: Path = DEFAULT_STORAGE_ROOT.joinpath('miniloan-lr.zip')
    if des.exists() and not os.getenv('EML_RETRAIN_MODELS'):
        logger.debug(f'model {des} exists, set EML_RETRAIN_MODELS to retain')
        return des

    data = DATA.loc[:, ['creditScore', 'income', 'loanAmount', 'monthDuration', 'rate', 'approval']]

    train, test = train_test_split(data, random_state=0)

    logger.info('training size: {size}'.format(size=len(train)))
    logger.info('validation size: {size}'.format(size=len(test)))

    grid = {
        'penalty': ['l2'],
        'dual': [False],
        'tol': [x for x in np.linspace(1e-5, 5e-1, num=1000)],
        'C': [x for x in np.linspace(1e-5, 1.0, num=1000)]
    }

    hyper_tuning_params = {
        'estimator': LogisticRegression(random_state=0),
        'cv': 3,
        'verbose': bool(__debug__),
        'n_jobs': -1,
        'scoring': 'accuracy',
        'error_score': 'raise'
    }

    random_search = {
        'param_distributions': grid,
        'random_state': 42,
        'n_iter': 500
    }

    parameter_estimator = RandomizedSearchCV(**{**hyper_tuning_params, **random_search})

    x = train.loc[:, ['creditScore', 'income', 'loanAmount', 'monthDuration', 'rate']]
    y = train.loc[:, 'approval']

    parameter_estimator.fit(x, y)
    best_estimator = LogisticRegression(
        random_state=0,
        **parameter_estimator.best_params_
    )

    best_estimator.fit(x, y)

    res = best_estimator.score(test.loc[:, ['creditScore', 'income', 'loanAmount', 'monthDuration', 'rate']],
                               test.loc[:, 'approval'])
    logger.info('accuracy: ' + str(res))

    internal_model = Model(
        model=obj_to_base64(best_estimator),
        name='miniloan-lr',
        version='v0',
        method_name='predict',
        input_schema=INPUT_SCHEMA,
        output_schema={
            'attributes': [
                {
                    'name': 'prediction',
                    'type': 'str'
                }
            ]
        },
        metadata={
            'description': 'Loan approval',
            'author': 'ke',
            'trained_at': datetime.utcnow().isoformat(),
            'metrics': [
                {
                    'name': 'accuracy',
                    'value': res
                }
            ]
        }
    )

    return internal_model.to_archive(directory=DEFAULT_STORAGE_ROOT, zip_file_name='miniloan-lr.zip')


def miniloan_rfr_zip() -> Path:
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    des: Path = DEFAULT_STORAGE_ROOT.joinpath('miniloan-rfr.zip')
    if des.exists() and not os.getenv('EML_RETRAIN_MODELS'):
        logger.debug(f'model {des} exists, set EML_RETRAIN_MODELS to retain')
        return des

    data = DATA.loc[:, ['creditScore', 'income', 'loanAmount', 'monthDuration', 'rate', 'yearlyReimbursement']]

    train, test = train_test_split(data, random_state=0)

    logger.info('training size: {size}'.format(size=len(train)))
    logger.info('validation size: {size}'.format(size=len(test)))

    grid = {
        'criterion': ['mse'],
        'n_estimators': [int(x) for x in np.linspace(50, 1000, num=20)],
        'min_samples_split': [int(x) for x in np.linspace(2, 64, num=50)],
        'min_samples_leaf': [int(x) for x in np.linspace(1, 32, num=20)]
    }

    hyper_tuning_params = {
        'estimator': RandomForestRegressor(random_state=0),
        'cv': 3,
        'verbose': bool(__debug__),
        'n_jobs': -1,
        'error_score': 'raise'
    }

    random_search = {
        'param_distributions': grid,
        'random_state': 42,
        'n_iter': 20
    }

    parameter_estimator = RandomizedSearchCV(**{**hyper_tuning_params, **random_search})

    x = train.loc[:, ['creditScore', 'income', 'loanAmount', 'monthDuration', 'rate']]
    y = train.loc[:, 'yearlyReimbursement']

    parameter_estimator.fit(x, y)
    best_estimator = RandomForestRegressor(
        random_state=0,
        **parameter_estimator.best_params_
    )

    best_estimator.fit(x, y)

    res = best_estimator.score(test.loc[:, ['creditScore', 'income', 'loanAmount', 'monthDuration', 'rate']],
                               test.loc[:, 'yearlyReimbursement'])
    logger.info('score: ' + str(res))

    internal_model = Model(
        model=obj_to_base64(best_estimator),
        name='miniloan-rfr',
        version='v0',
        method_name='predict',
        input_schema=INPUT_SCHEMA,
        output_schema={
            'attributes': [
                {
                    'name': 'prediction',
                    'type': 'float'
                }
            ]
        },
        metadata={
            'description': 'Evaluation of yearlyReimbursement',
            'author': 'ke',
            'trained_at': datetime.utcnow().isoformat(),
            'metrics': [
                {
                    'name': 'r2',
                    'value': res
                }
            ]
        }

    )

    return internal_model.to_archive(directory=DEFAULT_STORAGE_ROOT, zip_file_name='miniloan-rfr.zip')


def miniloan_rfc_zip() -> Path:
    logger = logging.getLogger(__name__)

    des: Path = DEFAULT_STORAGE_ROOT.joinpath('miniloan-rfc.zip')
    if des.exists() and not os.getenv('EML_RETRAIN_MODELS'):
        logger.debug(f'model {des} exists, set EML_RETRAIN_MODELS to retain')
        return des

    used_names = ['creditScore', 'income', 'loanAmount', 'monthDuration', 'rate', 'approval']

    train, test = train_test_split(DATA, random_state=7)

    logger.info(f'training size: {len(train)}')
    logger.info(f'validation size: {len(test)}')

    params = {
        'estimator': RandomForestClassifier(random_state=42),
        'cv': 3,
        'verbose': bool(__debug__),
        'n_jobs': -1,
        'random_state': 21,
        'n_iter': 5,
        'scoring': 'accuracy',
        'error_score': 'raise',
        'param_distributions': {
            'criterion': ['gini'],
            'n_estimators': [int(x) for x in np.linspace(50, 1000, num=20)],
            'min_samples_split': [int(x) for x in np.linspace(2, 64, num=50)],
            'min_samples_leaf': [int(x) for x in np.linspace(1, 32, num=20)]
        }
    }

    parameter_estimator = RandomizedSearchCV(**params)

    x_train = train.loc[:, used_names[:-1]]
    y_train = train.loc[:, used_names[-1]]

    parameter_estimator.fit(x_train, y_train)
    best_estimator = RandomForestClassifier(
        random_state=42,
        **parameter_estimator.best_params_
    )

    best_estimator.fit(x_train, y_train)

    acc = best_estimator.score(test.loc[:, used_names[:-1]],
                               test.loc[:, used_names[-1]])
    logger.info(f'accuracy: {acc}')

    conf = {
        'name': 'miniloan-rfc',
        'version': 'v0',
        'method_name': 'predict_proba',
        'input_schema': [
            {
                'name': "creditScore",
                'order': 0,
                'type': 'int64'
            },
            {
                'name': "income",
                'order': 1,
                'type': 'float64'
            },
            {
                'name': "loanAmount",
                'order': 2,
                'type': 'float64'
            },
            {
                'name': "monthDuration",
                'order': 3,
                'type': 'float64'
            },
            {
                'name': "rate",
                'order': 4,
                'type': 'float64'
            }
        ],
        'output_schema': {
            'attributes': [
                {
                    'name': 'prediction',
                    'type': 'str'
                }
            ]
        },
        'metadata': {
            'description': 'Loan approval',
            'author': 'ke',
            'trained_at': datetime.utcnow().isoformat(),
            'metrics': [
                {
                    'name': 'accuracy',
                    'value': acc
                }
            ]
        }
    }

    internal_model = Model(
        model=obj_to_base64(best_estimator),
        **conf
    )

    return internal_model.to_archive(directory=DEFAULT_STORAGE_ROOT, zip_file_name='miniloan-rfc.zip')


def miniloan_lr_pickle() -> Path:
    logger = logging.getLogger(__name__)

    des: Path = DEFAULT_STORAGE_ROOT.joinpath('miniloan-lr.pkl')
    if des.exists() and not os.getenv('EML_RETRAIN_MODELS'):
        logger.debug(f'model {des} exists, set EML_RETRAIN_MODELS to retain')
        return des

    data = DATA.loc[:, ['creditScore', 'income', 'loanAmount', 'monthDuration', 'rate', 'approval']]

    train, test = train_test_split(data, random_state=0)

    logger.info('training size: {size}'.format(size=len(train)))
    logger.info('validation size: {size}'.format(size=len(test)))

    grid = {
        'penalty': ['l2'],
        'dual': [False],
        'tol': [x for x in np.linspace(1e-5, 5e-1, num=1000)],
        'C': [x for x in np.linspace(1e-5, 1.0, num=1000)]
    }

    hyper_tuning_params = {
        'estimator': LogisticRegression(random_state=0),
        'cv': 3,
        'verbose': bool(__debug__),
        'n_jobs': -1,
        'scoring': 'accuracy',
        'error_score': 'raise'
    }

    random_search = {
        'param_distributions': grid,
        'random_state': 42,
        'n_iter': 10
    }

    parameter_estimator = RandomizedSearchCV(**{**hyper_tuning_params, **random_search})

    x = train.loc[:, ['creditScore', 'income', 'loanAmount', 'monthDuration', 'rate']]
    y = train.loc[:, 'approval']

    parameter_estimator.fit(x, y)
    best_estimator = LogisticRegression(
        random_state=0,
        **parameter_estimator.best_params_
    )

    best_estimator.fit(x, y)

    res = best_estimator.score(test.loc[:, ['creditScore', 'income', 'loanAmount', 'monthDuration', 'rate']],
                               test.loc[:, 'approval'])
    logger.info('accuracy: ' + str(res))

    conf = {
        'name': 'miniloan-lr',
        'version': 'v0',
        'method_name': 'predict',
        'input_schema': INPUT_SCHEMA,
        'output_schema': {
            'attributes': [
                {
                    'name': 'prediction',
                    'type': 'str'
                }
            ]
        },
        'metadata': {
            'description': 'Loan approval',
            'author': 'ke',
            'trained_at': datetime.utcnow().isoformat(),
            'metrics': [
                {
                    'name': 'accuracy',
                    'value': res
                }
            ]
        }
    }

    with des.open(mode='wb') as fd:
        pickle.dump(
            obj={
                'model': best_estimator,
                'model_config': conf
            },
            file=fd
        )

    return des


def miniloan_rfc_pickle() -> Path:
    logger = logging.getLogger(__name__)

    des: Path = DEFAULT_STORAGE_ROOT.joinpath('miniloan-rfc.pkl')
    if des.exists() and not os.getenv('EML_RETRAIN_MODELS'):
        logger.debug(f'model {des} exists, set EML_RETRAIN_MODELS to retain')
        return des

    used_names = ['creditScore', 'income', 'loanAmount', 'monthDuration', 'rate', 'approval']

    train, test = train_test_split(DATA, random_state=7)

    logger.info(f'training size: {len(train)}')
    logger.info(f'validation size: {len(test)}')

    params = {
        'estimator': RandomForestClassifier(random_state=42),
        'cv': 3,
        'verbose': bool(__debug__),
        'n_jobs': -1,
        'random_state': 21,
        'n_iter': 5,
        'scoring': 'accuracy',
        'error_score': 'raise',
        'param_distributions': {
            'criterion': ['gini'],
            'n_estimators': [int(x) for x in np.linspace(50, 1000, num=20)],
            'min_samples_split': [int(x) for x in np.linspace(2, 64, num=50)],
            'min_samples_leaf': [int(x) for x in np.linspace(1, 32, num=20)]
        }
    }

    parameter_estimator = RandomizedSearchCV(**params)

    x_train = train.loc[:, used_names[:-1]]
    y_train = train.loc[:, used_names[-1]]

    parameter_estimator.fit(x_train, y_train)
    best_estimator = RandomForestClassifier(
        random_state=42,
        **parameter_estimator.best_params_
    )

    best_estimator.fit(x_train, y_train)

    acc = best_estimator.score(test.loc[:, used_names[:-1]],
                               test.loc[:, used_names[-1]])
    logger.info(f'accuracy: {acc}')

    conf = {
        'name': 'miniloan-rfc',
        'version': 'v0',
        'method_name': 'predict_proba',
        'input_schema': [
            {
                'name': "creditScore",
                'order': 0,
                'type': 'int64'
            },
            {
                'name': "income",
                'order': 1,
                'type': 'float64'
            },
            {
                'name': "loanAmount",
                'order': 2,
                'type': 'float64'
            },
            {
                'name': "monthDuration",
                'order': 3,
                'type': 'float64'
            },
            {
                'name': "rate",
                'order': 4,
                'type': 'float64'
            }
        ],
        'output_schema': {
            'attributes': [
                {
                    'name': 'prediction',
                    'type': 'str'
                },
                {
                    'name': 'probabilities',
                    'type': '[Probability]'
                }
            ]
        },
        'metadata': {
            'description': 'Loan approval',
            'author': 'ke',
            'trained_at': datetime.utcnow().isoformat(),
            'class_names': {
                i: val for i, val in enumerate(best_estimator.classes_)
            },
            'metrics': [
                {
                    'name': 'accuracy',
                    'value': acc
                }
            ]
        }
    }

    with des.open(mode='wb') as fd:
        pickle.dump(
            obj={
                'model': best_estimator,
                'model_config': conf
            },
            file=fd
        )

    return des


def miniloan_rfc_no_class_names_pickle() -> Path:
    logger = logging.getLogger(__name__)

    des: Path = DEFAULT_STORAGE_ROOT.joinpath('miniloan-rfc-no-output-schema.pkl')
    if des.exists() and not os.getenv('EML_RETRAIN_MODELS'):
        logger.debug(f'model {des} exists, set EML_RETRAIN_MODELS to retain')
        return des

    used_names = ['creditScore', 'income', 'loanAmount', 'monthDuration', 'rate', 'approval']

    train, test = train_test_split(DATA, random_state=7)

    logger.info(f'training size: {len(train)}')
    logger.info(f'validation size: {len(test)}')

    params = {
        'estimator': RandomForestClassifier(random_state=42),
        'cv': 3,
        'verbose': bool(__debug__),
        'n_jobs': -1,
        'random_state': 21,
        'n_iter': 5,
        'scoring': 'accuracy',
        'error_score': 'raise',
        'param_distributions': {
            'criterion': ['gini'],
            'n_estimators': [int(x) for x in np.linspace(50, 1000, num=20)],
            'min_samples_split': [int(x) for x in np.linspace(2, 64, num=50)],
            'min_samples_leaf': [int(x) for x in np.linspace(1, 32, num=20)]
        }
    }

    parameter_estimator = RandomizedSearchCV(**params)

    x_train = train.loc[:, used_names[:-1]]
    y_train = train.loc[:, used_names[-1]]

    parameter_estimator.fit(x_train, y_train)
    best_estimator = RandomForestClassifier(
        random_state=42,
        **parameter_estimator.best_params_
    )

    best_estimator.fit(x_train, y_train)

    acc = best_estimator.score(test.loc[:, used_names[:-1]],
                               test.loc[:, used_names[-1]])
    logger.info(f'accuracy: {acc}')

    conf = {
        'name': 'miniloan-rfc-no-output-schema',
        'version': 'v0',
        'method_name': 'predict_proba',
        'input_schema': [
            {
                'name': "creditScore",
                'order': 0,
                'type': 'int64'
            },
            {
                'name': "income",
                'order': 1,
                'type': 'float64'
            },
            {
                'name': "loanAmount",
                'order': 2,
                'type': 'float64'
            },
            {
                'name': "monthDuration",
                'order': 3,
                'type': 'float64'
            },
            {
                'name': "rate",
                'order': 4,
                'type': 'float64'
            }
        ],
        'output_schema': {
            'attributes': [
                {
                    'name': 'prediction',
                    'type': 'str'
                },
                {
                    'name': 'probabilities',
                    'type': '[Probability]'
                }
            ]
        },
        'metadata': {
            'description': 'Loan approval',
            'author': 'ke',
            'trained_at': datetime.utcnow().isoformat(),
            'metrics': [
                {
                    'name': 'accuracy',
                    'value': acc
                }
            ]
        }
    }

    with des.open(mode='wb') as fd:
        pickle.dump(
            obj={
                'model': best_estimator,
                'model_config': conf
            },
            file=fd
        )

    return des


def miniloan_rfr_pickle() -> Path:
    logger = logging.getLogger(__name__)

    des: Path = DEFAULT_STORAGE_ROOT.joinpath('miniloan-rfr.pkl')
    if des.exists() and not os.getenv('EML_RETRAIN_MODELS'):
        logger.debug(f'model {des} exists, set EML_RETRAIN_MODELS to retain')
        return des

    data = DATA.loc[:, ['creditScore', 'income', 'loanAmount', 'monthDuration', 'rate', 'yearlyReimbursement']]

    train, test = train_test_split(data, random_state=0)

    logger.info('training size: {size}'.format(size=len(train)))
    logger.info('validation size: {size}'.format(size=len(test)))

    grid = {
        'criterion': ['mse'],
        'n_estimators': [int(x) for x in np.linspace(50, 1000, num=20)],
        'min_samples_split': [int(x) for x in np.linspace(2, 64, num=50)],
        'min_samples_leaf': [int(x) for x in np.linspace(1, 32, num=20)]
    }

    hyper_tuning_params = {
        'estimator': RandomForestRegressor(random_state=0),
        'cv': 3,
        'verbose': bool(__debug__),
        'n_jobs': -1,
        'error_score': 'raise'
    }

    random_search = {
        'param_distributions': grid,
        'random_state': 42,
        'n_iter': 10
    }

    parameter_estimator = RandomizedSearchCV(**{**hyper_tuning_params, **random_search})

    x = train.loc[:, ['creditScore', 'income', 'loanAmount', 'monthDuration', 'rate']]
    y = train.loc[:, 'yearlyReimbursement']

    parameter_estimator.fit(x, y)
    best_estimator = RandomForestRegressor(
        random_state=0,
        **parameter_estimator.best_params_
    )

    best_estimator.fit(x, y)

    res = best_estimator.score(test.loc[:, ['creditScore', 'income', 'loanAmount', 'monthDuration', 'rate']],
                               test.loc[:, 'yearlyReimbursement'])
    logger.info('score: ' + str(res))

    conf = {
        'name': 'miniloan-rfr',
        'version': 'v0',
        'method_name': 'predict',
        'input_schema': INPUT_SCHEMA,
        'output_schema': {
            'attributes': [
                {
                    'name': 'prediction',
                    'type': 'float'
                }
            ]
        },
        'metadata': {
            'description': 'Evaluation of yearlyReimbursement',
            'author': 'ke',
            'trained_at': datetime.utcnow().isoformat(),
            'metrics': [
                {
                    'name': 'r2',
                    'value': res
                }
            ]
        }

    }

    with des.open(mode='wb') as fd:
        pickle.dump(
            obj={
                'model': best_estimator,
                'model_config': conf
            },
            file=fd
        )

    return des


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.ERROR)
    miniloan_lr_pickle()
    miniloan_rfc_pickle()
    miniloan_rfr_pickle()
