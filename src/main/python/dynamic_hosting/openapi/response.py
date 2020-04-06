#!/usr/bin/env python3

from __future__ import annotations

from datetime import datetime
from typing import Text, List, Dict

import numpy as np
from pydantic import BaseModel, Field, validator


class ServerStatus(BaseModel):
    count: int = Field(..., description='Number of ml models in local provider')


class BaseResponseBody(BaseModel):
    """Ml output"""
    raw_output: Dict = Field(
        ...,
        description=
        'Data frame representation of result ndarray. '
        'It should be used when the result of predictor can not be serialized by predefined output serializer',
        example={'row_index': {'column_index': 'value'}}
    )


class ClassificationResponse(BaseModel):
    """Ml output for the most common model.predict(array_like)"""
    classification_output: Text = Field(
        ...,
        description=
        'Classification output for model.predict(array_like)'
    )


class RegressionResponse(BaseModel):
    """Ml output for the most common model.predict(array_like)"""
    regression_output: float = Field(
        ...,
        description=
        'Regression output for model.predict(array_like)'
    )


class FeatProbaPair(BaseModel):
    """Pair of feature name and its corresponding probability"""
    name: Text
    proba: np.float64


class PredictProbaResponse(BaseModel):
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

    @classmethod
    @validator('probabilities', pre=False, always=True)
    def probabilities_check(cls, probabilities: List[FeatProbaPair]) -> List[FeatProbaPair]:
        if np.isclose(sum([pair.proba for pair in probabilities]), 1, rtol=1e-08, atol=1e-08, equal_nan=False):
            return probabilities
        else:
            raise ValueError('The sum of probabilities needs to be 1')
