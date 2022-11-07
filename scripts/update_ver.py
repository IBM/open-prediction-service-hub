#!/usr/bin/env python3

import argparse
import pathlib
import re

OFFICIAL_SEMANTIC_VERSIONING_REGEX_CONTENT = '(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?'
OFFICIAL_SEMANTIC_VERSIONING_REGEX = '^' + OFFICIAL_SEMANTIC_VERSIONING_REGEX_CONTENT + '$'

ROOT = pathlib.Path(__file__).resolve().parent / '..'

OPS_SPEC_PATH = ROOT / 'open-prediction-service.yaml'
JAVA_SDK_POM_PATH = ROOT / 'ops-client-sdk' / 'pom.xml'
OPS_IMPLS_POM_PATH = ROOT / 'ops-implementations' / 'pom.xml'
IMPL_ADS_ML_SERVICE_POM_PATH = ROOT / 'ops-implementations' / 'ads-ml-service' / 'pom.xml'
IMPL_SAGEMAKER_POM_PATH = ROOT / 'ops-implementations' / 'sagemaker-service' / 'pom.xml'
IMPL_WML_POM_PATH = ROOT / 'ops-implementations' / 'wml-service' / 'pom.xml'
IMPL_ADS_ML_SERVICE_VER_PATH = ROOT / 'ops-implementations' / 'ads-ml-service' / 'app' / 'version.py'
IMPL_SAGEMAKER_VER_PATH = ROOT / 'ops-implementations' / 'sagemaker-service' / 'openapi_server' / 'version.py'
IMPL_WML_VER_PATH = ROOT / 'ops-implementations' / 'wml-service' / 'swagger_server' / 'version.py'


def main():
    parser = argparse.ArgumentParser('Update all version strings')
    parser.add_argument('ver', help='New version of the project', type=str)
    args = parser.parse_args()

    new_ver = args.ver
    if not re.match(OFFICIAL_SEMANTIC_VERSIONING_REGEX, new_ver):
        raise ValueError

    OPS_SPEC_PATH.write_text(re.sub(
        f'version: {OFFICIAL_SEMANTIC_VERSIONING_REGEX_CONTENT}',
        f'version: {new_ver}',
        OPS_SPEC_PATH.read_text(),
        count=1,
        flags=re.M))

    JAVA_SDK_POM_PATH.write_text(re.sub(
        f'<version>{OFFICIAL_SEMANTIC_VERSIONING_REGEX_CONTENT}</version>',
        f'<version>{new_ver}</version>',
        JAVA_SDK_POM_PATH.read_text(),
        count=1,
        flags=re.M))

    OPS_IMPLS_POM_PATH.write_text(re.sub(
        f'<version>{OFFICIAL_SEMANTIC_VERSIONING_REGEX_CONTENT}</version>',
        f'<version>{new_ver}</version>',
        OPS_IMPLS_POM_PATH.read_text(),
        count=1,
        flags=re.M))

    IMPL_ADS_ML_SERVICE_POM_PATH.write_text(re.sub(
        f'<version>{OFFICIAL_SEMANTIC_VERSIONING_REGEX_CONTENT}</version>',
        f'<version>{new_ver}</version>',
        IMPL_ADS_ML_SERVICE_POM_PATH.read_text(),
        count=1,
        flags=re.M))

    IMPL_SAGEMAKER_POM_PATH.write_text(re.sub(
        f'<version>{OFFICIAL_SEMANTIC_VERSIONING_REGEX_CONTENT}</version>',
        f'<version>{new_ver}</version>',
        IMPL_SAGEMAKER_POM_PATH.read_text(),
        count=1,
        flags=re.M))

    IMPL_WML_POM_PATH.write_text(re.sub(
        f'<version>{OFFICIAL_SEMANTIC_VERSIONING_REGEX_CONTENT}</version>',
        f'<version>{new_ver}</version>',
        IMPL_WML_POM_PATH.read_text(),
        count=1,
        flags=re.M))

    IMPL_ADS_ML_SERVICE_VER_PATH.write_text(re.sub(
        f'__version__ = \'{OFFICIAL_SEMANTIC_VERSIONING_REGEX_CONTENT}\'',
        f'__version__ = \'{new_ver}\'',
        IMPL_ADS_ML_SERVICE_VER_PATH.read_text(),
        count=1,
        flags=re.M))

    IMPL_SAGEMAKER_VER_PATH.write_text(re.sub(
        f'__version__ = \'{OFFICIAL_SEMANTIC_VERSIONING_REGEX_CONTENT}\'',
        f'__version__ = \'{new_ver}\'',
        IMPL_SAGEMAKER_VER_PATH.read_text(),
        count=1,
        flags=re.M))

    IMPL_WML_VER_PATH.write_text(re.sub(
        f'__version__ = \'{OFFICIAL_SEMANTIC_VERSIONING_REGEX_CONTENT}\'',
        f'__version__ = \'{new_ver}\'',
        IMPL_WML_VER_PATH.read_text(),
        count=1,
        flags=re.M))


if __name__ == '__main__':
    main()
