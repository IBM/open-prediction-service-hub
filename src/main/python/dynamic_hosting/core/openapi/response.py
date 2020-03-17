#!/usr/bin/env python3

from __future__ import annotations

from typing import Any, Text, Union, List

import numpy as np
from pydantic import BaseModel, Field


class BaseResponseBody(BaseModel):
    """Ml output"""
    raw_output: Any = Field(
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


class PredictProbaResponseBody(BaseResponseBody):
    """Ml output for the most common model.predict(array_like)"""
    predict_output: Text = Field(
        ...,
        description=
        'The classification result which maximize model.predict_proba(array_like)'
    )
    predict_proba_output: List[np.float64] = Field(
        ...,
        description=
        'Common output for model.predict_proba(array_like)'
    )
