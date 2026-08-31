# screen_akuisisi.py
# Screening 3: Sinyal akuisisi/korporasi, TANPA filter fundamental.
# Tujuannya nangkep saham yang fundamentalnya biasa aja tapi lagi
# ada "cerita" akuisisi/merger yang bisa jadi katalis harga naik.

import yfinance as yf
from config import SAHAM_ENERGI
from news_scanner import get_news_signal, _fetch_all_entries


def run_akuisisi_screening() -> list[dict]:
    hasil = []
    news_entries = _fetch_all_entries()

    for kode in SAHAM_ENERGI:
        news_signal = get_news_signal(kode, entries=news_entries)

        if not news_signal:
            continue  # cuma masukin saham yang KETEMU sinyal berita

        try:
            data = yf.Ticker(kode).history(period="5d")
            harga_terakhir = float(data["Close"].iloc[-1]) if not data.empty else None
        except Exception as e:
            print(f"[WARN] Gagal ambil harga {kode}: {e}")
            harga_terakhir = None

        hasil.append({
            "kode_saham": kode,
            "harga_terakhir": round(harga_terakhir, 2) if harga_terakhir else None,
            "news_signal": news_signal,
        })

    return hasil
