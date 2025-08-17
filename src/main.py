from analyzer import generate_report
from get_orders import fetch_orders_data
from mailer import send_report_email
from datetime import timedelta, date

def main():
    today = date.today()
    klient = ""
    data = fetch_orders_data()
    raport = generate_report(data, today)
    subject = f"AlertIQ – Raport Dzienny {today.strftime('%d.%m.%Y') }"
    send_report_email(klient, subject, raport)

if __name__ == "__main__":
    main()