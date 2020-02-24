#
# This program builds a SVM model to predict a loan payment default.
# It reads a labelled dataset of loan payments, makes the model, measures its accuracy and performs unit tests.
# It ends by a serialization through models. The serialized model is then used by the main program that serves it.
#

import os
import pandas as pd
from sklearn import svm
import pickle

data = pd.read_csv('data/miniloan-decisions-default-1K.csv', sep=',',header=0)
data.head()
print("Number of records: " + str(data.count()))

from sklearn.model_selection import train_test_split
from sklearn import metrics

#creditScore,income,loanAmount,monthDuration,rate,yearlyReimbursement,paymentDefault
X=data[['creditScore', 'income', 'loanAmount', 'monthDuration', 'rate' , 'yearlyReimbursement' ]] # Features
y=data['paymentDefault']  # Label

# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3) # 70% training and 30% test

model = svm.LinearSVC()
model.fit(X_train, y_train)

# Model Accuracy, how often is the classifier correct?
y_pred=model.predict(X_test)
accuracy = metrics.accuracy_score(y_test, y_pred)
print("Accuracy:",accuracy)

#Unit test
prediction = model.predict([[397,160982,570189,240,0.07,57195]]) # expected 1 meaning default
print("prediction with SVM: " + str(prediction) + " expect [1]")
decision_function = model.decision_function([[397,160982,570189,240,0.07,57195]]) # expected 1
print("Confidence levels:", decision_function)

prediction = model.predict([[580,66037,168781,120,0.09,16187]]) # expected 0
print("prediction with SVM: " + str(prediction) + " expect [0]")
decision_function = model.decision_function([[580,66037,168781,120,0.09,16187]]) # expected 0 meaning absence of default
print("Confidence levels:", decision_function)

creditScore = 397
income = 160982
loanAmount = 570189
monthDuration = 240
rate = 0.07
yearlyReimbursement = 57195
prediction = model.predict([[creditScore, income, loanAmount, monthDuration, rate, yearlyReimbursement]])
print("prediction with SVM: " + str(prediction) + " expect [1]")

#Model serialization
toBePersisted = dict({
    'model': model,
    'metadata': {
        'name': 'loan payment default classification',
        'author': 'Pierre Feillet',
        'date': '2020-01-28T15:45:00CEST',
        'metrics': {
            'accuracy': accuracy
        }
    }
})

modelFilePath = 'models/miniloandefault-svc.joblib'

from joblib import dump
dump(toBePersisted, modelFilePath)

#Testing deserialized model

from joblib import load
dictionary = load(modelFilePath)
loaded_model = dictionary['model']
prediction = loaded_model.predict([[creditScore, income, loanAmount, monthDuration, rate, yearlyReimbursement]])
print("prediction with serialized Support Vector Machine: " + str(prediction) + " expect [1]")
