from logger_setup import logger
from config import DATA_COLLECTION_DURATION_MINUTES
from fetch_prices import fetch_prices


def main():

    logger.info("Starting Bitcoin Price Tracker application")
    bitcoin_prices = fetch_prices(DATA_COLLECTION_DURATION_MINUTES)

    if not bitcoin_prices:
        logger.error("No price data was collected. Exiting.")
        return


if __name__ == "__main__":
    main()