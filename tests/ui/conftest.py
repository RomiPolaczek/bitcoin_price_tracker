import pytest
from selenium import webdriver


@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser").lower()
    print(f"Creating {browser} driver")
    if browser == "chrome":
        my_driver = webdriver.Chrome()
    elif browser == "safari":
        my_driver = webdriver.Safari()
    else:
        raise TypeError(f"Expected 'chrome' or 'safari', but got {browser}")
    yield my_driver
    print(f"Closing {browser} driver")
    my_driver.quit()


def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome", help="browser to execute tests (chrome or firefox)"
    )
