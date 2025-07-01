from datetime import datetime, timedelta
from collections import defaultdict

def sum_sales_by_product(data, target_date):
    result = defaultdict(int)
    for row in data:
        if row['data'] == target_date:
            result[row['produkt']] += row['sprzedano']

    return result

def products_without_sales(data, report_date):
    yesterday = report_date - timedelta(days=1)
    today_sales = sum_sales_by_product(data, report_date)
    yesterday_sales = sum_sales_by_product(data, yesterday)

    missing = []
    for product in yesterday_sales:
        if yesterday_sales[product] > 0 and today_sales.get(product, 0) == 0:
            missing.append(product)
    
    return missing

def get_best_selling_products(data, report_date, days=7, top_n=3):
    sales = defaultdict(int)

    for row in data:
        days_diff = (report_date - row["data"]).days
        if 0 <= days_diff < days:
            sales[row["produkt"]] += row["sprzedano"]
    
    sorted_sales = sorted(sales.items(), key=lambda x: x[1], reverse=True)

    return sorted_sales[:top_n]

def get_least_selling_products(data, report_date, days=7, bottom_n=3):
    sales = defaultdict(int)

    for row in data:
        days_diff = (report_date - row["data"]).days
        if 0 <= days_diff <= days:
            sales[row["produkt"]] += row["sprzedano"]
    
    filtered_sales = {k: v for k, v in sales.items() if v > 0}
    sorted_sales = sorted(filtered_sales.items(), key = lambda x: x[1])

    return sorted_sales[:bottom_n]

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
            changes[product] = f"{delta_percent:.0f}% vs wczoraj"

    return changes

def get_week_over_week_comparison(data, report_date):
    current_week_start = report_date - timedelta(days=report_date.weekday())
    previous_week_start = current_week_start - timedelta(days=7)

    current_week_total = 0.0
    previous_week_total = 0.0

    for row in data:
        row_date = row["data"]
        revenue = row["sprzedano"] * row["cena_jednostkowa"]

        if current_week_start <= row_date <= report_date:
            current_week_total += revenue
        elif previous_week_start <= row_date < current_week_start:
            previous_week_total += revenue
        
    if previous_week_total == 0:
        return "Brak danych z poprzedniego tygodnia"
    
    delta_percent = ((current_week_total - previous_week_total) / previous_week_total) * 100
    emoji = "🔺" if delta_percent > 0 else "🔻"
    return f"{emoji} {delta_percent:.0f}% vs poprzedni tydzien"

def get_average_order_value(data, target_date):
    total_revenue = 0.0
    total_orders = 0

    for row in data:
        if row["data"] == target_date:
            total_revenue += row["sprzedano"] * row["cena_jednostkowa"]
            total_orders += 1

    if total_orders == 0:
        return "Brak zamówień"

    avg_value = total_revenue / total_orders
    return f"{avg_value:.2f} zł"


def total_revenue(data, target_date):
    total_revenue = 0.0
    for row in data:
        if row['data'] == target_date:
            total_revenue += row['sprzedano']*row['cena_jednostkowa']

    return round(total_revenue, 2)

def get_daily_revenue_trend(data, report_date, days=2):
    trend = {}
    for i in range(days):
        day = report_date - timedelta(days=i)
        trend[day] = total_revenue(data, day)
    
    return dict(sorted(trend.items()))

def generate_report(data, report_date):
    yesterday_date = report_date - timedelta(days=1)
    today_sales = sum_sales_by_product(data, report_date)

    if not today_sales:
        return f"📊 Raport dzienny ({report_date}):\nBrak danych sprzedażowych."

    # basic raport
    yesterday_sales = sum_sales_by_product(data, yesterday_date)
    changes = compare_sales(today_sales, yesterday_sales)
    revenue = total_revenue(data, report_date)

    lines = [f"📊 AlertIQ – Raport dzienny ({report_date})", "-" * 40]
    for product, quantity in today_sales.items():
        lines.append(f"{product} – {quantity} szt. ({changes[product]})")

    lines.append(f"\n💰 Suma sprzedaży: {revenue:.2f} zł")

    # product_without_sales
    missing_products = products_without_sales(data, report_date)
    if missing_products:
        lines.append("\n📉 Produkty, które dziś się nie sprzedały (a sprzedawały się wczoraj):")
        for product in missing_products:
            lines.append(f"  -- {product}")
    else:
        lines.append("\n✅ Wszystkie aktywne produkty nadal się sprzedają.")
    
    # revenue trend
    trend = get_daily_revenue_trend(data, report_date)
    lines.append("\n📈 Trend przychodów (ostatnie 7 dni):")
    for day, value in trend.items():
        day_str = day.strftime("%d.%m")
        lines.append(f"{day_str}: {value:.2f} zł")

    # best selling products
    bestsellers = get_best_selling_products(data, report_date)
    if bestsellers:
        lines.append("\n🏆 Najlepiej sprzedające się produkty (ostatnie 7 dni):")
        for name, qty in bestsellers:
            lines.append(f"{name}: {qty} szt.")

    # least_selling_products
    least_sellers = get_least_selling_products(data, report_date)
    if least_sellers:
        lines.append("\n🐌 Produkty o najsłabszej sprzedaży (ostatnie 7 dni):")
        for name, qty in least_sellers:
            lines.append(f"{name}: {qty} szt.")

    # week over week comaprison

    week_trend = get_week_over_week_comparison(data, report_date)
    lines.append(f"\n📆 Tygodniowy trend sprzedaży: {week_trend}")

    avg_order_value = get_average_order_value(data, report_date)
    lines.append(f"📐 Średnia wartość zamówienia: {avg_order_value}")

    return "\n".join(lines)