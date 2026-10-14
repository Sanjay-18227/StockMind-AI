"""
Technical Analysis Indicators Engine:
Calculates SMA, EMA, RSI, MACD, Bollinger Bands, ATR, Momentum, Volatility, and Volume indicators.
Provides natural language interpretations for each indicator.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any
from utils.helpers import safe_float

def calculate_sma(series: pd.Series, period: int) -> pd.Series:
    """Simple Moving Average."""
    return series.rolling(window=period, min_periods=1).mean()

def calculate_ema(series: pd.Series, period: int) -> pd.Series:
    """Exponential Moving Average."""
    return series.ewm(span=period, adjust=False).mean()

def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """Wilder's Relative Strength Index."""
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    
    avg_gain = gain.ewm(alpha=1/period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period, adjust=False).mean()
    
    rs = avg_gain / (avg_loss + 1e-9)
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(series: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> tuple:
    """Moving Average Convergence Divergence."""
    ema_fast = calculate_ema(series, fast)
    ema_slow = calculate_ema(series, slow)
    macd_line = ema_fast - ema_slow
    signal_line = calculate_ema(macd_line, signal)
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

def calculate_bollinger_bands(series: pd.Series, period: int = 20, num_std: float = 2.0):
    """Bollinger Bands (Middle, Upper, Lower, Bandwidth, %B)."""
    middle = series.rolling(window=period, min_periods=1).mean()
    std = series.rolling(window=period, min_periods=1).std(ddof=0)
    upper = middle + (num_std * std)
    lower = middle - (num_std * std)
    bandwidth = ((upper - lower) / (middle + 1e-9)) * 100
    percent_b = (series - lower) / (upper - lower + 1e-9)
    return upper, middle, lower, bandwidth, percent_b

def calculate_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Average True Range."""
    high = df["High"]
    low = df["Low"]
    close = df["Close"]
    prev_close = close.shift(1)
    
    tr1 = high - low
    tr2 = (high - prev_close).abs()
    tr3 = (low - prev_close).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return tr.rolling(window=period, min_periods=1).mean()

def compute_all_indicators(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Compute full suite of technical indicators on a price DataFrame.
    Returns latest scalar values and historical series for plotting.
    """
    if df.empty or len(df) < 5:
        raise ValueError("Insufficient historical bars to compute technical indicators.")

    close = df["Close"]
    high = df["High"]
    low = df["Low"]
    volume = df["Volume"]
    current_price = safe_float(close.iloc[-1])

    # Moving Averages
    sma_20 = calculate_sma(close, 20)
    sma_50 = calculate_sma(close, 50)
    sma_100 = calculate_sma(close, 100)
    sma_200 = calculate_sma(close, 200)

    ema_9 = calculate_ema(close, 9)
    ema_20 = calculate_ema(close, 20)
    ema_50 = calculate_ema(close, 50)
    ema_200 = calculate_ema(close, 200)

    # RSI
    rsi = calculate_rsi(close, 14)
    latest_rsi = safe_float(rsi.iloc[-1], 50.0)

    # MACD
    macd_line, macd_sig, macd_hist = calculate_macd(close, 12, 26, 9)
    latest_macd = safe_float(macd_line.iloc[-1])
    latest_signal = safe_float(macd_sig.iloc[-1])
    latest_hist = safe_float(macd_hist.iloc[-1])

    # Bollinger Bands
    bb_upper, bb_mid, bb_lower, bb_width, bb_pct = calculate_bollinger_bands(close, 20, 2.0)
    latest_bb_upper = safe_float(bb_upper.iloc[-1])
    latest_bb_mid = safe_float(bb_mid.iloc[-1])
    latest_bb_lower = safe_float(bb_lower.iloc[-1])
    latest_bb_width = safe_float(bb_width.iloc[-1])
    latest_bb_pct = safe_float(bb_pct.iloc[-1])

    # ATR
    atr = calculate_atr(df, 14)
    latest_atr = safe_float(atr.iloc[-1])
    atr_percent = (latest_atr / (current_price + 1e-9)) * 100

    # Historical Volatility (20-day annualized)
    log_ret = np.log(close / close.shift(1))
    hist_vol = log_ret.rolling(window=20).std() * np.sqrt(252) * 100
    latest_vol = safe_float(hist_vol.iloc[-1], 20.0)

    # Volume Analysis
    vol_sma_20 = calculate_sma(volume, 20)
    latest_vol = safe_float(volume.iloc[-1])
    latest_vol_sma = safe_float(vol_sma_20.iloc[-1])
    volume_ratio = latest_vol / (latest_vol_sma + 1e-9)

    # Momentum (10-day Rate of Change)
    roc_10 = ((close - close.shift(10)) / (close.shift(10) + 1e-9)) * 100
    latest_momentum = safe_float(roc_10.iloc[-1])

    # Indicator Interpretations
    # RSI interpretation
    if latest_rsi >= 70:
        rsi_signal = "Overbought"
        rsi_desc = f"RSI is {latest_rsi:.1f}, signaling strong buying momentum, but entering commonly watched overbought territory where pullbacks may occur."
    elif latest_rsi <= 30:
        rsi_signal = "Oversold"
        rsi_desc = f"RSI is {latest_rsi:.1f}, indicating heavy recent selling pressure, placing the stock in oversold territory with potential for mean reversion."
    elif latest_rsi >= 55:
        rsi_signal = "Bullish"
        rsi_desc = f"RSI is {latest_rsi:.1f}, reflecting positive upward momentum above the neutral 50 centerline."
    elif latest_rsi <= 45:
        rsi_signal = "Bearish"
        rsi_desc = f"RSI is {latest_rsi:.1f}, reflecting prevailing downward momentum below the 50 centerline."
    else:
        rsi_signal = "Neutral"
        rsi_desc = f"RSI is {latest_rsi:.1f}, showing balanced supply and demand around neutral levels."

    # MACD interpretation
    if latest_hist > 0 and latest_macd > latest_signal:
        macd_desc = f"MACD line ({latest_macd:.2f}) is above Signal line ({latest_signal:.2f}) with a positive histogram (+{latest_hist:.2f}), confirming bullish momentum."
        macd_bias = "Bullish"
    elif latest_hist < 0 and latest_macd < latest_signal:
        macd_desc = f"MACD line ({latest_macd:.2f}) is below Signal line ({latest_signal:.2f}) with negative histogram ({latest_hist:.2f}), reflecting bearish momentum."
        macd_bias = "Bearish"
    else:
        macd_desc = f"MACD histogram is flat ({latest_hist:.2f}), showing momentum consolidation."
        macd_bias = "Neutral"

    # Moving Average positioning
    above_sma20 = current_price >= safe_float(sma_20.iloc[-1])
    above_sma50 = current_price >= safe_float(sma_50.iloc[-1])
    above_sma200 = current_price >= safe_float(sma_200.iloc[-1]) if len(df) >= 200 else None

    ma_summary = []
    if above_sma20:
        ma_summary.append("above 20-day SMA")
    else:
        ma_summary.append("below 20-day SMA")

    if above_sma50:
        ma_summary.append("above 50-day SMA")
    else:
        ma_summary.append("below 50-day SMA")

    if above_sma200 is not None:
        if above_sma200:
            ma_summary.append("above 200-day long-term baseline")
        else:
            ma_summary.append("below 200-day long-term baseline")

    trend_bias = "Bullish" if (above_sma20 and above_sma50) else ("Bearish" if (not above_sma20 and not above_sma50) else "Neutral / Mixed")

    return {
        "latest": {
            "current_price": current_price,
            "sma_20": round(safe_float(sma_20.iloc[-1]), 2),
            "sma_50": round(safe_float(sma_50.iloc[-1]), 2),
            "sma_100": round(safe_float(sma_100.iloc[-1]), 2) if len(df) >= 100 else None,
            "sma_200": round(safe_float(sma_200.iloc[-1]), 2) if len(df) >= 200 else None,
            "ema_9": round(safe_float(ema_9.iloc[-1]), 2),
            "ema_20": round(safe_float(ema_20.iloc[-1]), 2),
            "ema_50": round(safe_float(ema_50.iloc[-1]), 2),
            "ema_200": round(safe_float(ema_200.iloc[-1]), 2) if len(df) >= 200 else None,
            "rsi_14": round(latest_rsi, 2),
            "rsi_signal": rsi_signal,
            "rsi_desc": rsi_desc,
            "macd": round(latest_macd, 2),
            "macd_signal": round(latest_signal, 2),
            "macd_histogram": round(latest_hist, 2),
            "macd_desc": macd_desc,
            "macd_bias": macd_bias,
            "bollinger_upper": round(latest_bb_upper, 2),
            "bollinger_middle": round(latest_bb_mid, 2),
            "bollinger_lower": round(latest_bb_lower, 2),
            "bollinger_bandwidth_pct": round(latest_bb_width, 2),
            "bollinger_percent_b": round(latest_bb_pct, 2),
            "atr_14": round(latest_atr, 2),
            "atr_percent": round(atr_percent, 2),
            "historical_volatility": round(latest_vol, 2),
            "volume_ratio": round(volume_ratio, 2),
            "momentum_10d_pct": round(latest_momentum, 2),
            "trend_bias": trend_bias,
            "ma_summary": ", ".join(ma_summary)
        },
        "series": {
            "dates": [str(d.strftime("%Y-%m-%d")) for d in df.index],
            "close": [round(safe_float(x), 2) for x in close],
            "sma_20": [round(safe_float(x), 2) if not np.isnan(x) else None for x in sma_20],
            "sma_50": [round(safe_float(x), 2) if not np.isnan(x) else None for x in sma_50],
            "ema_20": [round(safe_float(x), 2) if not np.isnan(x) else None for x in ema_20],
            "rsi": [round(safe_float(x), 2) if not np.isnan(x) else None for x in rsi],
            "macd": [round(safe_float(x), 2) if not np.isnan(x) else None for x in macd_line],
            "macd_signal": [round(safe_float(x), 2) if not np.isnan(x) else None for x in macd_sig],
            "macd_hist": [round(safe_float(x), 2) if not np.isnan(x) else None for x in macd_hist],
            "bb_upper": [round(safe_float(x), 2) if not np.isnan(x) else None for x in bb_upper],
            "bb_lower": [round(safe_float(x), 2) if not np.isnan(x) else None for x in bb_lower]
        }
    }
