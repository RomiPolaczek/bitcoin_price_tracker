from flask import Flask, render_template, request, redirect, url_for, flash, session
import threading
from fetch_prices import fetch_prices_data
from graph_service import generate_price_graph
from email_service import send_max_price_email
from config import DATA_COLLECTION_DURATION_MINUTES, HOST, PORT
import logger_setup

app = Flask(__name__, template_folder='ui', static_folder='ui')
app.secret_key = 'bitcoin_tracker_2025'

logger = logger_setup.setup_logging()

completion_status = None
tracking_active = False


@app.route('/')
def home():
    global completion_status, tracking_active

    # Show completion message if available
    if completion_status:
        flash(completion_status, 'info')
        completion_status = None  # Clear it after showing

    # Get the last used duration from session, default to config value
    last_duration = session.get('last_duration', DATA_COLLECTION_DURATION_MINUTES)
    return render_template('index.html', last_duration=last_duration, tracking_active=tracking_active)


@app.route('/start', methods=['POST'])
def start_tracking():
    global completion_status, tracking_active

    duration = int(request.form.get('duration', DATA_COLLECTION_DURATION_MINUTES))

    # Save duration in session so form remembers it
    session['last_duration'] = duration

    # Show immediate message
    flash(f'Bitcoin tracking started! Running for {duration} minutes.', 'success')

    # Clear any previous completion status and set tracking active
    completion_status = None
    tracking_active = True

    # Start tracking in background
    def run_tracking():
        global completion_status, tracking_active
        try:
            logger.info(f"Tracking started for {duration} minutes")
            prices = fetch_prices_data(duration)

            if prices:
                generate_price_graph(prices)
                send_max_price_email(prices)
                logger.info(f'Completed! Collected {len(prices)} prices.')
                completion_status = f'Tracking completed! Collected {len(prices)} price points. Check your email!'
            else:
                logger.warning('No price data collected.')
                completion_status = 'Tracking completed but no price data was collected.'

        except Exception as e:
            logger.error(f"Tracking error: {str(e)}")
            completion_status = f'Tracking failed: {str(e)}'
        finally:
            tracking_active = False

    thread = threading.Thread(target=run_tracking)
    thread.daemon = True
    thread.start()

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)
