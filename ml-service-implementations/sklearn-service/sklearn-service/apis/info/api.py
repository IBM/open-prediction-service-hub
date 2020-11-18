from __future__ import annotations

from swagger_codegen.api.base import BaseApi

from . import get_capabilities
from . import get_info
class InfoApi(BaseApi):
    get_capabilities = get_capabilities.make_request
    get_info = get_info.make_request