from __future__ import annotations

import pydantic
import datetime
import asyncio
import typing

from pydantic import BaseModel

from swagger_codegen.api.base import BaseApi
from swagger_codegen.api.request import ApiRequest
class Capabilities(BaseModel):
    capabilities: typing.List[str] 

class Error(BaseModel):
    error: typing.Optional[str]  = None

def make_request(self: BaseApi,


) -> Capabilities:
    """Get Server Capabilities"""

    def serialize_item(item):
        if isinstance(item, pydantic.BaseModel):
            return item.dict()
        return item

    
    body = None
    

    m = ApiRequest(
        method="GET",
        path="/capabilities".format(
            
        ),
        content_type=None,
        body=body,
        headers=self._only_provided({
        }),
        query_params=self._only_provided({
        }),
        cookies=self._only_provided({
        }),
    )
    return self.make_request({
    
        "200": {
            
                "application/json": Capabilities,
            
        },
    
        "content": {
            
                "default": None,
            
        },
    
        "default": {
            
                "application/json": Error,
            
        },
    
        "description": {
            
                "default": None,
            
        },
    
    }, m)