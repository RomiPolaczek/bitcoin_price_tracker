from email_service import send_max_price_email
from config import DATA_COLLECTION_DURATION_MINUTES
from fetch_prices import fetch_prices_data
from graph_service import generate_price_graph
import logger_setup


def main():
    logger = logger_setup.setup_logging()
    logger.info("Starting bitcoin price tracker application")
    bitcoin_prices_data = fetch_prices_data(DATA_COLLECTION_DURATION_MINUTES)

    if not bitcoin_prices_data:
        logger.error("No price data was collected. Exiting.")
        return

    generate_price_graph(bitcoin_prices_data)
    send_max_price_email(bitcoin_prices_data)

    logger.info("Bitcoin price tracker application finished")


if __name__ == "__main__":
    main()
