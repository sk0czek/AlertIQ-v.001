from analyzer import generate_report
from get_orders import fetch_orders_data
from mailer import send_report_email
from get_token import get_valid_access_token, get_valid_access_token_from_dict, refresh_tokens_dict
from datetime import timedelta, date
import os
from dotenv import load_dotenv
from test_data import test_data, views_data, customer_data
from db import list_active_users, get_user_token

load_dotenv()

def main():
    report_date = date.today() - timedelta(days=1)

    users = []
    try:
        users = list_active_users()
    except Exception as e:
        print(f"❌ Brak połączenia z Supabase lub konfiguracji: {e}")
        print("➡️ Fallback do pojedynczego użytkownika z .env")
        try:
            access_token = get_valid_access_token()
            data = fetch_orders_data(access_token)
        except Exception:
            data = []
        klient = os.getenv("EMAIL_TO", "test@example.com")
        raport = generate_report(test_data if not data else data, report_date, views_data, customer_data)
        subject = f"AlertIQ – Raport Dzienny {report_date.strftime('%d.%m.%Y') }"
        send_report_email(klient, subject, raport)
        print("✅ Raport wysłany (tryb single-user)")
        return

    for user in users:
        try:
            email = user.get("email") or os.getenv("EMAIL_TO", "test@example.com")
            token_dict = get_user_token(user)
            try:
                access_token, updated_tokens = get_valid_access_token_from_dict(token_dict)
                
                # Jeśli tokeny zostały odświeżone, zapisz je do bazy
                if updated_tokens:
                    from db import save_user_tokens
                    save_user_tokens(user.get("id"), updated_tokens)
                    print("✅ Odświeżone tokeny zostały zapisane do bazy danych")
                    
            except ValueError as e:
                print(f"❌ Błąd tokenów dla użytkownika {email}: {e}")
                continue
            except Exception as e:
                print(f"⚠️ Problem z tokenem dla użytkownika {email}, próbuję odświeżyć: {e}")
                try:
                    # try full refresh and persist in Supabase
                    from db import save_user_tokens
                    refreshed_tokens = refresh_tokens_dict(token_dict)
                    save_user_tokens(user.get("id"), refreshed_tokens)
                    access_token = refreshed_tokens.get("access_token")
                    print("✅ Token został odświeżony i zapisany")
                except Exception as refresh_error:
                    print(f"❌ Nie udało się odświeżyć tokenu dla użytkownika {email}: {refresh_error}")
                    continue

            print(f"📊 Pobieranie danych zamówień dla użytkownika {email}...")
            data = fetch_orders_data(access_token)

            print("📈 Generowanie raportu...")
            raport = generate_report(test_data if not data else data, report_date, views_data, customer_data)

            subject = f"AlertIQ – Raport Dzienny {report_date.strftime('%d.%m.%Y') }"
            print("📧 Wysyłanie raportu...")
            send_report_email(email, subject, raport)
            print(f"✅ Raport został wysłany do {email}")
        except Exception as e:
            print(f"❌ Błąd przetwarzania użytkownika {user.get('email')}: {e}")

if __name__ == "__main__":
    main()