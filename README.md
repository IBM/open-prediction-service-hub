# Decision automation on machine learning

[![Build Status](https://travis.ibm.com/dba/ads-ml-service.svg?token=1gxxdyFN2gDs6CM3JxPc&branch=dev)](https://travis.ibm.com/dba/ads-ml-service)


## Usage

To clone the project 
```shell script
git clone --recurse-submodules git@github.ibm.com:dba/ads-ml-service.git ads-ml-service
```

To build the microservice image
```shell script
docker build -t embedded_ml .
```

To test the microservice
```shell script
docker run --rm -it -p 8080:8080 --name lml embedded_ml
```
Your predictive service is then ready at `http://localhost:8080/v1` and 
its openapi docs is available at `http://localhost:8080/v1/docs`.



### Configuration example for miniloan fraud detection

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

`metadata` needs to have `description`, `trained_at`, `author` and associated `metrics`.

`class_names` is optional. It is a lookup table defined as class index <-> class name.
It is used in classifications when the output relies on class index.

Note: json does not support int as mapping key. For this reason,
in the example we used `"0"` and `"1"` instead of `0` and `1`.


### Example for model invocation

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

`model_name` and `model_version`are used to uniquely identify ml models. 
Parameters of ml models are arranged in key-values pairs.

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


## Dependencies
* Dependencies for web service: `requirements.txt`
* Dependencies for ML model: `requirements-ml.txt`

Before adding new models, make sure that `requirements-ml.txt` already contains
all necessary dependencies.


## Model creation examples
[model creation](examples/model_training_and_deployment/README.md)
