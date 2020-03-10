from typing import Any, Union


def main():

    x = Union[Union[int, str], Union[float, object]]

    y = Union[(str, int)]

    print(x)

    print(y)


if __name__ == '__main__':
    main()