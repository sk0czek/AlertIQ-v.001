import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

load_dotenv()

try:
    from supabase import create_client, Client
except Exception:
    create_client = None
    Client = Any  # type: ignore


def get_supabase_client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
    if not url or not key:
        raise RuntimeError("Brak SUPABASE_URL lub SUPABASE_*_KEY w .env")
    if create_client is None:
        raise RuntimeError("Brak pakietu supabase. Dodaj go do requirements.txt")
    return create_client(url, key)


def list_active_users() -> List[Dict[str, Any]]:
    """Return users to process. Expected table: users(id, email, active, allegro_token_json, refresh_token, expires_at)"""
    sb = get_supabase_client()
    res = sb.table("users").select("id,email,active,allegro_token_json,refresh_token,expires_at").eq("active", True).execute()
    return res.data or []


def get_user_token(user: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    token = user.get("allegro_token_json")
    return token


def save_user_tokens(user_id: Any, token_payload: Dict[str, Any]):
    sb = get_supabase_client()
    sb.table("users").update({"allegro_token_json": token_payload, "refresh_token": token_payload.get("refresh_token"), "expires_at": token_payload.get("expires_at")}).eq("id", user_id).execute()


def upsert_user_tokens_by_email(email: str, token_payload: Dict[str, Any]):
    """Insert user if missing, update tokens if exists by email."""
    sb = get_supabase_client()
    # ensure expires_at exists
    if "expires_at" not in token_payload and token_payload.get("expires_in"):
        import time as _t
        token_payload["expires_at"] = int(_t.time()) + int(token_payload.get("expires_in", 43200))
    # Try update first
    res = sb.table("users").update({
        "allegro_token_json": token_payload,
        "refresh_token": token_payload.get("refresh_token"),
        "expires_at": token_payload.get("expires_at"),
        "active": True
    }).eq("email", email).execute()
    if res.data is None or len(res.data) == 0:
        # Insert if not exists
        sb.table("users").insert({
            "email": email,
            "active": True,
            "allegro_token_json": token_payload,
            "refresh_token": token_payload.get("refresh_token"),
            "expires_at": token_payload.get("expires_at")
        }).execute()

