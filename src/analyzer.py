from datetime import datetime, timedelta
from collections import defaultdict

def sum_sales_by_product(data, target_date):
    result = defaultdict(int)
    for row in data:
        if row['data'] == target_date:
            result[row['produkt']] += row['sprzedano']

    return result

def compare_sales(today_sales, yesterday_sales):
    changes = {}
    for product in today_sales:
        today = today_sales[product]
        yesterday = yesterday_sales.get(product, 0)
        if yesterday == 0:
            changes[product] = "🆕 nowy produkt"
        else:
            delta_percent = ((today-yesterday)/yesterday)*100
            emoji = '🔺' if delta_percent > 0 else '🔻'
            changes[product] = f"{emoji} {delta_percent:.0f}% vs wczoraj"

    return changes

def total_revenue(data, target_date):
    total_revenue = 0.0
    for row in data:
        if row['data'] == target_date:
            total_revenue += row['sprzedano']*row['cena_jednostkowa']

    return round(total_revenue, 2)


def generate_report(data, report_date):
    yesterday_date = report_date - timedelta(days=1)
    today_sales = sum_sales_by_product(data, report_date)
    yesterday_sales = sum_sales_by_product(data, yesterday_date)
    changes = compare_sales(today_sales, yesterday_sales)
    revenue = total_revenue(data, report_date)

    print(f"📊 AlertIQ – Raport dzienny ({report_date})")
    print("-" * 40)
    for product, quantity in today_sales.items():
        print(f"{product} – {quantity} szt. ({changes[product]})")
    print(f"\n💰 Suma sprzedaży: {revenue:.2f} zł")
