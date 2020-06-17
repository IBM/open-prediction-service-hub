# OPS with scikit and xgboost sample
Add short description

1. [Getting Started](#getting-started)
2. [Open Prediction Service](#open-prediction-service)
3. [Additional Dependencies](#additional-dependencies)
4. [Model Examples](#model-examples)

## Getting Started

### Prerequisites

Docker ?

### Run the microservice
To build the microservice image

```sh
docker build -t open-prediction-service
```

To run the microservice

```sh
docker run --rm -it -p 8080:8080 --name open-prediction-service open-prediction-service
```

To check that you have a running container
```sh
docker ps open-prediction-service
```

Your predictive service is then ready at [http://localhost:8080/v1](http://localhost:8080/v1).

Swagger UI documentation is available at [http://localhost:8080/v1/docs](http://localhost:8080/v1/docs).

### Stop the microservice
To stop the container
```sh
docker stop open-prediction-service
```

## Open Prediction Service

Different endpoints are available and documented at [http://localhost:8080/v1/docs](http://localhost:8080/v1/docs).

TODO ADD SCREENSHOTS

For example you can list all added models by running:
```sh
curl -X GET "http://localhost:8080/v1/models" -H "accept: application/json"
```

### Adding a model - POST /v1/models

The request body of the adding model request is an archive pickle file.

Structure of archive file:
```
<archive-file-name>.pkl
    └── Dict
        ├── 'model': ml_model
        └── 'model_config': configuration
```
where:
- `ml_model`: trained python class model to be added
- `configuration`: json object with the below structure
```
└── Dict
    ├── 'name': 'model name'     // name & version uniquely define model
    ├── 'version': 'v0'          // name & version uniquely define model
    ├── 'method_name': 'predict' // method name to be called for predictions
    ├── 'input_schema'           // input features schema
        └── Array
            └── Dict
                ├── 'name'
                ├── 'order'
                └── 'type'
    ├── 'output_schema':        // output format of most common use cases
        └── Dict
            ├── 'attributes'
                └── Array
                    └── Dict
                        ├── 'name'
                        └── 'type'
    └── 'metadata':
        └── Dict
            ├── 'description': 'model description'
            ├── 'author': 'model author'
            ├── 'trained_at': '2020-03-17 13:25:23'
            ├── 'class_names':              // OPTIONAL
                └── Dict                    // classification labels
                        ├── '0': 'label_0'  // "VALUE": "LABEL"
                        └── '1': 'label_1'
            └── 'metrics':
                └── Array
                    └── Dict
                        ├── 'name'
                        └── 'value'
            
```
#### Available Output formats


<table>
    <tr>
        <th>output type</th>
        <th>format</th>
        <th>
            corresponding output 
            example
        </th>
    </tr>
<tr>
<td>
regression
</td>
<td>
<pre lang="json">
[
    {
        "name": "prediction",
        "type": "float"
    }
]
</pre>
</td>
<td>
<pre lang="json">
{
  "prediction": 128.0
}
</pre>
</tr>
<tr>
<td>
classification
</td>
<td>
<pre lang="json">
[
    {
        "name": "prediction",
        "type": "string"
    }
]
</pre>
</td>
<td>
<pre lang="json">
{
  "prediction": "true"
}
</pre>
</tr>
<tr>
<td>
classification
with probabilities
</td>
<td>
<pre lang="json">
[
    {
        "name": "prediction",
        "type": "string"
    },
    {
        "name": "probabilities",
        "type": "[Probability]"
    }
]
</pre>
</td>
<td>
<pre lang="json">
{
    "prediction": "true",
    "probabilities": [
        {
          "class_name": "true",
          "class_index": 1,
          "value": 0.66
        },
        {
          "class_name": "false",
          "class_index": 0,
          "value": 0.34
        }
    ]
}
</pre>
</tr>
</table>


#### Configuration example for miniloan fraud detection

```json
{
  "name": "miniloan-rfc",
  "version": "v0",
  "method_name": "predict",
  "input_schema": [
    {
      "name": "creditScore",
      "order": 0,
      "type": "float64"
    },
    {
      "name": "income",
      "order": 1,
      "type": "float64"
    },
    {
      "name": "loanAmount",
      "order": 2,
      "type": "float64"
    },
    {
      "name": "monthDuration",
      "order": 3,
      "type": "float64"
    },
    {
      "name": "rate",
      "order": 4,
      "type": "float64"
    }
  ],
  "output_schema": {
        "attributes": [
            {
                "name": "prediction",
                "type": "string"
            },
            {
                "name": "probabilities",
                "type": "[Probability]"
            }
        ]
  },
  "metadata": {
    "description": "Loan payment classification",
    "author": "Somebody",
    "trained_at": "2020-03-17 13:25:23",
    "class_names": {
      "0": "false",
      "1": "true"
    },
    "metrics": [
      {
        "name":  "accuracy",
        "value": 0.9471577261809447
      }
    ]
  }
}
```

ML model is uniquely identified by its `name` and its `version`.

ML models are python classes. Local provider needs to know the `method_name` of prediction method.

`input_schema` is used as lookup table which local provider use to find type/position of
each feature. `type` needs to be a type alias in `numpy`module.

`output_schema` configures result formats for the most common use cases.

`metadata` needs to have `description`, `trained_at`, `author` and associated `metrics`.

`class_names` is optional. It is a lookup table defined as class index <-> class name.
It is used in classifications when the output relies on class index.

Note: json does not support int as mapping key. For this reason,
in the example we used `"0"` and `"1"` instead of `0` and `1`.


### Invoking a model - POST /v1/invocations

The request body of the adding model request is a JSON object with the following structure.
```
└── Dict
    ├── 'model_name': 'model name'     // name & version uniquely define model
    ├── 'model_version': 'v0'          // name & version uniquely define model
    └── 'params'                       // input features names and values
        └── Array
            └── Dict
                ├── 'name'
                └── 'value'  
```

#### Example of model invocation

Request body
```json
{
  "model_name": "miniloan-rfc",
  "model_version": "v0",
  "params": [
        {
            "name": "creditScore",
            "value": 400
        }, {
            "name": "income",
            "value": 45000
        }, {
            "name": "loanAmount",
            "value": 100000
        }, {
            "name": "monthDuration",
            "value": 24
        }, {
            "name": "rate",
            "value": 2.0
        }
    ]
}
```

Response body may look like:
```json
{
    "prediction": "true",
    "probabilities": [
        {
          "class_name": "true",
          "class_index": 1,
          "value": 0.66
        },
        {
          "class_name": "false",
          "class_index": 0,
          "value": 0.34
        }
    ]   
}
```


## Additional Dependencies
* Dependencies for web service: `requirements.txt`
* Dependencies for ML model: `requirements-ml.txt`

Before adding new models, make sure that `requirements-ml.txt` already contains
all necessary dependencies.

If new dependencies are added, you need to stop the running container and build the image again (see [Getting Started section](#getting-started))


## Model Examples

You can find examples of models ready to be added to your OPS instance in 
[examples/model_training_and_deployment/](examples/model_training_and_deployment/README.md) folder.
