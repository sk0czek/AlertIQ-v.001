import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_LOGIN = os.getenv("SMTP_LOGIN")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM")

def convert_text_to_html(text):
    return f"""<html>
    <body>
    <pre style="font-family: Consolas, monospace; font-size: 14px;">
{text}
    </pre>
    </body>
</html>"""


def send_report_email(to_email, subject, body):
    if not all([SMTP_SERVER, SMTP_PORT, SMTP_LOGIN, SMTP_PASSWORD, EMAIL_FROM]):
        raise ValueError("Brakuje danych SMTP - sprawdz plik .env")
    
    msg = MIMEMultipart("alternative")
    msg["From"] = EMAIL_FROM
    msg["To"] = to_email
    msg["Subject"] = subject

    html_body = convert_text_to_html(body)
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_LOGIN, SMTP_PASSWORD)
            server.send_message(msg)
        print(f"📧 Email wysłany do: {to_email}")
    except Exception as e:
        print(f"❌ Błąd podczas wysyłania emaila: {e}")