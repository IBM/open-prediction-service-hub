#!/usr/bin/env python3
from __future__ import annotations

from typing import Text, List, Dict, Sequence, Any

from pydantic import BaseModel


class RequestMetadata(BaseModel):
    model_name: Text = 'model_name'
    model_version: Text = 'model_version'


class BaseRequestBody(BaseModel):
    metadata: RequestMetadata

    class Config:
        fields = {'metadata': '__metadata__'}


class Parameter(BaseModel):
    name: Text = 'Feature name'
    order: int = 0
    value: Any = 'Feature value'


class GenericRequestBody(BaseRequestBody):
    params: List[Parameter] = list()

    @staticmethod
    def params_to_dict(ml_req: GenericRequestBody) -> Dict[Text, Sequence]:
        return {
            feat_val.name: [feat_val.value]
            for feat_val in ml_req.params
        }
