import datetime

with open('output/anomaly_summary.txt', 'r') as f:
    summary_text = f.read()

today = datetime.date.today()
email_content = f"""Subject: [Alert] Financial Anomaly Detected on {today}
To: finance-team@company.com
From: AI Anomaly Agent

Dear Team,

The AI anomaly detection agent has finished its daily run and identified the following unusual financial activity:

{summary_text}
Please check the attached 'anomaly_report.xlsx' and 'anomaly_dashboard.png' for full details.

Regards,
Automated AI Agent
"""

with open('output/sample_email.txt', 'w') as f:
    f.write(email_content)

print("Email Draft Complete! The project pipeline is officially finished. Check the output folder for sample_email.txt.")