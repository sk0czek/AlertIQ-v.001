from datetime import date, timedelta

today = date.today()
yesterday = today - timedelta(days=1)
two_days_ago = today - timedelta(days=2)
three_days_ago = today - timedelta(days=3)
four_days_ago = today - timedelta(days=4)
five_days_ago = today - timedelta(days=5)
six_days_ago = today - timedelta(days=6)
week_ago = today - timedelta(days=7)

test_data = [
    # Bestseler z historią
    {"data": week_ago, "produkt": "Kawa Arabica", "sprzedano": 5, "cena_jednostkowa": 25.0},
    {"data": six_days_ago, "produkt": "Kawa Arabica", "sprzedano": 3, "cena_jednostkowa": 25.0},
    {"data": four_days_ago, "produkt": "Kawa Arabica", "sprzedano": 6, "cena_jednostkowa": 25.0},
    {"data": yesterday, "produkt": "Kawa Arabica", "sprzedano": 5, "cena_jednostkowa": 25.0},
    {"data": today, "produkt": "Kawa Arabica", "sprzedano": 7, "cena_jednostkowa": 25.0},

    # Produkt, który przestał się sprzedawać
    {"data": six_days_ago, "produkt": "Herbata Zielona", "sprzedano": 3, "cena_jednostkowa": 12.5},
    {"data": four_days_ago, "produkt": "Herbata Zielona", "sprzedano": 2, "cena_jednostkowa": 12.5},
    {"data": yesterday, "produkt": "Herbata Zielona", "sprzedano": 4, "cena_jednostkowa": 12.5},

    # Nowy produkt dziś
    {"data": today, "produkt": "Nowy Energy Drink", "sprzedano": 10, "cena_jednostkowa": 6.0},
    {"data": today, "produkt": "Nowy Energy Drink", "sprzedano": 5, "cena_jednostkowa": 6.0},

    # Kolejny nowy produkt dziś
    {"data": today, "produkt": "Shot Imbirowy", "sprzedano": 2, "cena_jednostkowa": 5.5},

    # Slow seller – Sok Marchewkowy
    {"data": five_days_ago, "produkt": "Sok Marchewkowy", "sprzedano": 1, "cena_jednostkowa": 8.0},
    {"data": three_days_ago, "produkt": "Sok Marchewkowy", "sprzedano": 1, "cena_jednostkowa": 8.0},
    {"data": today, "produkt": "Sok Marchewkowy", "sprzedano": 1, "cena_jednostkowa": 8.0},

    # Średnio rotujący produkt – Baton
    {"data": week_ago, "produkt": "Baton Proteinowy", "sprzedano": 2, "cena_jednostkowa": 4.0},
    {"data": two_days_ago, "produkt": "Baton Proteinowy", "sprzedano": 3, "cena_jednostkowa": 4.0},
    {"data": yesterday, "produkt": "Baton Proteinowy", "sprzedano": 2, "cena_jednostkowa": 4.0},
    {"data": today, "produkt": "Baton Proteinowy", "sprzedano": 3, "cena_jednostkowa": 4.0},

    # Inny wolny produkt – Shot Magnezowy
    {"data": six_days_ago, "produkt": "Shot Magnezowy", "sprzedano": 1, "cena_jednostkowa": 5.5},
    {"data": three_days_ago, "produkt": "Shot Magnezowy", "sprzedano": 1, "cena_jednostkowa": 5.5},

    # Inny aktywny produkt – Woda Kokosowa
    {"data": yesterday, "produkt": "Woda Kokosowa", "sprzedano": 4, "cena_jednostkowa": 7.5},
    {"data": today, "produkt": "Woda Kokosowa", "sprzedano": 5, "cena_jednostkowa": 7.5},

    # Historia produktu który się kończy – Sok Pomidorowy
    {"data": six_days_ago, "produkt": "Sok Pomidorowy", "sprzedano": 2, "cena_jednostkowa": 6.5},
    {"data": five_days_ago, "produkt": "Sok Pomidorowy", "sprzedano": 2, "cena_jednostkowa": 6.5},
    {"data": four_days_ago, "produkt": "Sok Pomidorowy", "sprzedano": 1, "cena_jednostkowa": 6.5},
]