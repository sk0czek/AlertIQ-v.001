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

def compare_sales(today_sales, yesterday_les):
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

def render_html_table(rows, headers):
    html = '<table style="border-collapse: collapse; width: 100%; font-family: monospace;">'
    html += '<thead><tr>'
    for h in headers:
        html += f'<th style="border: 1px solid #ccc; padding: 6px;">{h}</th>'
    html += '</tr></thead><tbody>'
    for row in rows:
        html += '<tr>'
        for cell in row:
            html += f'<td style="border: 1px solid #ccc; padding: 6px;">{cell}</td>'
        html += '</tr>'
    html += '</tbody></table>'
    return html

def generate_report(data, report_date):
    today_sales = sum_sales_by_product(data, report_date)
    yesterday_sales = sum_sales_by_product(data, report_date - timedelta(days=1))
    changes = compare_sales(today_sales, yesterday_sales)

    total = total_revenue(data, report_date)
    avg = get_average_order_value(data, report_date)
    count = count_orders(data, report_date)
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

    # HTML TABLE
    headers = ["Produkt", "Ilość", "Zmiana vs wczoraj", "Status"]
    rows_html = ""
    for product, qty in sorted(today_sales.items(), key=lambda x: x[1], reverse=True):
        change = changes.get(product, "—")
        status = "🆕" if "🆕" in change else "Stały"
        rows_html += f"""
        <tr>
            <td style="border:1px solid #ccc; padding:6px;">{product}</td>
            <td style="border:1px solid #ccc; padding:6px; text-align:center;">{qty}</td>
            <td style="border:1px solid #ccc; padding:6px;">{change}</td>
            <td style="border:1px solid #ccc; padding:6px;">{status}</td>
        </tr>"""

    revenue_chart = "<br>".join([f"{date.strftime('%d.%m')}: {value:.0f} zł" for date, value in daily_trend.items()])
    top3 = "".join([f"<li>{p} – {q} szt.</li>" for p, q in best])
    worst3 = "".join([f"<li>{p} – {q} szt.</li>" for p, q in worst])
    recos = "".join([f"<li><strong>{p}</strong>: {a}</li>" for p, a in recommendations])

    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; font-size: 14px; line-height: 1.6; color: #333;">
        <h2>📊 AlertIQ – Raport Dzienny ({report_date.strftime('%d.%m.%Y')})</h2>
        <p><strong>Wygenerowano:</strong> {datetime.now().strftime('%d.%m.%Y %H:%M')}<br>
        <strong>Sklep:</strong> AlertIQ (demo)</p>

        <h3>🔍 Kluczowe Wnioski</h3>
        <ul>
            <li><strong>Sprzedaż:</strong> {total:.2f} zł ({sales_change}% vs wczoraj)</li>
            <li><strong>Nowość:</strong> "{top_new_product}" – {top_new_product_sales} szt.</li>
            <li><strong>Brak sprzedaży:</strong> "{stale_product}" – {stale_days} dzień bez zamówień</li>
            <li><strong>Tygodniowy trend:</strong> {emoji} {weekly_trend_percent:.0f}% vs poprzedni tydzień</li>
        </ul>

        <h3>💸 Podsumowanie Sprzedaży ({report_date.strftime('%d.%m.%Y')})</h3>
        <table style="border-collapse: collapse; width: 100%; margin-bottom: 20px;">
            <thead>
                <tr>
                    {''.join(f'<th style="border:1px solid #ccc; padding:6px; background:#f4f4f4;">{h}</th>' for h in headers)}
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>

        <p>
            <strong>Całkowity przychód:</strong> {total:.2f} zł<br>
            <strong>Średnia wartość zamówienia:</strong> {avg}<br>
            <strong>Liczba zamówień:</strong> {count}
        </p>

        <h3>📈 Trend Przychodów (Ostatnie 7 dni)</h3>
        <p style="white-space:pre-wrap;">{revenue_chart}</p>

        <h3>🏆 Top 3 Produkty Tygodnia</h3>
        <ul>{top3}</ul>

        <h3>🐢 Produkty o Niskiej Sprzedaży</h3>
        <ul>{worst3}</ul>

        <h3>✅ Rekomendacje</h3>
        <ul>{recos}</ul>

        <hr>
        <p>📬 Kolejny raport: jutro o 9:00<br>
        📩 Pytania? Skontaktuj się z AlertIQ: <a href="mailto:support@alertiq.com">support@alertiq.com</a></p>
    </body>
    </html>
    """