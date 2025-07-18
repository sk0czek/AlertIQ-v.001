from datetime import datetime, timedelta
from collections import defaultdict, Counter

def sum_sales_by_product(data, target_date):
    result = defaultdict(int)
    for row in data:
        if row['data'] == target_date:
            result[row['produkt']] += row['sprzedano']
    
    return result

def total_revenue(data, target_date):
    return round(sum(row['sprzedano']*row['cena_jednostkowa'] for row in data if row['data'] == target_date), 2)

def get_average_order_value(data, target_date):
    orders = [row['sprzedano'] * row['cena_jednostkowa'] for row in data if row['data'] == target_date]
    if not orders:
        return "Brak zamówień"
    return f"{(sum(orders) / len(orders)):.2f} zł"

def count_orders(data, target_date):
    return sum(1 for row in data if row['data'] == target_date)

def get_sales_change_percentage(data, report_date):
    today = total_revenue(data, report_date)
    yesterday = total_revenue(data, report_date - timedelta(days=1))

    if yesterday == 0:
        return "Brak danych"
    delta = ((today-yesterday) / yesterday) * 100
    return f"{delta:.0f}"

def compare_sales(today_sales, yesterday_sales):
    result = {}
    for product in today_sales:
        today = today_sales[product]
        yesterday = yesterday_sales.get(product, 0)
        if yesterday == 0:
            result[product] = "🆕 Nowy produkt"
        else:
            delta = ((today - yesterday) / yesterday) * 100
            emoji = "🔺" if delta > 0 else "🔻"
            result[product] = f"{emoji} {delta:.0f}% vs wczoraj"
    return result

def get_best_selling_products(data, report_date, days=7, top_n=3):
    sales = defaultdict(int)
    for row in data:
        if 0 <= (report_date - row['data']).days < days:
            sales[row['produkt']] += row['sprzedano']
    return sorted(sales.items(), key=lambda x: x[1], reverse=True)[:top_n]

def get_least_selling_products(data, report_date, days=7, bottom_n=3):
    sales = defaultdict(int)
    for row in data:
        if 0 <= (report_date - row['data']).days < days:
            sales[row['produkt']] += row['sprzedano']
    return sorted(sales.items(), key=lambda x:x[1])[:bottom_n]

def get_new_products(data, report_date):
    today = set(row['produkt'] for row in data if row['data'] == report_date)
    yesterday = set(row['produkt'] for row in data if row['data'] == report_date - timedelta(days=1))
    new = today - yesterday
    counter = Counter()
    for row in data:
        if row['data'] == report_date and row['produkt'] in new:
            counter[row['produkt']] += row['sprzedano']
    if counter:
        return counter.most_common(1)[0]
    return None, 0

def get_products_without_sales(data, report_date):
    today_sales = sum_sales_by_product(data, report_date)
    yesterday_sales = sum_sales_by_product(data, report_date - timedelta(days=1))
    return [p for p in yesterday_sales if yesterday_sales[p] > 0 and today_sales.get(p, 0) == 0]

def get_daily_revenue_trend(data, report_date, days=7):
    trend = {}
    for i in reversed(range(days)):
        date = report_date - timedelta(days=i)
        trend[date] = total_revenue(data, date)
    return trend

def get_week_over_week_comparison(data, report_date):
    current_week_start = report_date - timedelta(days=report_date.weekday())
    previous_week_start = current_week_start - timedelta(days=7)

    current_total = 0
    previous_total = 0

    for row in data:
        d = row['data']
        rev = row['sprzedano'] * row['cena_jednostkowa']
        if current_week_start <= d <= report_date:
            current_total += rev
        elif previous_week_start <= d < current_week_start:
            previous_total += rev
        
    if previous_total == 0:
        return "Brak danych"
    
    delta = ((current_total - previous_total) / previous_total) * 100
    return ("📈", delta) if delta > 0 else ("📉", delta) 

