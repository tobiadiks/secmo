import os
import resend  # Import Resend SDK

def send_email(subject, body, to_email):
    """
    Sends an email to the specified recipient using Resend SDK.
    """
    
    resend.api_key =os.getenv("RESEND_API_KEY") # Initialize Resend with API key

    try:

        params: resend.Emails.SendParams = {
        "from": "Secmo <secmo@salespadi.store>",
        "to": [to_email],
        "subject": subject,
        "html": body,
        }
        email = resend.Emails.send(params)
        print(email)   
    except Exception as e:
        print(f"Failed to send email: {e}")
