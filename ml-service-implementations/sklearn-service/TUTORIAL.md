# Tutorial

Stp by step guide to create this server

## Generate server source code from OpenAPI

There is a maven command to execute swagger code generation:

`mvn -P generate generate-source`

## Correct generated code

At the time of writing, the openapi code generator doesn't correctly support anyOf. While waiting for the a bug fix, we suggest the following workaround:

Remove imports in `openapi_server/models/parameter.py`

```python
from openapi_server.models.any_ofintegernumberstringboolean import AnyOfintegernumberstringboolean
```

Add instead

```python
from openapi_server.models.check_and_get_type import check_and_get_type
```

Replace `AnyOfintegernumberstringboolean` type by `check_and_get_type('Parameter.value',int,float,str,bool)`

In the automatically generated file `openapi_server/util.py`, add Line 18:

```    try:
        if klass.__name__=='_check_and_get_type':
            klass=klass(data)
    except AttributeError:
        pass
```

Finally copy and paste `openapi_server/models/check_and_get_type.py` to your model folder.

This suggested workaround has been applied in this ops server, please feel to read source code in doubt.

## Model change

Except the workaround described above, to support anyOf, no model has been changed.

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

## Update the discover controller

The discover controller gathers, at server initilization, the available models in the server.

This is implemented in `openserver/controllers/helper.py` where the `supported_models` list gathers all the directories with a `model.pkl`

The discover controller, in this example's implementation,  serves the endpoints and models requests based on the data available in the file `deployment_conf.json` that is in the same directory as the `model.pkl`.

## Update the run controller

The run controller has been modified, the function `prediction` in `openapi_server\controllers\run_controller.py` has been updated to take the argument `body` instead of the default `prediction` that doesn't work.

The run controller simply executes the pickle file `model.pkl` of the model requested by the client with the supplied arguments
