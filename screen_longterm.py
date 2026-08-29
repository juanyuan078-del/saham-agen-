# screen_longterm.py
# Screening 1: Value investing + fokus sektor energi + sinyal akuisisi.

import yfinance as yf
from config import SAHAM_ENERGI, LONGTERM_CRITERIA
from news_scanner import get_news_signal, _fetch_all_entries


def run_longterm_screening() -> list[dict]:
    hasil = []
    news_entries = _fetch_all_entries()  # ambil sekali, dipakai buat semua saham

    for kode in SAHAM_ENERGI:
        try:
            ticker = yf.Ticker(kode)
            info = ticker.info

            per = info.get("trailingPE")
            pbv = info.get("priceToBook")
            roe = info.get("returnOnEquity")
            der = info.get("debtToEquity")
            div_yield = info.get("dividendYield")

            # Skip kalau data penting gak lengkap
            if per is None or roe is None:
                print(f"[SKIP] {kode}: data fundamental gak lengkap")
                continue

            # der dari yfinance biasanya dalam bentuk persen (misal 45.2 = 45.2%)
            der_ratio = (der / 100) if der is not None else None

            lolos = (
                per <= LONGTERM_CRITERIA["per_max"]
                and (pbv is None or pbv <= LONGTERM_CRITERIA["pbv_max"])
                and roe >= LONGTERM_CRITERIA["roe_min"]
                and (der_ratio is None or der_ratio <= LONGTERM_CRITERIA["der_max"])
            )

            if not lolos:
                continue

            news_signal = get_news_signal(kode, entries=news_entries)

            hasil.append({
                "kode_saham": kode,
                "sektor": "Energi",
                "per": round(per, 2) if per else None,
                "roe": round(roe, 4) if roe else None,
                "der": round(der_ratio, 2) if der_ratio else None,
                "dividend_yield": round(div_yield, 4) if div_yield else None,
                "free_float": None,  # yfinance gak selalu punya data ini utk saham IDX
                "news_signal": news_signal,
            })

        except Exception as e:
            print(f"[ERROR] {kode}: {e}")
            continue

    return hasil
