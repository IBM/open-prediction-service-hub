#!/usr/bin/env python3
#
# Copyright 2020 IBM
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.IBM Confidential
#


import enum
import typing
import typing_extensions
import datetime as dt

import numpy
import pydantic as pydt

import app.core.uri as app_uri
import app.gen.schemas.ops_schemas as ops_schemas
import app.models as models


class FeatureImpl(ops_schemas.Feature):
    """
    Feature of machine learning model
    :param name: name of the feature
    :param order: the position of the feature in method signature
    :param type: type of feature. Can be python type or numpy type
    """
    name: typing.Text = pydt.Field(..., description='Feature name')
    order: int = pydt.Field(..., description='Position of feature')
    type: typing.Text = pydt.Field(..., description='Numpy type of feature')

    class Config:
        """Feature is immutable inside model"""
        allow_mutation: bool = False

    @pydt.validator('type')
    def type_check(cls, t) -> typing.Type:
        if t in ('int', 'float', 'bool', 'str', 'string'):  # Python type
            return t
        elif hasattr(numpy, t) and numpy.issubdtype(getattr(numpy, t), numpy.generic):
            return t
        else:
            raise ValueError('Type not supported: {t}'.format(t=t))


class ModelCreateImpl(ops_schemas.ModelCreation):
    version: typing.Optional[str] = pydt.Field('v1', description='version of the model')
    input_schema: typing.Optional[typing.List[FeatureImpl]] = pydt.Field(None, )


class ModelUpdateImpl(ops_schemas.ModelUpdate):
    input_schema: typing.Optional[typing.List[FeatureImpl]] = pydt.Field(None, )


class ModelImpl(ops_schemas.Model):
    """Model independent information"""
    input_schema: typing.Optional[typing.List[FeatureImpl]] = pydt.Field(None, description='Input schema of ml model')

    @staticmethod
    def from_database(db_obj: models.Model) -> typing.Dict[typing.Text, typing.Any]:
        return {
            'id': db_obj.id,
            'created_at': db_obj.created_at.astimezone(dt.timezone.utc).isoformat(),
            'modified_at': db_obj.modified_at.astimezone(dt.timezone.utc).isoformat(),
            **db_obj.config.configuration,
            'links': [
                {
                    'rel': 'self',
                    'href': app_uri.TEMPLATE.format(resource_type='models', resource_id=db_obj.id)
                }
                ,
                {
                    'rel': 'endpoint',
                    'href': app_uri.TEMPLATE.format(resource_type='endpoints', resource_id=db_obj.endpoint.id)
                }

            ] if db_obj.endpoint is not None else [
                {
                    'rel': 'self',
                    'href': app_uri.TEMPLATE.format(resource_type='models', resource_id=db_obj.id)
                }
            ]
        }


class ModelsImpl(ops_schemas.Models):
    models: typing.Optional[typing.List[ModelImpl]] = pydt.Field(None, description='List of models')


class EndpointImpl(ops_schemas.Endpoint):
    @staticmethod
    def from_database(e: models.Endpoint) -> typing.Dict[typing.Text, typing.Any]:
        metadata = e.metadata_
        return {
            'id': e.id,
            'name': e.name,
            'deployed_at': e.deployed_at.astimezone(dt.timezone.utc).isoformat(),
            'status': StatusImpl.in_service if e.binary else StatusImpl.creating,
            'metadata': metadata,
            'links': [
                {
                    'rel': 'self',
                    'href': app_uri.TEMPLATE.format(resource_type='endpoints', resource_id=e.id)
                },
                {
                    'rel': 'model',
                    'href': app_uri.TEMPLATE.format(resource_type='models', resource_id=e.id)
                }

            ]
        }


class EndpointsImpl(ops_schemas.Endpoints):
    pass


class StatusImpl(typing.Text, enum.Enum):
    out_of_service = 'out_of_service'
    creating = 'creating'
    updating = 'updating'
    under_maintenance = 'under_maintenance'
    rolling_back = 'rolling_back'
    in_service = 'in_service'
    deleting = 'deleting'
    failed = 'failed'


class ParameterImpl(pydt.BaseModel):
    name: str = pydt.Field(..., description='Name of the feature', title='Name')
    value: typing.Any = pydt.Field(
        ..., description='Value of the feature', title='Value'
    )

    @pydt.validator('value')
    def value_check(cls, v) -> typing.Any:
        if isinstance(v, (int, float, bool, str)):  # Python type
            return v
        else:
            raise ValueError(f'Value not supported: {v}')


class PredictionImpl(pydt.BaseModel):
    target: typing.List[ops_schemas.Link] = pydt.Field(
        ...,
        description='Add at least a relation to an `endpoint`to be able to call the correct prediction. Eventually add '
                    'also a `model` in case endpoints contains multiple models.',
    )
    parameters: typing.List[typing.Union[typing.List[ParameterImpl], ParameterImpl]] = pydt.Field(
        ..., description='Model parameters', title='Parameters'
    )


class AdditionalPMMLModelInfo(pydt.BaseModel):
    modelType: typing.Literal['pmml']
    modelSubType: str


class AdditionalPickleModelInfo(pydt.BaseModel):
    modelType: typing.Literal['pickle']
    pickleProtoVersion: str


class AdditionalOtherModelInfo(pydt.BaseModel):
    modelType: typing.Literal['other']


AdditionalModelInfo = typing_extensions.Annotated[
    typing.Union[AdditionalPMMLModelInfo, AdditionalPickleModelInfo, AdditionalOtherModelInfo], pydt.Field(discriminator='modelType')]
