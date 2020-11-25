import json

supported_models=["regression"]

def get_model_conf(model_id):
    return json.load(open(f"data/{model_id}/deployment_conf.json","r"))