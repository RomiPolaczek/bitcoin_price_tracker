from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import ticker
from config import GRAPH_PNG_FILE_NAME
import logging

logger = logging.getLogger(__name__)


def generate_price_graph(prices_data):
    try:
        logger.info("Generating price graph")

        price_values = [p["price"] for p in prices_data]
        timestamps = [datetime.fromisoformat(p["timestamp"]) for p in prices_data]

        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, price_values, "b-o")
        plt.ticklabel_format(style="plain", axis="y")

        date = datetime.now().strftime("%d/%m/%Y")
        plt.title(f"Bitcoin Price Tracker {date}")
        plt.xlabel("Time")
        plt.ylabel("Price (USD)")
        plt.grid(True)
        plt.xticks(rotation=45)

        ax = plt.gca()
        ax.yaxis.set_major_formatter(
            ticker.FuncFormatter(lambda x, _: f"{x:,.0f}")
        )  # fix y-axis numbers

        timestamp = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
        plt.tight_layout()
        plt.savefig(f"{GRAPH_PNG_FILE_NAME}_{timestamp}.png")
        logger.info(f"Graph saved")

    except Exception as e:
        logger.error(f"Error generating graph: {str(e)}")
