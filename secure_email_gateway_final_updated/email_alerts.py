import smtplib
from email.message import EmailMessage
from config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASS, ALERT_RECIPIENT

def send_alert(user_email, infected_file):
    subject = f"ALERT: Infected file detected in {user_email}"
    body = f"""
Dear Admin,

An infected file was detected in {user_email}:
- {infected_file}

Please review the scan report for details:
./reports/report.html

Best Regards,
Secure Email Gateway
    """.strip()

    msg = EmailMessage()
    msg['From'] = SMTP_USER
    msg['To'] = '228r1a62j0@cmrec.ac.in' # Always send to 228r1a62j0@cmrec.ac.in
    msg['Subject'] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        print(f"✅ Alert sent to {ALERT_RECIPIENT}")
    except Exception as e:
        print(f"❌ Failed to send alert: {e}")
