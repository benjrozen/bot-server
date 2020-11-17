import pytest


def pytest_addoption(parser):
    parser.addoption("--id", action="store")


@pytest.fixture(scope='session')
def id(request):
    id_value = request.config.option.id
    if id_value is None:
        pytest.skip()
    return id_value