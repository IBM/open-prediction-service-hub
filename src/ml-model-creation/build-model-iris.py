#
# This program builds a SVM model to predict a loan payment default.
# It reads a labelled dataset of loan payments, makes the model, measures its accuracy and performs unit tests.
# It ends by a serialization through models. The serialized model is then used by the main program that serves it.
#

import os
import pandas as pd
import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

from sklearn import svm
from sklearn import datasets

# Prepare data
iris = load_iris()
X = pd.DataFrame(iris.data)
X.columns = np.array(iris.feature_names)
y = pd.Series(np.array(iris.target_names)[iris.target])
y.name = "Class"
X_tr, X_test, y_tr, y_test = train_test_split(X, y, test_size=0.33, random_state=123)

model = svm.SVC()
X, y = datasets.load_iris(return_X_y=True)
model.fit(X, y)

prediction = model.predict(X_test)

score = model.score(X_test, y_test)

# Unit test

prediction = model.predict(iris.data[:3])

# Model serialization


d = datetime.datetime.today()

toBePersisted = dict({
    'model': model,
    'metadata': {
        'name': 'iris',
        'author': 'Pierre Feillet',
        'date': d,
        'metrics': {
            'accuracy': score
        },
        'invocation': 'predict',
        'signature': [
            {
                'name': "sepal length",
                'order': 0,
                'type': 'float'
            },
            {
                'name': "sepal width",
                'order': 1,
                'type': 'float'
            },
            {
                'name': "petal length",
                'order': 2,
                'type': 'float'
            },
            {
                'name': "petal width",
                'order': 3,
                'type': 'float'
            }
        ]
    },
    'outcome': {
        'probabilities': '[float]',
        'prediction': 'Iris Setosa, Iris Versicolour, Iris Virginica'
    },
})

modelFilePath = 'models/iris-svc.joblib'
from joblib import dump

dump(toBePersisted, modelFilePath)

# Testing deserialized model

from joblib import load

dictionary = load(modelFilePath)
loaded_model = dictionary['model']

#5.1,3.5,1.4,0.2,Iris-setosa
prediction = loaded_model.predict([[5.1,3.5,1.4,0.2]])
print("prediction with serialized model: " + str(prediction) + " expect [0]")

#6.0,3.4,4.5,1.6,Iris-versicolor
prediction = loaded_model.predict([[6.0,3.4,4.5,1.6]])
print("prediction with serialized model: " + str(prediction) + " expect [1]")

#6.3,2.5,5.0,1.9,Iris-virginica
prediction = loaded_model.predict([[6.3,2.5,5.0,1.9]])
print("prediction with serialized model: " + str(prediction) + " expect [2]")
