#!/usr/bin/env python3

from __future__ import annotations

from typing import Text, List, Dict, Optional, Union

import numpy as np
from pydantic import BaseModel, Field, validator


class ServerStatus(BaseModel):
    model_count: np.long = Field(..., description='Number of ml models in local provider')


class FeatProbaPair(BaseModel):
    """Pair of feature name and its corresponding probability"""
    name: Text
    proba: np.float64


class Prediction(BaseModel):
    """Ml output for model.predict(array_like) and model.predict_proba(array_like)"""
    prediction: Text = Field(..., description='Model output for Classification/Regression')
    probabilities: Optional[List[FeatProbaPair]] = Field(..., description='Probabilities for classification result')

    @validator('probabilities', always=True)
    def probabilities_check(cls, probabilities: Optional[List[FeatProbaPair]]) -> Optional[List[FeatProbaPair]]:
        if probabilities is None:
            return probabilities
        if np.isclose(sum([pair.proba for pair in probabilities]), 1, rtol=1e-05, atol=1e-05, equal_nan=False):
            return probabilities
        else:
            raise ValueError('The sum of probabilities needs to be 1')
