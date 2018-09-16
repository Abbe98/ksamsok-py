import pytest

def pytest_addoption(parser):
    parser.addoption("--offline", action="store_true",
                     default=False, help="skip tests requiring an internet connection")

def pytest_collection_modifyitems(config, items):
    if config.getoption("--offline"):
        offline = pytest.mark.skip(reason="offline argument given")
        for item in items:
            if "online" in item.keywords:
                item.add_marker(offline)
