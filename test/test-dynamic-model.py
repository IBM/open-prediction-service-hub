#!/usr/bin/env python3
from fastapi.utils import get_model_definitions
from dynamic_hosting.core.model import Parameter


def main():
    print(get_model_definitions(flat_models={Parameter}, model_name_map={Parameter: 'Parameter'}))


if __name__ == '__main__':
    main()
