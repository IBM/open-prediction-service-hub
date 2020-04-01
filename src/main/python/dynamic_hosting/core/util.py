#!/usr/bin/env python3
import base64
import logging
import os
import pickle
from logging import Logger
from pathlib import Path
from typing import Text, Any, Dict, NoReturn, Type, Union, Set

from dynamic_hosting.openapi.request import RequestBody
from pydantic import BaseModel, create_model

DynamicIOSchemaPrefix = 'Dynamic'

DEFAULT_STORAGE_ROOT_DIR_NAME: Text = 'example_models'
DEFAULT_STORAGE_ROOT: Path = Path(__file__).resolve().parents[5].joinpath(DEFAULT_STORAGE_ROOT_DIR_NAME)


def rmdir(
        directory: Path
) -> None:
    logger: Logger = logging.getLogger(__name__)
    for item in directory.iterdir():
        if item.is_dir():
            rmdir(item)
            logger.info('Removed file: <{item}>'.format(item=item))
        else:
            item.unlink()
    directory.rmdir()
    logger.info('Removed directory: <{directory}>'.format(directory=directory))


def storage_root() -> Path:
    """Find storage root for runtime env"""
    logger: Logger = logging.getLogger(__name__)

    logger.debug('Finding storage root')
    if 'RUNTIME_DIR' not in os.environ:
        logger.debug(
            'RUNTIME_DIR not set, return default storage root: <{storage_root}>'.format(
                storage_root=DEFAULT_STORAGE_ROOT))
        return DEFAULT_STORAGE_ROOT
    else:
        return Path(os.environ['RUNTIME_DIR']).joinpath(DEFAULT_STORAGE_ROOT_DIR_NAME)


def obj_to_base64(obj: Any) -> Text:
    return base64.b64encode(pickle.dumps(obj)).decode('ascii')


def base64_to_obj(serialized: Text) -> Any:
    return pickle.loads(base64.b64decode(serialized))


def load_direct_request_schema(direct_path: Dict, placeholder_name: Text, real_request_name: Text) -> NoReturn:
    schema: Dict = direct_path['post']['requestBody']['content']['application/json']['schema']
    schema['$ref'] = schema['$ref'].replace(placeholder_name, real_request_name)


def replace_any_of_in_response(p: Dict) -> NoReturn:
    schema: Dict = p['post']['responses']['200']['content']['application/json']['schema']
    schema['oneOf'] = schema['anyOf']
    del schema['anyOf']


def replace_any_of(schema: Dict, real_request_name: Text, property_name: Text) -> NoReturn:
    property_map: Dict = schema[real_request_name]['properties'][property_name]
    property_map['oneOf'] = property_map['anyOf']
    del property_map['anyOf']


# Disable type check because this function use dynamic type
# noinspection PyTypeChecker
def get_real_request_class(
        generic_request_class: Type[BaseModel],
        parameter_types: Set[Type[BaseModel]]
) -> Type[RequestBody]:
    return create_model(
        '{prefix}{genetic_class_name}'.format(
            prefix=DynamicIOSchemaPrefix,
            genetic_class_name=generic_request_class.__name__
        ),
        params=(Union[tuple(parameter_types)], ...),
        __base__=generic_request_class
    )
