import requests
import json
import os
from datetime import datetime
from get_token import get_valid_access_token

try:
    from zoneinfo import ZoneInfo 
except Exception:  
    try:
        from backports.zoneinfo import ZoneInfo
    except Exception:
        ZoneInfo = None

ALLEGRO_API_URL = "https://api.allegro.pl"
TOKEN_FILE = "allegro_tokens.json"
DEFAULT_TZ = os.getenv("ALLEGRO_TZ", "Europe/Warsaw")

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

def _parse_date_to_local(date_str: str) -> datetime.date:
    utc_dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    try:
        local_dt = utc_dt.astimezone(ZoneInfo(DEFAULT_TZ)) if ZoneInfo else utc_dt
    except Exception:
        local_dt = utc_dt
    return local_dt.date()


def fetch_orders_data():
    access_token = get_valid_access_token()
    events_data = get_order_events(access_token)

    seen_ids = set()
    result = []

    for event in events_data.get("events", []):
        form_id = event["checkoutForm"]["id"]
        if form_id not in seen_ids:
            seen_ids.add(form_id)
            form = get_checkout_form(access_token, form_id)

            order_date = _parse_date_to_local(form["updatedAt"])

            for line in form["lineItems"]:
                result.append({
                    "data": order_date,
                    "order_id": form_id,
                    "produkt": line["offer"]["name"],
                    "sprzedano": line["quantity"],
                    "cena_jednostkowa": float(line["price"]["amount"]),
                })

    return result
