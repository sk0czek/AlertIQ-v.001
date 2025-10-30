from datetime import date, timedelta

# Daty testowe - ostatnie 30 dni
today = date.today()
yesterday = today - timedelta(days=1)
two_days_ago = today - timedelta(days=2)
three_days_ago = today - timedelta(days=3)
four_days_ago = today - timedelta(days=4)
five_days_ago = today - timedelta(days=5)
six_days_ago = today - timedelta(days=6)
week_ago = today - timedelta(days=7)
two_weeks_ago = today - timedelta(days=14)
three_weeks_ago = today - timedelta(days=21)
month_ago = today - timedelta(days=30)

# Dane testowe zgodne z formatem Allegro API
test_data = [
    # ===== DZISIAJ (today) =====
    # Bestseller - Kawa Arabica (wielu klientów, różne zamówienia)
    {"data": today, "order_id": "ORD-2024-001", "customer_id": "CUST-001", "produkt": "Kawa Arabica Premium 500g", "sprzedano": 2, "cena_jednostkowa": 45.99},
    {"data": today, "order_id": "ORD-2024-002", "customer_id": "CUST-002", "produkt": "Kawa Arabica Premium 500g", "sprzedano": 1, "cena_jednostkowa": 45.99},
    {"data": today, "order_id": "ORD-2024-003", "customer_id": "CUST-003", "produkt": "Kawa Arabica Premium 500g", "sprzedano": 3, "cena_jednostkowa": 45.99},
    
    # Nowy produkt - Energy Drink (duża sprzedaż)
    {"data": today, "order_id": "ORD-2024-004", "customer_id": "CUST-004", "produkt": "Energy Drink Natural 250ml", "sprzedano": 5, "cena_jednostkowa": 8.50},
    {"data": today, "order_id": "ORD-2024-005", "customer_id": "CUST-005", "produkt": "Energy Drink Natural 250ml", "sprzedano": 3, "cena_jednostkowa": 8.50},
    
    # Kolejny nowy produkt - Shot Imbirowy
    {"data": today, "order_id": "ORD-2024-006", "customer_id": "CUST-006", "produkt": "Shot Imbirowy 50ml", "sprzedano": 2, "cena_jednostkowa": 12.99},
    
    # Produkty z wczoraj (kontynuacja)
    {"data": today, "order_id": "ORD-2024-007", "customer_id": "CUST-007", "produkt": "Woda Kokosowa 1L", "sprzedano": 2, "cena_jednostkowa": 15.50},
    {"data": today, "order_id": "ORD-2024-008", "customer_id": "CUST-008", "produkt": "Baton Proteinowy 60g", "sprzedano": 4, "cena_jednostkowa": 6.99},
    
    # Slow seller - Sok Marchewkowy
    {"data": today, "order_id": "ORD-2024-009", "customer_id": "CUST-009", "produkt": "Sok Marchewkowy 500ml", "sprzedano": 1, "cena_jednostkowa": 9.99},

    # ===== WCZORAJ (yesterday) =====
    {"data": yesterday, "order_id": "ORD-2024-010", "customer_id": "CUST-010", "produkt": "Kawa Arabica Premium 500g", "sprzedano": 1, "cena_jednostkowa": 45.99},
    {"data": yesterday, "order_id": "ORD-2024-011", "customer_id": "CUST-011", "produkt": "Herbata Zielona 100g", "sprzedano": 2, "cena_jednostkowa": 18.50},
    {"data": yesterday, "order_id": "ORD-2024-012", "customer_id": "CUST-012", "produkt": "Woda Kokosowa 1L", "sprzedano": 3, "cena_jednostkowa": 15.50},
    {"data": yesterday, "order_id": "ORD-2024-013", "customer_id": "CUST-013", "produkt": "Baton Proteinowy 60g", "sprzedano": 2, "cena_jednostkowa": 6.99},
    {"data": yesterday, "order_id": "ORD-2024-014", "customer_id": "CUST-014", "produkt": "Sok Pomidorowy 500ml", "sprzedano": 1, "cena_jednostkowa": 7.99},

    # ===== 2 DNI TEMU =====
    {"data": two_days_ago, "order_id": "ORD-2024-015", "customer_id": "CUST-015", "produkt": "Kawa Arabica Premium 500g", "sprzedano": 2, "cena_jednostkowa": 45.99},
    {"data": two_days_ago, "order_id": "ORD-2024-016", "customer_id": "CUST-016", "produkt": "Baton Proteinowy 60g", "sprzedano": 3, "cena_jednostkowa": 6.99},
    {"data": two_days_ago, "order_id": "ORD-2024-017", "customer_id": "CUST-017", "produkt": "Herbata Czarna 100g", "sprzedano": 1, "cena_jednostkowa": 22.00},

    # ===== 3 DNI TEMU =====
    {"data": three_days_ago, "order_id": "ORD-2024-018", "customer_id": "CUST-018", "produkt": "Kawa Arabica Premium 500g", "sprzedano": 1, "cena_jednostkowa": 45.99},
    {"data": three_days_ago, "order_id": "ORD-2024-019", "customer_id": "CUST-019", "produkt": "Sok Marchewkowy 500ml", "sprzedano": 1, "cena_jednostkowa": 9.99},
    {"data": three_days_ago, "order_id": "ORD-2024-020", "customer_id": "CUST-020", "produkt": "Shot Magnezowy 50ml", "sprzedano": 2, "cena_jednostkowa": 14.99},

    # ===== 4 DNI TEMU =====
    {"data": four_days_ago, "order_id": "ORD-2024-021", "customer_id": "CUST-021", "produkt": "Kawa Arabica Premium 500g", "sprzedano": 3, "cena_jednostkowa": 45.99},
    {"data": four_days_ago, "order_id": "ORD-2024-022", "customer_id": "CUST-022", "produkt": "Sok Pomidorowy 500ml", "sprzedano": 2, "cena_jednostkowa": 7.99},
    {"data": four_days_ago, "order_id": "ORD-2024-023", "customer_id": "CUST-023", "produkt": "Herbata Zielona 100g", "sprzedano": 1, "cena_jednostkowa": 18.50},

    # ===== 5 DNI TEMU =====
    {"data": five_days_ago, "order_id": "ORD-2024-024", "customer_id": "CUST-024", "produkt": "Kawa Arabica Premium 500g", "sprzedano": 2, "cena_jednostkowa": 45.99},
    {"data": five_days_ago, "order_id": "ORD-2024-025", "customer_id": "CUST-025", "produkt": "Sok Pomidorowy 500ml", "sprzedano": 1, "cena_jednostkowa": 7.99},
    {"data": five_days_ago, "order_id": "ORD-2024-026", "customer_id": "CUST-026", "produkt": "Woda Kokosowa 1L", "sprzedano": 1, "cena_jednostkowa": 15.50},

    # ===== 6 DNI TEMU =====
    {"data": six_days_ago, "order_id": "ORD-2024-027", "customer_id": "CUST-027", "produkt": "Kawa Arabica Premium 500g", "sprzedano": 1, "cena_jednostkowa": 45.99},
    {"data": six_days_ago, "order_id": "ORD-2024-028", "customer_id": "CUST-028", "produkt": "Herbata Zielona 100g", "sprzedano": 2, "cena_jednostkowa": 18.50},
    {"data": six_days_ago, "order_id": "ORD-2024-029", "customer_id": "CUST-029", "produkt": "Shot Magnezowy 50ml", "sprzedano": 1, "cena_jednostkowa": 14.99},

    # ===== TYDZIEŃ TEMU =====
    {"data": week_ago, "order_id": "ORD-2024-030", "customer_id": "CUST-030", "produkt": "Kawa Arabica Premium 500g", "sprzedano": 2, "cena_jednostkowa": 45.99},
    {"data": week_ago, "order_id": "ORD-2024-031", "customer_id": "CUST-031", "produkt": "Baton Proteinowy 60g", "sprzedano": 1, "cena_jednostkowa": 6.99},
    {"data": week_ago, "order_id": "ORD-2024-032", "customer_id": "CUST-032", "produkt": "Herbata Czarna 100g", "sprzedano": 1, "cena_jednostkowa": 22.00},

    # ===== 2 TYGODNIE TEMU =====
    {"data": two_weeks_ago, "order_id": "ORD-2024-033", "customer_id": "CUST-033", "produkt": "Kawa Arabica Premium 500g", "sprzedano": 1, "cena_jednostkowa": 45.99},
    {"data": two_weeks_ago, "order_id": "ORD-2024-034", "customer_id": "CUST-034", "produkt": "Woda Kokosowa 1L", "sprzedano": 2, "cena_jednostkowa": 15.50},
    {"data": two_weeks_ago, "order_id": "ORD-2024-035", "customer_id": "CUST-035", "produkt": "Sok Pomidorowy 500ml", "sprzedano": 1, "cena_jednostkowa": 7.99},

    # ===== 3 TYGODNIE TEMU =====
    {"data": three_weeks_ago, "order_id": "ORD-2024-036", "customer_id": "CUST-036", "produkt": "Kawa Arabica Premium 500g", "sprzedano": 2, "cena_jednostkowa": 45.99},
    {"data": three_weeks_ago, "order_id": "ORD-2024-037", "customer_id": "CUST-037", "produkt": "Herbata Zielona 100g", "sprzedano": 1, "cena_jednostkowa": 18.50},
    {"data": three_weeks_ago, "order_id": "ORD-2024-038", "customer_id": "CUST-038", "produkt": "Baton Proteinowy 60g", "sprzedano": 2, "cena_jednostkowa": 6.99},

    # ===== MIESIĄC TEMU =====
    {"data": month_ago, "order_id": "ORD-2024-039", "customer_id": "CUST-039", "produkt": "Kawa Arabica Premium 500g", "sprzedano": 1, "cena_jednostkowa": 45.99},
    {"data": month_ago, "order_id": "ORD-2024-040", "customer_id": "CUST-040", "produkt": "Woda Kokosowa 1L", "sprzedano": 1, "cena_jednostkowa": 15.50},
    {"data": month_ago, "order_id": "ORD-2024-041", "customer_id": "CUST-041", "produkt": "Sok Marchewkowy 500ml", "sprzedano": 1, "cena_jednostkowa": 9.99},

    # ===== DODATKOWE DANE DLA TESTÓW =====
    # Produkty z różnymi cenami dla testów AOV
    {"data": today, "order_id": "ORD-2024-042", "customer_id": "CUST-042", "produkt": "Kawa Ekskluzywna 1kg", "sprzedano": 1, "cena_jednostkowa": 89.99},
    {"data": yesterday, "order_id": "ORD-2024-043", "customer_id": "CUST-043", "produkt": "Kawa Ekskluzywna 1kg", "sprzedano": 1, "cena_jednostkowa": 89.99},
    
    # Produkty z bardzo niską sprzedażą (dla testów worst sellers)
    {"data": today, "order_id": "ORD-2024-044", "customer_id": "CUST-044", "produkt": "Sok Z Buraka 500ml", "sprzedano": 1, "cena_jednostkowa": 11.99},
    {"data": yesterday, "order_id": "ORD-2024-045", "customer_id": "CUST-045", "produkt": "Sok Z Buraka 500ml", "sprzedano": 1, "cena_jednostkowa": 11.99},
    
    # Produkty sezonowe (dla testów sezonowości)
    {"data": today, "order_id": "ORD-2024-046", "customer_id": "CUST-046", "produkt": "Herbata Zimowa 100g", "sprzedano": 2, "cena_jednostkowa": 25.99},
    {"data": week_ago, "order_id": "ORD-2024-047", "customer_id": "CUST-047", "produkt": "Herbata Zimowa 100g", "sprzedano": 1, "cena_jednostkowa": 25.99},
    {"data": two_weeks_ago, "order_id": "ORD-2024-048", "customer_id": "CUST-048", "produkt": "Herbata Zimowa 100g", "sprzedano": 3, "cena_jednostkowa": 25.99},
    {"data": three_weeks_ago, "order_id": "ORD-2024-049", "customer_id": "CUST-049", "produkt": "Herbata Zimowa 100g", "sprzedano": 2, "cena_jednostkowa": 25.99},
]

