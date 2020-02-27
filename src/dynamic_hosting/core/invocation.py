#!/usr/bin/env python3
from .models import Model
from pandas import DataFrame
from typing import Any


def invoke_predict(model: Model, data: DataFrame) -> Any:
    return model.invoke(data)
