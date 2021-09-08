#!/usr/bin/env python3

import pathlib

import lxml.etree
import yaml

ROOT = pathlib.Path(__file__).parents[1]
OPS_SPEC_PATH = ROOT.joinpath('open-prediction-service.yaml')
JAVA_SDK_POM_PATH = ROOT.joinpath('ops-client-sdk', 'pom.xml')
OPS_IMPLS_POM_PATH = ROOT.joinpath('ops-implementations', 'pom.xml')
IMPL_ADS_ML_SERVICE_POM_PATH = ROOT.joinpath('ops-implementations', 'ads-ml-service', 'pom.xml')
IMPL_SAGEMAKER_POM_PATH = ROOT.joinpath('ops-implementations', 'sagemaker-service', 'pom.xml')
IMPL_WML_POM_PATH = ROOT.joinpath('ops-implementations', 'wml-service', 'pom.xml')


def get_openapi_info_ver(openapi_spec_path: pathlib.Path):
    contents = yaml.safe_load(openapi_spec_path.read_text())
    return contents['info']['version']


def get_pom_ver(pom_path: pathlib.Path):
    root = lxml.etree.fromstring(pom_path.read_bytes())

    namesp = root.tag.replace('project', '')  # get the namesapce from the root key
    version = root.find(namesp + 'version')

    if version is None:
        return root.find(namesp + 'parent').find(namesp + 'version').text
    return version.text


def main():
    versions = [
        get_openapi_info_ver(OPS_SPEC_PATH),
        get_pom_ver(JAVA_SDK_POM_PATH),
        get_pom_ver(OPS_IMPLS_POM_PATH),
        get_pom_ver(IMPL_ADS_ML_SERVICE_POM_PATH),
        get_pom_ver(IMPL_SAGEMAKER_POM_PATH),
        get_pom_ver(IMPL_WML_POM_PATH)
    ]

    if not versions.count(versions[0]) == len(versions):
        print('{file}: {ver}'.format(file=OPS_SPEC_PATH.__str__(), ver=get_openapi_info_ver(OPS_SPEC_PATH)))
        print('{file}: {ver}'.format(file=JAVA_SDK_POM_PATH.__str__(), ver=get_pom_ver(JAVA_SDK_POM_PATH)))
        print('{file}: {ver}'.format(file=OPS_IMPLS_POM_PATH.__str__(), ver=get_pom_ver(OPS_IMPLS_POM_PATH)))
        print('{file}: {ver}'.format(file=IMPL_ADS_ML_SERVICE_POM_PATH.__str__(), ver=get_pom_ver(IMPL_ADS_ML_SERVICE_POM_PATH)))
        print('{file}: {ver}'.format(file=IMPL_SAGEMAKER_POM_PATH.__str__(), ver=get_pom_ver(IMPL_SAGEMAKER_POM_PATH)))
        print('{file}: {ver}'.format(file=IMPL_WML_POM_PATH.__str__(), ver=get_pom_ver(IMPL_WML_POM_PATH)))
        raise ValueError('Versions are not synchronized')


if __name__ == '__main__':
    main()
