from logger_setup import logger
from config import DATA_COLLECTION_DURATION_MINUTES
from fetch_prices import fetch_prices_data
from graph_service import generate_price_graph


def main():

    logger.info("Starting Bitcoin Price Tracker application")
    bitcoin_prices_data = fetch_prices_data(DATA_COLLECTION_DURATION_MINUTES)

    if not bitcoin_prices_data:
        logger.error("No price data was collected. Exiting.")
        return

    generate_price_graph(bitcoin_prices_data)



if __name__ == "__main__":
    main()