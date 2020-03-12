from typing import Any, Union

from pydantic import BaseModel


class A(BaseModel):
    a: int


class B(BaseModel):
    b: str


def main():

    x = B

    b1 = B(a=1, b='a')
    b2 = x(a=1, b='a')

    print(b1 == b2)
    print(type(x))

    x = Union[Union[int, str], Union[float, object]]

    y = Union[(str, int)]

    print(x)

    print(y)


if __name__ == '__main__':
    main()