import requests
import time
import base64
import json
from dotenv import load_dotenv
import os

load_dotenv()
CLIENT_ID = os.getenv("ALLEGRO_CLIENT_ID")
CLIENT_SECRET = os.getenv("ALLEGRO_CLIENT_SECRET")

ALLEGRO_API_URL = "https://allegro.pl"


def get_device_code():
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode()}"
    }

    data = {
        "client_id": CLIENT_ID
    }

    response = requests.post(
        f"{ALLEGRO_API_URL}/auth/oauth/device",
        data=data,
        headers=headers
    )
    response.raise_for_status()
    return response.json()


def poll_for_token(device_code, interval):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode()}"
    }

    data = {
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        "device_code": device_code
    }

    print("\n⏳ Oczekiwanie na autoryzację użytkownika...")

    while True:
        response = requests.post(
            f"{ALLEGRO_API_URL}/auth/oauth/token",
            data=data,
            headers=headers
        )

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            error = response.json().get("error")
            if error == "authorization_pending":
                time.sleep(interval)
            elif error == "slow_down":
                interval += 5
                time.sleep(interval)
            else:
                raise Exception(f"Błąd autoryzacji: {error}")
        else:
            raise Exception(f"Błąd HTTP: {response.status_code}")


def save_tokens(tokens, filename="allegro_tokens.json"):
    tokens["expires_at"] = int(time.time()) + tokens.get("expires_in", 43200)
    with open(filename, "w") as f:
        json.dump(tokens, f, indent=2)
    print(f"\n✅ Tokeny zapisane do pliku {filename}")

def refresh_access_token(refresh_token, filename="allegro_tokens.json"):
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{CLIENT-ID}:{CLIENT_SECRET}'.encode()).decode()}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    resposne = requests.post(
        f"{ALLERGRO_API_URL}/auth/oauth/token",
        data=data,
        headers=headers
    )

    if response.status_code == 200:
        tokens=response.json()
        save_tokens(tokens, filename)
        print("🔁 Token został odświeżony.")
        return tokens
    else:
        raise Exception(f"❌ Błąd odświeżania tokena: {response.status_code}, {response.text}")

def load_tokens(filename="allegro_tokens.json"):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Plik z tokenami '{filename}' nie istenieje.")
    
    with open(filename, "r") as file:
        return json.load(file)

def get_valid_access_token():
    tokens = load_tokens()
    access_token = tokens.get("access_token")
    expires_at = tokens.get("expires_at")

    if not expires_at or time.time() >= expires_at:
        print("⚠️ Access token wygasł – odświeżam...")
        tokens = refresh_access_token(tokens["refresh_token"])
        access_token = tokens["access_token"]
    
    return access_token


def main():
    print("🔐 Rozpoczynanie uwierzytelniania Device Flow...")

    device_data = get_device_code()
    print("\n📱 Przejdź do:")
    print(f"{device_data['verification_uri_complete']}")
    print(f"Lub wejdź na {device_data['verification_uri']} i wpisz kod: {device_data['user_code']}")

    tokens = poll_for_token(device_data["device_code"], device_data["interval"])
    save_tokens(tokens)

    print("\n🎉 Autoryzacja zakończona pomyślnie!")
    print(f"Access token: {tokens['access_token'][:10]}...")  # skrócony do podglądu

if __name__ == "__main__":
    main()
