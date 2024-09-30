from apscheduler.schedulers.background import BackgroundScheduler
from log_fetcher import fetch_filtered_logs
from analyzer import generate_threat_report
from emailer import send_email
import os

def job():
    log_file_path = os.getenv("LOG_FILE_PATH")
    recipient_email = os.getenv("RECIPIENT_EMAIL")
    
    # Fetch logs
    logs = fetch_filtered_logs(log_file_path)
    
    # Generate report
    report = generate_threat_report(logs)
    
    # Send email
    send_email("Scheduled Threat Intelligence Report", report, recipient_email)

def start_scheduler():
    scheduler = BackgroundScheduler()
    interval_minutes = int(os.getenv("INTERVAL_MINUTES", 60))  # Default to 60 mins if not set
    scheduler.add_job(job, 'interval', minutes=interval_minutes)
    scheduler.start()
