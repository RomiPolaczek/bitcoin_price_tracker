import pytest
from selenium import webdriver
import threading
import time

from config import HOST, PORT
from ui_main import app


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
        "--browser", action="store", default="chrome", help="browser to execute tests (chrome or safari)"
    )


@pytest.fixture(scope="session", autouse=True)
def flask_server():
    def run_server():
        app.run(debug=False,  host=HOST, port=PORT, use_reloader=False)

    # Start server in background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Wait for server to start
    time.sleep(2)
    yield
