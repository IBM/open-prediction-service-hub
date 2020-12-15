import json
import os
import logging
from urllib.parse import quote_plus, unquote_plus


def model_encode(model_dir):
    return model_dir.replace('/', '|')

supported_models = [model_encode(root[7:]) # to get rid of `./data/` characters and encode subdirectories / into |
                    for root, dir, files in os.walk("./data")
                    for file in files if file.endswith("model.pkl")]


def model_decode(model_id):
    return model_id.replace('|', '/')


def get_model_conf(model_id):
    model_dir = model_decode(model_id)
    return json.load(open(f"data/{model_dir}/deployment_conf.json", "r"))
