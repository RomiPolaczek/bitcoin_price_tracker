import smtplib
import os
from logger_setup import logger
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_EMAIL_PASSWORD = os.getenv("SENDER_EMAIL_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")


def send_max_price_email(prices_data):

    try:
        logger.info("Preparing email...")

        max_price_data = max(prices_data, key=lambda x: x["price"])
        max_price_value = max_price_data["price"]
        max_price_time = max_price_data["timestamp"]

        logger.info(f"The Maximum Price is ${max_price_value:,.2f} USD")

        body = f"""        
               The maximum price in the last hour: ${max_price_value:,.2f} USD
               Recorded at: {max_price_time}
               """

        msg = MIMEText(body)
        msg['Subject'] = 'Bitcoin Price Report - Maximum Price'
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_EMAIL_PASSWORD)
            server.send_message(msg)

        logger.info(f"Email sent successfully")
        return True

    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        return False
