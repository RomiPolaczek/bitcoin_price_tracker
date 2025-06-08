import time
from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from config import URL

pytestmark = pytest.mark.ui


def test_page_loads_successfully(driver):
    driver.get(URL)

    header_locator = driver.find_element(By.TAG_NAME, "h1")
    header_text = header_locator.text
    assert header_text == "Bitcoin Price Tracker"

    heading = driver.find_element(By.TAG_NAME, "h1")
    assert heading.text == "Bitcoin Price Tracker"


def test_page_elements_display(driver):
    driver.get(URL)

    start_tracking_header = driver.find_element(By.XPATH, "//h2[text()='Start Tracking']")
    assert start_tracking_header.is_displayed()

    duration_input_locator = driver.find_element(By.ID, "duration")
    assert duration_input_locator.is_displayed()

    submit_button_locator = driver.find_element(By.ID, "submit_duration")
    assert submit_button_locator.is_displayed()
    assert submit_button_locator.text == "Start Tracking"

    duration_min_locator = driver.find_element(By.ID, "duration_min_label")
    assert duration_min_locator.text == "Duration (minutes):"

    how_it_works_header = driver.find_element(By.XPATH, "//h2[text()='How it works']")
    assert how_it_works_header.is_displayed()


def test_form_submission_with_duration(driver):
    driver.get(URL)

    duration_input_locator = driver.find_element(By.ID, "duration")
    duration_input_locator.clear()
    duration_input_locator.send_keys("2")

    submit_button_locator = driver.find_element(By.ID, "submit_duration")
    submit_button_locator.click()

    wait = WebDriverWait(driver, 10)
    success_msg_element = wait.until(ec.presence_of_element_located((By.ID, "flash_message")))
    assert success_msg_element.is_displayed()
    assert success_msg_element.text == "Bitcoin tracking started! Running for 2 minutes."


# @patch('ui_main.fetch_prices_data')
# def test_form_submission_with_duration_error(mock_fetch, driver):
#     mock_fetch.return_value = []
#
#     driver.get(URL)
#
#     duration_input_locator = driver.find_element(By.ID, "duration")
#     duration_input_locator.clear()
#     duration_input_locator.send_keys("2")
#
#     submit_button = driver.find_element(By.ID, "submit_duration")
#     submit_button.click()
#
#     wait = WebDriverWait(driver, 10)
#     success_msg_element = wait.until(ec.presence_of_element_located((By.ID, "flash_message")))
#     assert success_msg_element.is_displayed()
#     assert success_msg_element.text == "Bitcoin tracking started! Running for 2 minutes."
#
#     # Wait for background thread to complete - could use polling instead
#     time.sleep(5)  # Increase to 3 seconds to be safer
#
#     # Refresh to see completion message
#     driver.refresh()
#
#     # Should show error completion message
#     error_msg = wait.until(ec.presence_of_element_located((By.ID, "flash_message")))
#     assert "no price data was collected" in error_msg.text.lower()
