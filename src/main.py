from analyzer import generate_report
from get_orders import fetch_orders_data
from datetime import date

def main():
    today = date.today()
    data = fetch_orders_data()
    generate_report(data, today)


if __name__ == "__main__":
    main()