def get_recommendations(data, report_date):
    recommendations = []
    new, _ = get_new_products(data, report_date)
    if new:
        recommendations.append((new, "Zwiększ widoczność nowości"))
    missing = get_products_without_sales(data, report_date)
    for m in missing[:1]:
        recommendations.append((m, "Sprawdź, czy oferta jest nadal aktywna"))
    top = get_best_selling_products(data, report_date)
    if top:
        recommendations.append((top[0][0], "Zabezpiecz stan magazynowy"))
    least = get_least_selling_products(data, report_date)
    if least:
        recommendations.append((least[0][0], "Rozważ wycofanie lub promocję"))
    return recommendations[:4]

def generate_report(data, report_date):
    today_sales = sum_sales_by_product(data, report_date)
    yesterday_sales = sum_sales_by_product(data, report_date - timedelta(days=1))
    sales_change = get_sales_change_percentage(data, report_date)

    top_new_product, top_new_product_sales = get_new_products(data, report_date) or ("Brak", 0)
    stale_products = get_products_without_sales(data, report_date)
    stale_product = stale_products[0] if stale_products else "Brak"
    stale_days = 1

    daily_trend = get_daily_revenue_trend(data, report_date)
    emoji, weekly_trend_percent = get_week_over_week_comparison(data, report_date) if get_week_over_week_comparison(data, report_date) != "Brak danych" else ("📊", 0)

    best = get_best_selling_products(data, report_date)
    worst = get_least_selling_products(data, report_date)
    recommendations = get_recommendations(data, report_date)

    # Format product table
    product_table = "| Produkt                        | Ilość | Zmiana vs wczoraj | Status |\n"
    product_table += "|--------------------------------|-------|-------------------|--------|\n"
    changes = compare_sales(today_sales, yesterday_sales)
    for product, qty in sorted(today_sales.items(), key=lambda x: x[1], reverse=True):
        product_name = product[:27] + "..." if len(product) > 27 else product
        product_table += f"| {product_name.ljust(30)} | {str(qty).rjust(5)} | {changes.get(product, '').ljust(17)} | Stały |\n"

    # Format revenue trend
    revenue_chart = " → ".join(f"{date.strftime('%d.%m')}: {value:.0f} zł" for date, value in daily_trend.items())

    return f"""
📊 AlertIQ – Raport Dzienny ({report_date.strftime('%d.%m.%Y')})
=============================================================

🕒 Wygenerowano: {datetime.now().strftime('%d.%m.%Y %H:%M')}
🏪 Sklep: AlertIQ (demo)

## 🔍 Kluczowe Wnioski
- **Sprzedaż**: {total_revenue(data, report_date)} zł ({sales_change}% vs wczoraj)
- **Nowość**: "{top_new_product}" – {top_new_product_sales} szt.
- **Brak sprzedaży**: "{stale_product}" – {stale_days} dzień bez zamówień
- **Tygodniowy trend**: {emoji} {weekly_trend_percent:.0f}% vs poprzedni tydzień

## 💸 Podsumowanie Sprzedaży ({report_date.strftime('%d.%m.%Y')})
{product_table}

- **Całkowity przychód**: {total_revenue(data, report_date)} zł
- **Średnia wartość zamówienia**: {get_average_order_value(data, report_date)}
- **Liczba zamówień**: {count_orders(data, report_date)}

## 📈 Trend Przychodów (Ostatnie 7 Dni)
{revenue_chart}

## 🏆 Top 3 Produkty Tygodnia
""" + "\n".join([f"- {p} – {q} szt." for p, q in best]) + """

## 🐢 Produkty o Niskiej Sprzedaży
""" + "\n".join([f"- {p} – {q} szt." for p, q in worst]) + """

## ✅ Rekomendacje
""" + "\n".join([f"- **{p}**: {a}" for p, a in recommendations]) + """

=============================================================
📬 Kolejny raport: jutro o 9:00
📩 Pytania? Skontaktuj się z AlertIQ: support@alertiq.com
""".strip()