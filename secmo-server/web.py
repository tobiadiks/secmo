from flask import Flask, jsonify, request
from flask_cors import CORS
from scheduler import start_scheduler
from log_fetcher import fetch_filtered_logs
from analyzer import generate_threat_report
from emailer import send_email
import os
import re  # Add this import at the top of the file

app = Flask(__name__)
CORS(app=app)

# Route to view the most recent logs and analysis
@app.route('/logs', methods=['GET'])
def view_logs():
    log_file_path = os.getenv("LOG_FILE_PATH")
    logs = fetch_filtered_logs(log_file_path)
    
    return logs

# Route to manually trigger log analysis
@app.route('/analyze', methods=['POST'])
def trigger_analysis():
    log_file_path = os.getenv("LOG_FILE_PATH")
    logs = fetch_filtered_logs(log_file_path)
    report = generate_threat_report(logs)
    
    # Get recipient email from request body, fallback to env variable
    email = request.json.get("email")
    recipient_email = os.getenv("RECIPIENT_EMAIL")
    
    # Validate email format
    if email and re.match(r"[^@]+@[^@]+\.[^@]+", email) and os.getenv("RESEND_API_KEY"):
        send_email("Manual Log Analysis Report", report, email)
    if recipient_email and re.match(r"[^@]+@[^@]+\.[^@]+", email) and os.getenv("RESEND_API_KEY"):
        send_email("Manual Log Analysis Report", report, recipient_email)
    
    return report
    

# Route to show the status of the scheduler
@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        "status": "Scheduler is running",
        "interval": os.getenv("INTERVAL_MINUTES")
    })

# Run the scheduler in the background
def run_flask_with_scheduler():
    start_scheduler()
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    run_flask_with_scheduler()
