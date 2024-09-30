import os
from dotenv import load_dotenv

load_dotenv()

LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "/var/log/syslog")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", "admin@example.com")
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "your-email@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your-email-password")
INTERVAL_MINUTES = os.getenv("INTERVAL_MINUTES", 60)
