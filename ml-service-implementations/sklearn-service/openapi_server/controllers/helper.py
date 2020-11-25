import json
import os



supported_models=[ root[7:] for root, dir, files in os.walk("./data") for file in files if file.endswith("model.pkl")]

def get_model_conf(model_id):
    return json.load(open(f"data/{model_id}/deployment_conf.json","r"))