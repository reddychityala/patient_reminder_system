# src/notification_utils.py
import smtplib
from email.mime.text import MIMEText

def send_email_alert(subject, body, to_email):
    sender = "noreply@example.com"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to_email
    try:
        # mock connection (no auth)
        print(f"Mock email sent to {to_email}: {subject}")
    except Exception as e:
        print("Email send failed:", e)
