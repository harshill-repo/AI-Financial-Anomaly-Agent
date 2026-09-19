import os
import smtplib
import ssl
import datetime
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

with open('output/anomaly_summary.txt', 'r') as f:
    summary_text = f.read()

today = datetime.date.today()
msg = EmailMessage()
msg['Subject'] = f'[Alert] Financial Anomaly Detected on {today}'
msg['From'] = SENDER_EMAIL
msg['To'] = RECEIVER_EMAIL

email_body = f"""Dear Team,

The AI anomaly detection agent has finished its daily run and identified the following unusual financial activity:

{summary_text}

Please check the attached 'anomaly_report.xlsx' for full details.

Regards,
Automated AI Agent
"""
msg.set_content(email_body)

with open('output/anomaly_report.xlsx', 'rb') as f:
    excel_data = f.read()
    msg.add_attachment(excel_data, maintype='application', subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename='anomaly_report.xlsx')

print("Connecting to Gmail server...")
context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
    server.login(SENDER_EMAIL, APP_PASSWORD)
    server.send_message(msg)

print("Success! The AI has officially emailed the report. Go check your inbox!")