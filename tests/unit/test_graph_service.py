from config import GRAPH_PNG_FILE_NAME
from graph_service import generate_price_graph
import glob
import os


def test_generate_price_graph(mock_prices_data):
    generate_price_graph(mock_prices_data)

    files = glob.glob(f"{GRAPH_PNG_FILE_NAME}_*.png")
    assert files, "no graph png file created"

    for file_path in files:
        os.remove(file_path)
