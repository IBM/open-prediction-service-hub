import logging
import sys

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.svm import SVC
from sklearn.datasets import load_iris
from pathlib import Path
from time import gmtime, strftime

from dynamic_hosting.core.model import MLModel


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
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

    internal_model = MLModel(
        model=best_estimator,
        name='iris-svc-RandomizedSearchCV',
        version='v0',
        method_name='predict',
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
            'name': 'Loan payment classification',
            'author': 'ke',
            'date': strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            'metrics': {
                'accuracy': res
            }
        }

    )

    storage_root = Path(__file__).resolve().parents[3].joinpath('example_models')
    internal_model.save_to_disk(storage_root=storage_root)


if __name__ == '__main__':
    main()
