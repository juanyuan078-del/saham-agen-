# supabase_client.py
# Koneksi ke Supabase & fungsi simpan hasil screening.

import os
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")


def get_client() -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError(
            "SUPABASE_URL dan SUPABASE_KEY belum diset di environment variables."
        )
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def save_longterm_results(rows: list[dict]):
    if not rows:
        return
    client = get_client()
    client.table("screening_longterm").insert(rows).execute()


def save_trading_results(rows: list[dict]):
    if not rows:
        return
    client = get_client()
    client.table("screening_trading").insert(rows).execute()
