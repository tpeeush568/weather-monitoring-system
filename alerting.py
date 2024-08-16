import smtplib
import configparser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Access SMTP configuration
SMTP_SERVER = os.getenv('SMTP_SERVER', config.get('smtp', 'smtp_server'))
SMTP_PORT = int(os.getenv('SMTP_PORT', config.get('smtp', 'smtp_port')))
EMAIL_SENDER = os.getenv('EMAIL_SENDER', config.get('smtp', 'email_sender'))
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', config.get('smtp', 'email_password'))

# Access alerting configuration
TEMP_THRESHOLD = float(config.get('alerting', 'temperature_threshold'))
ALERT_RECIPIENTS = [email.strip() for email in config.get('alerting', 'alert_recipients').split(',')]

def send_email(subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            for recipient in ALERT_RECIPIENTS:
                msg['To'] = recipient
                server.sendmail(EMAIL_SENDER, recipient, msg.as_string())
        print("Alert sent successfully.")
    except Exception as e:
        print(f"Failed to send alert. Error: {e}")

# Example call (You should trigger this function based on your application logic)
# send_email("Weather Alert", "Temperature has exceeded the threshold.")
