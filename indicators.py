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
