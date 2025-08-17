from analyzer import generate_report
from get_orders import fetch_orders_data
from mailer import send_report_email
from get_token import get_valid_access_token
from datetime import timedelta, date
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    # Automatyczne odświeżanie tokenów
    print("🔐 Sprawdzanie i odświeżanie tokenów...")
    try:
        access_token = get_valid_access_token()
        print("✅ Tokeny są aktualne")
    except Exception as e:
        print(f"❌ Błąd z tokenami: {e}")
        print("Uruchom get_token.py aby uzyskać nowe tokeny")
        return

    today = date.today()
    
    # Pobierz adres email z zmiennych środowiskowych
    klient = os.getenv("EMAIL_TO", "")
    if not klient:
        print("⚠️ Brak EMAIL_TO w .env - raport nie zostanie wysłany")
        klient = "test@example.com"  # fallback
    
    print("📊 Pobieranie danych zamówień...")
    data = fetch_orders_data()
    
    print("📈 Generowanie raportu...")
    raport = generate_report(data, today)
    
    subject = f"AlertIQ – Raport Dzienny {today.strftime('%d.%m.%Y') }"
    
    print("📧 Wysyłanie raportu...")
    send_report_email(klient, subject, raport)
    
    print("✅ Raport został wygenerowany i wysłany!")

if __name__ == "__main__":
    main()