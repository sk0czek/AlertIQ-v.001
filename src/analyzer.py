from datetime import datetime, timedelta
from collections import defaultdict, Counter

# ------------------ BASIC ------------------------
def sum_sales_by_product(data, target_date):
    result = defaultdict(int)
    for row in data:
        if row['data'] == target_date:
            result[row['produkt']] += row['sprzedano']
    
    return result

def total_revenue(data, target_date):
    return round(sum(row['sprzedano']*row['cena_jednostkowa'] for row in data if row['data'] == target_date), 2)

def get_average_order_value(data, target_date):
    # Compute based on unique orders (if order_id available), else fallback to line-based average
    revenues_by_order = defaultdict(float)
    num_orders = 0
    for row in data:
        if row['data'] == target_date:
            order_key = row.get('order_id') or (row['produkt'], row['data'])
            revenues_by_order[order_key] += row['sprzedano'] * row['cena_jednostkowa']
    num_orders = len(revenues_by_order)
    if num_orders == 0:
        return "Brak zamówień"
    avg = sum(revenues_by_order.values()) / num_orders
    return f"{avg:.2f} zł"

def count_orders(data, target_date):
    # Count unique orders if possible
    order_ids = set()
    for row in data:
        if row['data'] == target_date:
            order_ids.add(row.get('order_id') or (row['produkt'], row['data']))
    return len(order_ids)

# ------------------ ZMIANY I POROWNANIA ----------
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

# ----------------------- BEST / WORST --------------
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

# ------------------- NOWE PRODUKTY I BRAKI
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

# -------------------------- ZALECENIA ----------------
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

def get_seasonality_comparison(data, report_date):
    """Porównanie z tym samym dniem tygodnia z poprzednich tygodni"""
    target_weekday = report_date.weekday()
    today_revenue = total_revenue(data, report_date)
    
    # Znajdź ten sam dzień tygodnia z poprzednich 3 tygodni
    previous_weeks = []
    for week in range(1, 4):
        prev_date = report_date - timedelta(days=7 * week)
        # Dostosuj do tego samego dnia tygodnia
        while prev_date.weekday() != target_weekday:
            prev_date -= timedelta(days=1)
        prev_revenue = total_revenue(data, prev_date)
        if prev_revenue > 0:
            previous_weeks.append(prev_revenue)
    
    if not previous_weeks:
        return "Brak danych historycznych"
    
    avg_previous = sum(previous_weeks) / len(previous_weeks)
    if avg_previous == 0:
        return "Brak danych"
    
    change = ((today_revenue - avg_previous) / avg_previous) * 100
    return f"{change:+.0f}% vs średnia z poprzednich {len(previous_weeks)} tygodni"

def get_conversion_rate(data, report_date):
    """Wskaźnik konwersji - uproszczona wersja (można rozszerzyć o dane o wyświetleniach)"""
    # Uproszczona wersja - stosunek zamówień do liczby produktów
    today_orders = count_orders(data, report_date)
    today_products = len(set(row['produkt'] for row in data if row['data'] == report_date))
    
    if today_products == 0:
        return "Brak danych"
    
    # Symulacja konwersji (w rzeczywistości potrzebne dane o wyświetleniach)
    # Zakładamy, że każdy produkt miał 10 wyświetleń
    estimated_views = today_products * 10
    conversion = (today_orders / estimated_views) * 100 if estimated_views > 0 else 0
    
    return f"{conversion:.1f}% (szacunkowo)"

def get_aov_trend(data, report_date, days=7):
    """Trend średniej wartości zamówienia (AOV)"""
    aov_values = []
    for i in range(days):
        date = report_date - timedelta(days=i)
        avg = get_average_order_value(data, date)
        if avg != "Brak zamówień":
            aov_values.append(float(avg.replace(' zł', '')))
    
    if len(aov_values) < 2:
        return "Brak danych"
    
    current_aov = aov_values[0]
    avg_previous = sum(aov_values[1:]) / len(aov_values[1:])
    
    if avg_previous == 0:
        return "Brak danych"
    
    change = ((current_aov - avg_previous) / avg_previous) * 100
    return f"{change:+.1f}% vs średnia z ostatnich {days-1} dni"