# Dane o wyświetleniach produktów (dla testów konwersji)
views_data = {
    "Kawa Arabica Premium 500g": 150,
    "Energy Drink Natural 250ml": 80,
    "Shot Imbirowy 50ml": 45,
    "Woda Kokosowa 1L": 120,
    "Baton Proteinowy 60g": 200,
    "Sok Marchewkowy 500ml": 30,
    "Herbata Zielona 100g": 90,
    "Sok Pomidorowy 500ml": 60,
    "Herbata Czarna 100g": 70,
    "Shot Magnezowy 50ml": 25,
    "Kawa Ekskluzywna 1kg": 40,
    "Sok Z Buraka 500ml": 15,
    "Herbata Zimowa 100g": 110,
}

# Dane o klientach (dla testów retencji)
customer_data = {
    "CUST-001": {"name": "Jan Kowalski", "registration_date": month_ago},
    "CUST-002": {"name": "Anna Nowak", "registration_date": three_weeks_ago},
    "CUST-003": {"name": "Piotr Wiśniewski", "registration_date": two_weeks_ago},
    "CUST-004": {"name": "Maria Kaczmarek", "registration_date": week_ago},
    "CUST-005": {"name": "Tomasz Lewandowski", "registration_date": six_days_ago},
    "CUST-006": {"name": "Katarzyna Zielińska", "registration_date": four_days_ago},
    "CUST-007": {"name": "Michał Dąbrowski", "registration_date": three_days_ago},
    "CUST-008": {"name": "Agnieszka Kozłowska", "registration_date": two_days_ago},
    "CUST-009": {"name": "Paweł Jankowski", "registration_date": yesterday},
    "CUST-010": {"name": "Magdalena Mazur", "registration_date": today},
    # Dodatkowi klienci dla testów retencji
    "CUST-011": {"name": "Robert Krawczyk", "registration_date": month_ago},
    "CUST-012": {"name": "Ewa Piotrowska", "registration_date": three_weeks_ago},
    "CUST-013": {"name": "Marcin Grabowski", "registration_date": two_weeks_ago},
    "CUST-014": {"name": "Joanna Pawłowska", "registration_date": week_ago},
    "CUST-015": {"name": "Łukasz Michalski", "registration_date": six_days_ago},
}