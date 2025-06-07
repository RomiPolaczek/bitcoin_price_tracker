from flask import Flask, render_template, request, redirect, url_for
import threading
from datetime import datetime
from fetch_prices import fetch_prices_data
from graph_service import generate_price_graph
from email_service import send_max_price_email
from config import DATA_COLLECTION_DURATION_MINUTES
import logger_setup

app = Flask(__name__, template_folder='ui', static_folder='ui')

logger = logger_setup.setup_logging()

# Simple global status
is_tracking = False
status_message = "Ready to start tracking"
current_duration = DATA_COLLECTION_DURATION_MINUTES

@app.route('/')
def home():
    global is_tracking, status_message, current_duration
    return render_template('index.html',
                           is_tracking=is_tracking,
                           message=status_message,
                           duration=current_duration)


@app.route('/start', methods=['POST'])
def start_tracking():
    global is_tracking, status_message, current_duration

    if is_tracking:
        status_message = "Already tracking! Please wait..."
        return redirect(url_for('home'))

    duration = int(request.form.get('duration', DATA_COLLECTION_DURATION_MINUTES))
    current_duration = duration  # Remember the chosen duration

    # Update status immediately
    is_tracking = True
    status_message = f"Started tracking for {duration} minutes!"

    def run_tracking():
        global is_tracking, status_message
        try:
            logger.info(f"Tracking started for {duration} minutes")
            prices = fetch_prices_data(duration)

            if prices:
                generate_price_graph(prices)
                send_max_price_email(prices)
                status_message = f"Done! Collected {len(prices)} prices. Check email!"
            else:
                status_message = "Done but no data collected."

        except Exception as e:
            status_message = f"Error: {str(e)}"
            logger.error(f"Tracking error: {str(e)}")
        finally:
            is_tracking = False

    thread = threading.Thread(target=run_tracking)
    thread.daemon = True
    thread.start()

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, port=5001)