def get_customer_retention(data, report_date, days=30):
    """Wskaźnik retencji klientów (uproszczona wersja)"""
    # Uproszczona wersja - sprawdzamy czy klienci wracają
    # W rzeczywistości potrzebne dane o ID klientów
    
    # Symulacja retencji na podstawie powtarzających się produktów
    recent_products = set()
    older_products = set()
    
    for row in data:
        days_diff = (report_date - row['data']).days
        if 0 <= days_diff < 7:  # Ostatni tydzień
            recent_products.add(row['produkt'])
        elif 7 <= days_diff < days:  # Starsze dane
            older_products.add(row['produkt'])
    
    returning_products = recent_products.intersection(older_products)
    
    if len(older_products) == 0:
        return "Brak danych historycznych"
    
    retention_rate = (len(returning_products) / len(older_products)) * 100
    return f"{retention_rate:.1f}% produktów wróciło"

def get_sales_stability(data, report_date, days=7):
    """Wskaźnik stabilności sprzedaży (odchylenie standardowe)"""
    revenues = []
    for i in range(days):
        date = report_date - timedelta(days=i)
        rev = total_revenue(data, date)
        revenues.append(rev)
    
    if len(revenues) < 2:
        return "Brak danych"
    
    mean_revenue = sum(revenues) / len(revenues)
    variance = sum((x - mean_revenue) ** 2 for x in revenues) / len(revenues)
    std_dev = variance ** 0.5
    
    if mean_revenue == 0:
        return "Brak sprzedaży"
    
    coefficient_of_variation = (std_dev / mean_revenue) * 100
    
    if coefficient_of_variation < 20:
        stability = "Stabilna"
    elif coefficient_of_variation < 40:
        stability = "Umiarkowana"
    else:
        stability = "Zmienna"
    
    return f"{stability} (CV: {coefficient_of_variation:.1f}%)"

def get_long_term_trend(data, report_date, days=30):
    """Wskaźnik trendu długoterminowego (ostatnie 30 dni)"""
    if days < 2:
        return "Brak danych"
    
    # Podziel dane na dwie połowy
    mid_point = days // 2
    
    first_half_revenue = 0
    second_half_revenue = 0
    
    for i in range(days):
        date = report_date - timedelta(days=i)
        rev = total_revenue(data, date)
        
        if i < mid_point:
            second_half_revenue += rev
        else:
            first_half_revenue += rev
    
    if first_half_revenue == 0:
        return "Brak danych"
    
    change = ((second_half_revenue - first_half_revenue) / first_half_revenue) * 100
    
    if change > 10:
        trend = "📈 Rosnący"
    elif change < -10:
        trend = "📉 Spadający"
    else:
        trend = "📊 Stabilny"
    
    return f"{trend} ({change:+.1f}%)"


