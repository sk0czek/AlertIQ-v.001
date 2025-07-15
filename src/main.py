from analyzer import generate_report
from get_orders import fetch_orders_data
from mailer import send_report_email
from datetime import date, timedelta

def main():
    today = date.today()
    klient = ""
    data = fetch_orders_data()
    raport = generate_report(data, today)
    send_report_email(klient, "mail_subject", raport)
    print(raport)

if __name__ == "__main__":
    main()