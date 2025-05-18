import json
import time

from logger_setup import logger
import requests
from config import API, JSON_FILE_NAME


def get_bitcoin_price():
    try:
        logger.info("Requesting Bitcoin price from API")
        response = requests.get(API)

        if response.status_code == 200:
            data = response.json()
            price = float(data['data']['amount'])
            logger.info(f"Bitcoin price: ${price}")
            return price
        else:
            logger.error(f"API request failed: status code: {response.status_code} error detail: {response.json()}")
            return None

    except Exception as e:
        logger.error(f"Exception in getting Bitcoin price: {str(e)}")
        return None


def fetch_prices(duration_minutes):

    logger.info(f"Starting to collect Bitcoin prices for {duration_minutes} minutes")

    prices = []
    for i in range(duration_minutes):
        price = get_bitcoin_price()

        if price is not None:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            prices.append({"timestamp": timestamp,  "price": price})
            logger.info(f"Added price: {timestamp}, ${price}")
            save_to_json_file(prices)

        else:
            logger.warning("Failed to get price")

        time.sleep(60)

    logger.info(f"Completed collection of {len(prices)} bitcoin prices")
    return prices


def save_to_json_file(prices):

    try:
        with open(JSON_FILE_NAME, 'w') as f:
            json.dump(prices, f, indent=4)

        logger.info(f"Saved {len(prices)} prices to {JSON_FILE_NAME}")
    except Exception as e:
        logger.error(f"Error saving to JSON: {str(e)}")
