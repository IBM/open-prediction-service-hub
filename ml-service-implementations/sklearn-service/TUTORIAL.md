# Tutorial

Stp by step guide to create this server

## Generate server source code from OpenAPI

There is a maven command to execute swagger code generation:

`mvn generate-source`

## Correct generated code

Remove imports in `openapi_server/models/parameter.py`

```python
from openapi_server.models.any_ofintegernumberstringboolean import AnyOfintegernumberstringboolean
```

Add instead

```python
from typing import Union
```

Replace `AnyOfintegernumberstringboolean` type by `Union(int,float,bool,str)`

## Update the info controller

Add import Capability
in `get_capabilities()` replace `return 'do some magic!'` by

```python
   return Capabilities([Capability.INFO, Capability.DISCOVER, Capability.RUN])
```

in `get_info()` replace `return 'do some magic!'` by

```python
    info = dict(
        description='Open Prediction Service for Scikit Learn models based on OPSv2 API'
    )
    return ServerInfo(status='ok', info=info)
```

## Add model support

TBC
