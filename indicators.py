

# indicators.py
# Fungsi-fungsi untuk menghitung indikator teknikal dari data harga historis.

import pandas as pd


def calc_rsi(close: pd.Series, period: int = 14) -> float:
    """Hitung RSI (Relative Strength Index) dari data harga penutupan."""
    delta = close.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss.replace(0, 1e-10)
    rsi = 100 - (100 / (1 + rs))
    return round(float(rsi.iloc[-1]), 2) if not rsi.empty else None


def calc_ma(close: pd.Series, period: int) -> float:
    """Hitung Moving Average sederhana."""
    if len(close) < period:
        return None
    return round(float(close.rolling(window=period).mean().iloc[-1]), 2)


def calc_volume_ratio(volume: pd.Series, period: int = 20) -> float:
    """Bandingkan volume hari terakhir dengan rata-rata N hari sebelumnya."""
    if len(volume) < period + 1:
        return None
    avg_vol = volume.iloc[-period - 1:-1].mean()
    last_vol = volume.iloc[-1]
    if avg_vol == 0:
        return None
    return round(float(last_vol / avg_vol), 2)


def is_golden_cross(close: pd.Series) -> bool:
    """
    Deteksi golden cross: MA50 baru saja menembus ke atas MA200
    (dibandingkan antara hari ini dan kemarin).
    """
    if len(close) < 201:
        return False
    ma50 = close.rolling(window=50).mean()
    ma200 = close.rolling(window=200).mean()

    today_above = ma50.iloc[-1] > ma200.iloc[-1]
    yesterday_above = ma50.iloc[-2] > ma200.iloc[-2]

    return bool(today_above and not yesterday_above)


def calc_trade_levels(entry_price: float, stop_loss_pct: float, tp1_rr: float, tp2_rr: float) -> dict:
    """
    Hitung level entry, stop loss, dan take profit berdasarkan rasio risk-reward.
    Ini murni perhitungan matematis, bukan sinyal/nasihat keuangan.
    """
    stop_loss = entry_price * (1 - stop_loss_pct)
    risk = entry_price - stop_loss

    return {
        "entry": round(entry_price, 2),
        "stop_loss": round(stop_loss, 2),
        "take_profit_1": round(entry_price + risk * tp1_rr, 2),
        "take_profit_2": round(entry_price + risk * tp2_rr, 2),
    }


def calc_fibonacci_levels(high: pd.Series, low: pd.Series, lookback: int = 90) -> dict:
    """
    Hitung level Fibonacci Retracement dari swing tertinggi & terendah
    dalam periode lookback (default 90 hari terakhir).

    Level umum yang dipakai: 23.6%, 38.2%, 50%, 61.8%, 78.6%.
    Level ini sering dipakai sebagai area support/resistance potensial.
    """
    recent_high = high.iloc[-lookback:]
    recent_low = low.iloc[-lookback:]

    swing_high = float(recent_high.max())
    swing_low = float(recent_low.min())
    range_diff = swing_high - swing_low

    if range_diff == 0:
        return None

    return {
        "swing_high": round(swing_high, 2),
        "swing_low": round(swing_low, 2),
        "fib_23.6": round(swing_high - range_diff * 0.236, 2),
        "fib_38.2": round(swing_high - range_diff * 0.382, 2),
        "fib_50": round(swing_high - range_diff * 0.5, 2),
        "fib_61.8": round(swing_high - range_diff * 0.618, 2),
        "fib_78.6": round(swing_high - range_diff * 0.786, 2),
    }


def nearest_fib_level(current_price: float, fib_levels: dict) -> str:
    """
    Cari level Fibonacci mana yang paling deket sama harga sekarang.
    Berguna buat tau saham lagi 'nempel' di level support/resistance mana.
    """
    if not fib_levels:
        return None

    candidates = {k: v for k, v in fib_levels.items() if k.startswith("fib_")}
    closest_key = min(candidates, key=lambda k: abs(candidates[k] - current_price))
    return closest_key.replace("fib_", "") + "%"
