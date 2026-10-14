"""
Global Market Data Engine: Tracks key Indian and International market indices.
Calculates broad market sentiment, volatility, and trends.
"""

import yfinance as yf
import numpy as np
import pandas as pd
from typing import Dict, Any, List
from utils.helpers import cache, safe_float, format_percent

MAJOR_INDICES = [
    {"name": "NIFTY 50", "ticker": "^NSEI", "region": "India", "currency": "INR", "currency_symbol": "₹"},
    {"name": "SENSEX", "ticker": "^BSESN", "region": "India", "currency": "INR", "currency_symbol": "₹"},
    {"name": "NIFTY BANK", "ticker": "^NSEBANK", "region": "India", "currency": "INR", "currency_symbol": "₹"},
    {"name": "S&P 500", "ticker": "^GSPC", "region": "US / Global", "currency": "USD", "currency_symbol": "$"},
    {"name": "NASDAQ", "ticker": "^IXIC", "region": "US / Global", "currency": "USD", "currency_symbol": "$"},
    {"name": "Dow Jones", "ticker": "^DJI", "region": "US / Global", "currency": "USD", "currency_symbol": "$"}
]

def get_market_overview() -> Dict[str, Any]:
    """
    Fetch live/latest data for all major indices, compute sentiment, volatility, and market summary.
    """
    cache_key = "global_market_overview"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    indices_data = []
    bullish_count = 0
    bearish_count = 0
    neutral_count = 0

    for item in MAJOR_INDICES:
        name = item["name"]
        ticker_sym = item["ticker"]
        try:
            t = yf.Ticker(ticker_sym)
            hist = t.history(period="1mo")
            if hist.empty or len(hist) < 2:
                continue

            closes = hist["Close"].values
            curr = safe_float(closes[-1])
            prev = safe_float(closes[-2])
            change = curr - prev
            pct_change = (change / prev) * 100 if prev > 0 else 0.0

            # 20-day annualized volatility
            if len(closes) >= 5:
                daily_returns = np.diff(closes) / closes[:-1]
                volatility_20d = safe_float(np.std(daily_returns) * np.sqrt(252) * 100)
            else:
                volatility_20d = 0.0

            # Trend & Sentiment
            # If > +0.3% Bullish, < -0.3% Bearish, otherwise Neutral
            if pct_change >= 0.3:
                sentiment = "Bullish"
                bullish_count += 1
            elif pct_change <= -0.3:
                sentiment = "Bearish"
                bearish_count += 1
            else:
                sentiment = "Neutral"
                neutral_count += 1

            # 52w high and low
            high_1y = safe_float(hist["High"].max())
            low_1y = safe_float(hist["Low"].min())

            indices_data.append({
                "name": name,
                "ticker": ticker_sym,
                "region": item["region"],
                "currency": item["currency"],
                "currency_symbol": item["currency_symbol"],
                "current_price": round(curr, 2),
                "previous_close": round(prev, 2),
                "change": round(change, 2),
                "change_percent": round(pct_change, 2),
                "change_formatted": format_percent(pct_change),
                "sentiment": sentiment,
                "volatility_20d": round(volatility_20d, 2),
                "high_1m": round(high_1y, 2),
                "low_1m": round(low_1y, 2)
            })
        except Exception:
            # Avoid failing entire overview if one index fails
            continue

    # Determine broad market mood
    total_valid = len(indices_data)
    if total_valid == 0:
        overall_sentiment = "Neutral"
        sentiment_summary = "Market data temporarily unavailable. Please retry shortly."
    else:
        if bullish_count > bearish_count and bullish_count >= total_valid / 2:
            overall_sentiment = "Bullish"
            sentiment_summary = f"Markets are leaning positive today with {bullish_count} of {total_valid} benchmark indices trading in the green."
        elif bearish_count > bullish_count and bearish_count >= total_valid / 2:
            overall_sentiment = "Bearish"
            sentiment_summary = f"Markets face selling pressure today with {bearish_count} of {total_valid} benchmark indices in the red."
        else:
            overall_sentiment = "Mixed / Neutral"
            sentiment_summary = f"Markets are showing mixed, range-bound price action across major domestic and global indices."

    result = {
        "indices": indices_data,
        "overall_sentiment": overall_sentiment,
        "sentiment_summary": sentiment_summary,
        "bullish_count": bullish_count,
        "bearish_count": bearish_count,
        "neutral_count": neutral_count,
        "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    cache.set(cache_key, result, ttl=90)
    return result
