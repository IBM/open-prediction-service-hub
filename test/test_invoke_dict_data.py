import logging
import sys
from time import gmtime, strftime

import numpy as np
import pandas as pd
from dynamic_hosting.core.model import MLModel
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.svm import SVC


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
        'n_iter': 100
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

    test_x: pd.DataFrame = test.loc[:, col_names[:-1]]
    test_dict = test_x.to_dict(orient='list')

    internal_model.invoke_from_dict(test_dict)


if __name__ == '__main__':
    main()
