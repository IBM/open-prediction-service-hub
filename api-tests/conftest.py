# content of conftest.py
import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--url", action="store", default="http://localhost:8080/v1/", help="service URL"
    )


@pytest.fixture
def url(request):
    return request.config.getoption("--url")