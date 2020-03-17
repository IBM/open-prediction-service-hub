#!/usr/bin/env python3

from __future__ import annotations

from typing import Any, Text, Union, List, Dict, Mapping

import numpy as np
from pydantic import BaseModel, Field


class BaseResponseBody(BaseModel):
    """Ml output"""
    raw_output: Union[Text, Dict] = Field(
        ...,
        description=
        'Data frame representation of result ndarray. '
        'It should be used when the result of predictor can not be serialized by predefined output serializer'
    )


class PredictResponseBody(BaseResponseBody):
    """Ml output for the most common model.predict(array_like)"""
    predict_output: Union[Text, np.float64] = Field(
        ...,
        description=
        'Common output for model.predict(array_like)'
    )


class FeatProbaPair(BaseModel):
    """Pair of feature name and its corresponding probability"""
    name: Text
    proba: np.float64


class PredictProbaResponseBody(BaseResponseBody):
    """Ml output for the most common model.predict(array_like)"""
    predict_output: Text = Field(
        ...,
        description=
        'The classification result which maximize model.predict_proba(array_like)'
    )
    probabilities: List[FeatProbaPair] = Field(
        ...,
        description=
        'Common output for model.predict_proba(array_like)'
    )
