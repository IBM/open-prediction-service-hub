import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Text, List, Type, Dict

import numpy as np
import pandas as pd
from dynamic_hosting.core.model import Model
from dynamic_hosting.core.util import obj_to_base64
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, RandomizedSearchCV

DEFAULT_STORAGE_ROOT_DIR_NAME: Text = 'examples'
DEFAULT_STORAGE_ROOT: Path = Path(__file__).resolve().parents[4].joinpath(DEFAULT_STORAGE_ROOT_DIR_NAME).joinpath(
    'models')

NAMES: List[Text] = ['name', 'creditScore', 'income', 'loanAmount', 'monthDuration', 'approval', 'rate',
                     'yearlyReimbursement']
DTYPES: Dict[Text, Type] = {
    'name': np.object,
    'creditScore': np.float64,
    'income': np.float64,
    'loanAmount': np.float64,
    'monthDuration': np.float64,
    'approval': np.object,
    'rate': np.float64,
    'yearlyReimbursement': np.float64
}

MINILOAN_FILE: Path = DEFAULT_STORAGE_ROOT.parent.parent.joinpath(
    'data', 'decisions-on-spark', 'data', 'miniloan'
).joinpath('{dataset_name}.{extension}'.format(
    dataset_name='miniloan-decisions-ls-10K', extension='csv')
)

DATA = pd.read_csv(
    MINILOAN_FILE,
    header=0,
    delimiter=r'\s*,\s*',
    engine='python',
    names=NAMES,
    dtype=DTYPES
)


def miniloan_lr() -> Path:
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    data = DATA.replace([np.inf, -np.inf], np.nan).dropna()
    data = data.loc[:, ['creditScore', 'income', 'loanAmount', 'monthDuration', 'rate', 'approval']]

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
        type='CLASSIFICATION',
        input_schema=[
            {
                'name': "creditScore",
                'order': 0,
                'type': 'float64'
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
        output_schema=None,
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


def miniloan_rfr() -> Path:
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    data = DATA.replace([np.inf, -np.inf], np.nan).dropna()
    data = data.loc[:, ['creditScore', 'income', 'loanAmount', 'monthDuration', 'rate', 'yearlyReimbursement']]

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
        type='REGRESSION',
        input_schema=[
            {
                'name': "creditScore",
                'order': 0,
                'type': 'int64'
            },
            {
                'name': "income",
                'order': 1,
                'type': 'float32'
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
        output_schema=None,
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


def miniloan_rfc() -> Path:
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    data = DATA.replace([np.inf, -np.inf], np.nan).dropna()
    data = data.loc[:, ['creditScore', 'income', 'loanAmount', 'monthDuration', 'rate', 'approval']]

    train, test = train_test_split(data, random_state=0)

    logger.info('training size: {size}'.format(size=len(train)))
    logger.info('validation size: {size}'.format(size=len(test)))

    grid = {
        'criterion': ['gini'],
        'n_estimators': [int(x) for x in np.linspace(50, 1000, num=20)],
        'min_samples_split': [int(x) for x in np.linspace(2, 64, num=50)],
        'min_samples_leaf': [int(x) for x in np.linspace(1, 32, num=20)]
    }

    hyper_tuning_params = {
        'estimator': RandomForestClassifier(random_state=0),
        'cv': 3,
        'verbose': bool(__debug__),
        'n_jobs': -1,
        'scoring': 'accuracy',
        'error_score': 'raise'
    }

    random_search = {
        'param_distributions': grid,
        'random_state': 42,
        'n_iter': 20
    }

    parameter_estimator = RandomizedSearchCV(**{**hyper_tuning_params, **random_search})

    x = train.loc[:, ['creditScore', 'income', 'loanAmount', 'monthDuration', 'rate']]
    y = train.loc[:, 'approval']

    parameter_estimator.fit(x, y)
    best_estimator = RandomForestClassifier(
        random_state=0,
        **parameter_estimator.best_params_
    )

    best_estimator.fit(x, y)

    res = best_estimator.score(test.loc[:, ['creditScore', 'income', 'loanAmount', 'monthDuration', 'rate']],
                               test.loc[:, 'approval'])
    logger.info('accuracy: ' + str(res))

    internal_model = Model(
        model=obj_to_base64(best_estimator),
        name='miniloan-rfc',
        version='v0',
        method_name='predict_proba',
        type='PREDICT_PROBA',
        input_schema=[
            {
                'name': "creditScore",
                'order': 0,
                'type': 'int64'
            },
            {
                'name': "income",
                'order': 1,
                'type': 'float32'
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
        output_schema=None,
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

    return internal_model.to_archive(directory=DEFAULT_STORAGE_ROOT, zip_file_name='miniloan-rfc.zip')