# ------------ RAPORT GLOWNY ---------------
def generate_report(data, report_date):
    from datetime import datetime

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
    wow = get_week_over_week_comparison(data, report_date)
    if wow == "Brak danych":
        emoji, weekly_trend_percent = ("📊", 0)
    else:
        emoji, weekly_trend_percent = wow

    best = get_best_selling_products(data, report_date)
    worst = get_least_selling_products(data, report_date)
    recommendations = get_recommendations(data, report_date)

    # Nowe wskaźniki
    seasonality = get_seasonality_comparison(data, report_date)
    conversion_rate = get_conversion_rate(data, report_date)
    aov_trend = get_aov_trend(data, report_date)
    customer_retention = get_customer_retention(data, report_date)
    sales_stability = get_sales_stability(data, report_date)
    long_term_trend = get_long_term_trend(data, report_date)

    # Generate line chart data
    chart_data = []
    max_value = max(daily_trend.values()) if daily_trend.values() else 1
    chart_height = 120
    chart_width = 700
    
    for i, (date, value) in enumerate(daily_trend.items()):
        x = (i / (len(daily_trend) - 1)) * chart_width if len(daily_trend) > 1 else chart_width / 2
        y = chart_height - (value / max_value) * chart_height
        chart_data.append({
            'date': date.strftime('%d'),
            'value': value,
            'x': x,
            'y': y,
            'height': chart_height - y
        })

    # Generate SVG path for line chart
    if len(chart_data) > 1:
        path_points = []
        for point in chart_data:
            path_points.append(f"{point['x']},{point['y']}")
        path_d = f"M {' L '.join(path_points)}"
    else:
        path_d = f"M {chart_data[0]['x']},{chart_data[0]['y']}"

    # Format recommendations
    recos = "".join([f'<li style="margin-bottom: 8px;">{a}</li>' for _, a in recommendations])

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AlertIQ - Raport Dzienny</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0;
                padding: 40px;
                background-color: white;
                color: #333;
                line-height: 1.6;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
            }}
            .header {{
                margin-bottom: 40px;
            }}
            .header h1 {{
                margin: 0 0 8px 0;
                font-size: 28px;
                font-weight: 700;
                color: #333;
                display: inline-block;
            }}
            .header .date {{
                float: right;
                font-size: 18px;
                font-weight: 600;
                color: #333;
                margin-top: 5px;
            }}
            .header .subtitle {{
                color: #666;
                font-size: 14px;
                margin-bottom: 5px;
            }}
            .header .generated {{
                color: #999;
                font-size: 14px;
            }}
            .metrics {{
                display: flex;
                gap: 20px;
                margin-bottom: 40px;
            }}
            .metric-card {{
                flex: 1;
                padding: 24px;
                border-radius: 8px;
                text-align: center;
            }}
            .metric-card.revenue {{
                background: #fef7ed;
            }}
            .metric-card.orders {{
                background: #f0f9ff;
            }}
            .metric-card .label {{
                font-size: 14px;
                font-weight: 600;
                margin-bottom: 8px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            .metric-card .value {{
                font-size: 32px;
                font-weight: 800;
                margin-bottom: 8px;
                color: #333;
            }}
            .metric-card .change {{
                font-size: 14px;
                font-weight: 500;
            }}
            .metric-card.revenue .label {{
                color: #FF6B35;
            }}
            .metric-card.revenue .change {{
                color: #FF6B35;
            }}
            .metric-card.orders .label {{
                color: #4A90E2;
            }}
            .metric-card.orders .change {{
                color: #4A90E2;
            }}
            .section {{
                margin-bottom: 40px;
            }}
            .section h3 {{
                margin: 0 0 20px 0;
                font-size: 20px;
                font-weight: 700;
                color: #333;
            }}
            .insights {{
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
            }}
            .insights ul {{
                margin: 0;
                padding-left: 20px;
            }}
            .insights li {{
                margin-bottom: 8px;
                color: #555;
            }}
            .advanced-metrics {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 16px;
                margin: 20px 0;
            }}
            .metric-item {{
                background: #f8f9fa;
                padding: 16px;
                border-radius: 8px;
                border-left: 4px solid #FF6B35;
            }}
            .metric-item h4 {{
                margin: 0 0 8px 0;
                font-size: 14px;
                font-weight: 600;
                color: #333;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            .metric-item .value {{
                font-size: 16px;
                font-weight: 600;
                color: #FF6B35;
            }}
            .sales-table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                background: white;
                border-radius: 8px;
                overflow: hidden;
            }}
            .sales-table th {{
                background: #f8f9fa;
                padding: 12px;
                text-align: left;
                font-weight: 600;
                color: #333;
                border-bottom: 2px solid #e5e7eb;
            }}
            .sales-table td {{
                padding: 12px;
                border-bottom: 1px solid #f0f0f0;
            }}
            .status-new {{
                color: #059669;
                font-weight: 600;
            }}
            .status-regular {{
                color: #6b7280;
            }}
            .product-list {{
                display: flex;
                flex-direction: column;
                gap: 12px;
            }}
            .product-item {{
                background: #f8f9fa;
                padding: 16px;
                border-radius: 6px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            .product-name {{
                font-weight: 500;
                color: #374151;
                font-size: 16px;
            }}
            .product-qty {{
                font-weight: 600;
                color: #059669;
                background: #d1fae5;
                padding: 6px 12px;
                border-radius: 16px;
                font-size: 14px;
            }}
            .chart-container {{
                margin: 20px 0;
                background: white;
                border-radius: 8px;
                padding: 20px;
            }}
            .chart {{
                position: relative;
                height: 140px;
                margin: 20px 0;
            }}
            .chart-line {{
                stroke: #FF6B35;
                stroke-width: 3;
                fill: none;
                stroke-linecap: round;
                stroke-linejoin: round;
            }}
            .chart-point {{
                fill: #FF6B35;
                stroke: white;
                stroke-width: 2;
            }}
            .chart-labels {{
                display: flex;
                justify-content: space-between;
                margin-top: 16px;
                padding: 0 10px;
            }}
            .chart-label {{
                font-size: 12px;
                color: #666;
                text-align: center;
            }}
            .recommendations {{
                list-style: none;
                padding: 0;
                margin: 0;
            }}
            .recommendations li {{
                background: #fef7ed;
                color: #92400e;
                padding: 16px;
                border-radius: 6px;
                margin-bottom: 12px;
                font-weight: 500;
                border-left: 4px solid #FF6B35;
            }}
            .footer {{
                text-align: center;
                color: #999;
                font-size: 14px;
                margin-top: 40px;
            }}
            @media (max-width: 600px) {{
                .metrics {{
                    flex-direction: column;
                }}
                .advanced-metrics {{
                    grid-template-columns: 1fr;
                }}
                .header .date {{
                    float: none;
                    display: block;
                    margin-top: 15px;
                }}
                .sales-table {{
                    font-size: 12px;
                }}
                .sales-table th,
                .sales-table td {{
                    padding: 8px;
                }}
                .chart-container {{
                    padding: 15px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>AlertIQ - Raport Dzienny</h1>
                <div class="date">{report_date.strftime('%d.%m.%Y')}</div>
                <div class="subtitle">Sklep: AlertIQ (demo)</div>
                <div class="generated">Wygenerowano: {datetime.now().strftime('%d.%m.%Y %H:%M')}</div>
            </div>

            <div class="metrics">
                <div class="metric-card revenue">
                    <div class="label">Przychód</div>
                    <div class="value">{total:.2f} zł</div>
                    <div class="change">+{sales_change}% vs wczoraj</div>
                </div>
                <div class="metric-card orders">
                    <div class="label">Zamówienia</div>
                    <div class="value">{count}</div>
                    <div class="change">Średnio {avg.replace(' zł', '')} zł</div>
                </div>
            </div>

            <div class="section">
                <h3>🔍 Kluczowe Wnioski</h3>
                <div class="insights">
                    <ul>
                        <li><strong>Sprzedaż:</strong> {total:.2f} zł ({sales_change}% vs wczoraj)</li>
                        <li><strong>Nowość:</strong> "{top_new_product}" – {top_new_product_sales} szt.</li>
                        <li><strong>Brak sprzedaży:</strong> "{stale_product}" – {stale_days} dzień bez zamówień</li>
                        <li><strong>Tygodniowy trend:</strong> {emoji} {weekly_trend_percent:.0f}% vs poprzedni tydzień</li>
                    </ul>
                </div>
            </div>

            <div class="section">
                <h3>📊 Zaawansowane Wskaźniki</h3>
                <div class="advanced-metrics">
                    <div class="metric-item">
                        <h4>Sezonowość</h4>
                        <div class="value">{seasonality}</div>
                    </div>
                    <div class="metric-item">
                        <h4>Konwersja</h4>
                        <div class="value">{conversion_rate}</div>
                    </div>
                    <div class="metric-item">
                        <h4>Trend AOV</h4>
                        <div class="value">{aov_trend}</div>
                    </div>
                    <div class="metric-item">
                        <h4>Retencja Klientów</h4>
                        <div class="value">{customer_retention}</div>
                    </div>
                    <div class="metric-item">
                        <h4>Stabilność Sprzedaży</h4>
                        <div class="value">{sales_stability}</div>
                    </div>
                    <div class="metric-item">
                        <h4>Trend Długoterminowy</h4>
                        <div class="value">{long_term_trend}</div>
                    </div>
                </div>
            </div>

            <div class="section">
                <h3>💸 Podsumowanie Sprzedaży ({report_date.strftime('%d.%m.%Y')})</h3>
                <table class="sales-table">
                    <thead>
                        <tr>
                            <th>Produkt</th>
                            <th>Ilość</th>
                            <th>Zmiana vs wczoraj</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join([f'''
                        <tr>
                            <td>{product[:50]}</td>
                            <td style="text-align: center;">{qty}</td>
                            <td>{changes.get(product, "—")}</td>
                            <td class="{'status-new' if '🆕' in changes.get(product, '') else 'status-regular'}">
                                {'🆕' if '🆕' in changes.get(product, '') else 'Stały'}
                            </td>
                        </tr>''' for product, qty in sorted(today_sales.items(), key=lambda x: x[1], reverse=True)])}
                    </tbody>
                </table>
            </div>

            <div class="section">
                <h3>🏆 Top 3 Produkty Tygodnia</h3>
                <div class="product-list">
                    {''.join([f'''
                    <div class="product-item">
                        <div class="product-name">{p}</div>
                        <div class="product-qty">{q} szt.</div>
                    </div>''' for p, q in best])}
                </div>
            </div>

            <div class="section">
                <h3>🐢 Produkty o Niskiej Sprzedaży</h3>
                <div class="product-list">
                    {''.join([f'''
                    <div class="product-item">
                        <div class="product-name">{p}</div>
                        <div class="product-qty">{q} szt.</div>
                    </div>''' for p, q in worst])}
                </div>
            </div>

            <div class="section">
                <h3>📈 Trend Przychodów (7 dni)</h3>
                <div class="chart-container">
                    <svg width="100%" height="140" viewBox="0 0 700 140">
                        <defs>
                            <linearGradient id="lineGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                                <stop offset="0%" style="stop-color:#FF6B35;stop-opacity:0.3" />
                                <stop offset="100%" style="stop-color:#FF6B35;stop-opacity:0" />
                            </linearGradient>
                        </defs>
                        <!-- Grid lines -->
                        <line x1="0" y1="35" x2="700" y2="35" stroke="#f0f0f0" stroke-width="1"/>
                        <line x1="0" y1="70" x2="700" y2="70" stroke="#f0f0f0" stroke-width="1"/>
                        <line x1="0" y1="105" x2="700" y2="105" stroke="#f0f0f0" stroke-width="1"/>
                        
                        <!-- Line chart -->
                        <path d="{path_d}" class="chart-line"/>
                        
                        <!-- Data points -->
                        {''.join([f'''
                        <circle cx="{point['x']}" cy="{point['y']}" r="4" class="chart-point"/>
                        <text x="{point['x']}" y="{point['y'] - 8}" text-anchor="middle" font-size="10" fill="#666">{point['value']:.0f}</text>''' for point in chart_data])}
                    </svg>
                    <div class="chart-labels">
                        {''.join([f'<div class="chart-label">{point["date"]}</div>' for point in chart_data])}
                    </div>
                </div>
            </div>

            <div class="section">
                <h3>✅ Rekomendacje</h3>
                <ul class="recommendations">
                    {recos}
                </ul>
            </div>

            <div class="footer">
                Kolejny raport: jutro o 9:00
            </div>
        </div>
    </body>
    </html>
    """