import lime.lime_tabular
from openapi_server.common import get_feature_names
from openapi_server.loan_scoring import pipeline, x_train_data

explainer = lime.lime_tabular.LimeTabularExplainer(
    x_train_data.values,
    feature_names=get_feature_names(),
    class_names=["No Payment Default", "Payment Default"],
    discretize_continuous=False)


def explain(data):
    explanation = explainer.explain_instance(data, pipeline.predict_proba, top_labels=1)
    return explanation.as_list(explanation.available_labels()[0])
