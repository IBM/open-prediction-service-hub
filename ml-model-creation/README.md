# Machine Learning model creation

This projects gathers sample code to create several ML models:
- a Logistic Regression model to predict a loan payment default.
- an SVM model to predict a loan payment default.
- a Random Forest Classification model to predict a loan payment default.
- an Iris multi-classification model.

These models have already been trained and serialized as pickle and joblib files with Python 3.6. So running the creation code is necessary only when changing the datasets, models or updating the Python libraries. 

## Creating the ML models
```console
python build*.py
```
## Check the ML models
Models are generated under the local models folder and repicated under the model folder of the 2 other microservice projects. 

