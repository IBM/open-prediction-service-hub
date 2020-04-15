import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Text

import numpy as np
import pandas as pd
from dynamic_hosting.core.model import Model
from dynamic_hosting.core.util import obj_to_base64
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.svm import SVC

DEFAULT_STORAGE_ROOT_DIR_NAME: Text = 'examples'
DEFAULT_STORAGE_ROOT: Path = Path(__file__).resolve().parents[4].joinpath(DEFAULT_STORAGE_ROOT_DIR_NAME)


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    col_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class_name']

    iris = load_iris()

    data = pd.DataFrame(
        data=np.c_[iris['data'], iris['target']],
        columns=col_names
    )

    data = data.replace([np.inf, -np.inf], np.nan).dropna()

    train, test = train_test_split(data, random_state=0)

    logger.info('training size: {size}'.format(size=len(train)))
    logger.info('validation size: {size}'.format(size=len(test)))

    grid = {
        'C': [x for x in np.linspace(1e-5, 1.0, num=1000)],
        'tol': [x for x in np.linspace(1e-5, 5e-1, num=1000)],
        'kernel': ['linear', 'poly', 'rbf', 'sigmoid', 'rbf']
    }

    hyper_tuning_params = {
        'estimator': SVC(random_state=0),
        'cv': 3,
        'verbose': bool(__debug__),
        'n_jobs': -1,
        'scoring': 'accuracy',
        'error_score': 'raise'
    }

    random_search = {
        'param_distributions': grid,
        'random_state': 42,
        'n_iter': 1000
    }

    parameter_estimator = RandomizedSearchCV(**{**hyper_tuning_params, **random_search})

    x = data.loc[:, col_names[:-1]]
    y = data.loc[:, col_names[-1]]

    parameter_estimator.fit(x, y)
    best_estimator = SVC(
        random_state=0,
        **parameter_estimator.best_params_
    )

    best_estimator.fit(x, y)

    res = best_estimator.score(test.loc[:, col_names[:-1]],
                               test.loc[:, col_names[-1]])
    logger.info('accuracy: ' + str(res))

    internal_model = Model(
        model=obj_to_base64(best_estimator),
        name='iris-svc',
        version='v0',
        method_name='predict',
        type='CLASSIFICATION',
        input_schema=[
            {
                'name': "sepal_length",
                'order': 0,
                'type': 'float64'
            },
            {
                'name': "sepal_width",
                'order': 1,
                'type': 'float64'
            },
            {
                'name': "petal_length",
                'order': 2,
                'type': 'float64'
            },
            {
                'name': "petal_width",
                'order': 3,
                'type': 'float64'
            }
        ],
        output_schema=None,
        metadata={
            'description': 'Iris classification',
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

    internal_model.to_archive(directory=DEFAULT_STORAGE_ROOT, zip_file_name='iris-svc.zip')


if __name__ == '__main__':
    main()
