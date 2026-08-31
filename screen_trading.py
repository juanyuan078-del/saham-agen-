# screen_trading.py
# Screening 2: Momentum/trading berdasarkan RSI, MA, volume, golden cross.

import yfinance as yf
from config import SAHAM_ENERGI, TRADING_CRITERIA, RISK_REWARD
from indicators import (
    calc_rsi, calc_ma, calc_volume_ratio, is_golden_cross,
    calc_trade_levels, calc_fibonacci_levels, nearest_fib_level,
)


def run_trading_screening() -> list[dict]:
    hasil = []

    for kode in SAHAM_ENERGI:
        try:
            data = yf.Ticker(kode).history(period="1y")
            if data.empty or len(data) < 60:
                print(f"[SKIP] {kode}: data harga gak cukup")
                continue

            close = data["Close"]
            high = data["High"]
            low = data["Low"]
            volume = data["Volume"]

            rsi = calc_rsi(close)
            ma50 = calc_ma(close, 50)
            ma200 = calc_ma(close, 200)
            vol_ratio = calc_volume_ratio(volume)
            golden_cross = is_golden_cross(close)
            fib_levels = calc_fibonacci_levels(high, low, lookback=90)

            if rsi is None:
                continue

            lolos_rsi = (
                TRADING_CRITERIA["rsi_min"] <= rsi <= TRADING_CRITERIA["rsi_max"]
            )
            lolos_volume = (
                vol_ratio is not None
                and vol_ratio >= TRADING_CRITERIA["volume_ratio_min"]
            )

            # Lolos kalau: RSI di range momentum ATAU ada golden cross,
            # DITAMBAH volume lagi ramai
            if (lolos_rsi or golden_cross) and lolos_volume:
                harga_terakhir = float(close.iloc[-1])
                levels = calc_trade_levels(
                    entry_price=harga_terakhir,
                    stop_loss_pct=RISK_REWARD["stop_loss_pct"],
                    tp1_rr=RISK_REWARD["tp1_rr"],
                    tp2_rr=RISK_REWARD["tp2_rr"],
                )

                hasil.append({
                    "kode_saham": kode,
                    "rsi": rsi,
                    "ma50": ma50,
                    "ma200": ma200,
                    "volume_ratio": vol_ratio,
                    "golden_cross": golden_cross,
                    "entry_price": levels["entry"],
                    "stop_loss": levels["stop_loss"],
                    "take_profit_1": levels["take_profit_1"],
                    "take_profit_2": levels["take_profit_2"],
                    "fib_support": fib_levels["fib_61.8"] if fib_levels else None,
                    "fib_resistance": fib_levels["fib_38.2"] if fib_levels else None,
                    "fib_nearest": nearest_fib_level(harga_terakhir, fib_levels) if fib_levels else None,
                })

        except Exception as e:
            print(f"[ERROR] {kode}: {e}")
            continue

    return hasil
