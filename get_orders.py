import requests
import json
from datetime import datetime
from dotenv import load_dotenv

ALLEGRO_API_URL = "https://api.allegro.pl"
TOKEN_FILE = "allegro_tokens.json"

def load_access_token():
    with open(TOKEN_FILE, "r") as f:
        tokens = json.load(f)
    return tokens["access_token"]

def get_order_events(access_token, limit=100):
    url = f"{ALLEGRO_API_URL}/order/events"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.allegro.public.v1+json"
    }
    params = {
        "type": "READY_FOR_PROCESSING",
        "limit": limit
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def get_checkout_form(access_token, checkout_form_id):
    url = f"{ALLEGRO_API_URL}/order/checkout-forms/{checkout_form_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.allegro.public.v1+json"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def fetch_orders_data():
    access_token = load_access_token()
    events_data = get_order_events(access_token)

    seen_ids = set()
    result = []

    for event in events_data["events"]:
        form_id = event["checkoutForm"]["id"]
        if form_id not in seen_ids:
            seen_ids.add(form_id)
            form = get_checkout_form(access_token, form_id)

            order_date = datetime.fromisoformat(form['updatedAt'].replace("Z", "+00:00")).date()

            for line in form["lineItems"]:
                result.append({
                    "data": order_date,
                    "produkt": line["offer"]["name"],
                    "sprzedano": line["quantity"],
                    "cena_jednostkowa": float(line["price"]["amount"])
                })

    return result
