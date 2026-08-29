# telegram_notify.py
# Kirim pesan notifikasi ke Telegram bot.

import os
import requests

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


def send_message(text: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram token/chat_id belum diset, skip notifikasi.")
        print(text)
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
    }
    resp = requests.post(url, json=payload, timeout=15)
    if resp.status_code != 200:
        print(f"Gagal kirim Telegram: {resp.status_code} - {resp.text}")


def format_longterm_message(hasil: list[dict]) -> str:
    if not hasil:
        return "📊 *[LONG-TERM/ENERGI]*\nGak ada saham yang lolos kriteria hari ini."

    lines = ["📊 *[LONG-TERM/ENERGI]* Hasil Screening\n"]
    for r in hasil:
        news_tag = f"\n🔥 Cerita: {r['news_signal']}" if r.get("news_signal") else ""
        lines.append(
            f"*{r['kode_saham']}*\n"
            f"PER: {r.get('per', '-')} | ROE: {r.get('roe', '-')} | "
            f"DER: {r.get('der', '-')} | Div: {r.get('dividend_yield', '-')}"
            f"{news_tag}\n"
        )
    return "\n".join(lines)


def format_trading_message(hasil: list[dict]) -> str:
    if not hasil:
        return "📈 *[TRADING]*\nGak ada saham yang lolos kriteria hari ini."

    lines = ["📈 *[TRADING]* Hasil Screening\n"]
    for r in hasil:
        gc = "✅" if r.get("golden_cross") else "-"
        lines.append(
            f"*{r['kode_saham']}*\n"
            f"RSI: {r.get('rsi', '-')} | MA50: {r.get('ma50', '-')} | "
            f"MA200: {r.get('ma200', '-')} | Golden Cross: {gc}\n"
        )
    return "\n".join(lines)
