# Model deployment

Open prediction service can serve classifiers/regressors that follow the 
[scikit learn predictor API](https://scikit-learn.org/stable/developers/develop.html#apis-of-scikit-learn-objects). As 
predictor API is not an abstract interface but a widely used convention, this web service can be
used for a much richer range of libraries(e.g xgboost). To use libraries other than scikit-learn 
and xgboost, user only needs to add dependencies into `requirements-ml.txt` before building 
docker image. 

## Getting started

For each type of machine learning (classification/regression), examples are 
given in `examples/model_training_and_deployment/<type>`. Each project 
inside `<type>/` is a separate deployment project.

### Deployment projects

Each project contains a python scripts and an example configuration file. 

project structure:
```
**/<type>/project
    └── training.py
    └── deployment_conf.json
```

`training.py` trains an example ML model and stores the model in
`model.[pkl, bst]`.

Documents for `deployment_conf.json` can be found:
[Configuration](../../README.md#Open-Prediction-Service)
