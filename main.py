# main.py
# Entry point. Dipanggil oleh GitHub Actions dengan argumen "longterm" atau "trading".

import sys
from screen_longterm import run_longterm_screening
from screen_trading import run_trading_screening
from supabase_client import save_longterm_results, save_trading_results
from telegram_notify import (
    send_message,
    format_longterm_message,
    format_trading_message,
)


def run_longterm():
    print("Menjalankan screening jangka panjang...")
    hasil = run_longterm_screening()
    print(f"Ditemukan {len(hasil)} saham lolos.")

    save_longterm_results(hasil)
    pesan = format_longterm_message(hasil)
    send_message(pesan)


def run_trading():
    print("Menjalankan screening trading...")
    hasil = run_trading_screening()
    print(f"Ditemukan {len(hasil)} saham lolos.")

    save_trading_results(hasil)
    pesan = format_trading_message(hasil)
    send_message(pesan)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "trading"

    if mode == "longterm":
        run_longterm()
    elif mode == "trading":
        run_trading()
    else:
        print("Mode gak dikenali. Pakai: python main.py [longterm|trading]")
