#!/usr/bin/env python3

from __future__ import annotations

from typing import Optional, Any

from pydantic import BaseModel, Field


class BaseResponseBody(BaseModel):
    """Ml output"""
    raw_output: Optional[Any] = Field(
        ...,
        description=
        'Data frame representation of result ndarray. '
        'It should be used when the result of predictor can not be serialized by predefined output serializer'
    )
