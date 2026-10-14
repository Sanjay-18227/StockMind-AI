"""
Live Signal & Stock Analysis Pipeline:
Orchestrates quote fetching, indicators, statistics, support/resistance, risk,
ML predictions, and educational strategy into a unified analysis bundle.
"""

from typing import Dict, Any, Optional
from data.market_data import get_stock_quote, get_historical_data, resolve_ticker
from data.global_market_data import MAJOR_INDICES
from analysis.indicators import compute_all_indicators
from analysis.support_resistance import compute_support_resistance
from analysis.statistics import compute_historical_statistics
from analysis.risk import assess_stock_risk
from analysis.signal_engine import generate_market_scenarios
from model.predict import generate_stock_predictions
from utils.helpers import cache, safe_float
from ui.charts import build_candlestick_chart_payload
from ui.components import build_dashboard_cards

def run_complete_stock_analysis(symbol_or_query: str, period: str = "1y") -> Dict[str, Any]:
    """
    Executes full pipeline for a stock and returns complete quantitative results.
    """
    ticker = resolve_ticker(symbol_or_query)
    cache_key = f"full_analysis_{ticker}_{period}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    # 1. Fetch quote
    quote = get_stock_quote(ticker)
    
    # 2. Fetch history: use at least 1y for robust indicator & ML model calibration
    fetch_period = "1y" if period in ["1d", "5d", "1mo", "3mo", "6mo"] else period
    hist_df = get_historical_data(ticker, period=fetch_period, interval="1d")
    
    # 3. Fetch benchmark history for Beta/Correlation
    benchmark_ticker = "^NSEI" if quote["currency"] == "INR" else "^GSPC"
    try:
        benchmark_df = get_historical_data(benchmark_ticker, period=fetch_period, interval="1d")
    except Exception:
        benchmark_df = None

    # 4. Technical indicators
    indicators = compute_all_indicators(hist_df)
    latest_ind = indicators["latest"]

    # 5. Support and resistance
    sr_levels = compute_support_resistance(hist_df)

    # 6. Historical statistics
    stats = compute_historical_statistics(hist_df, benchmark_df=benchmark_df)

    # 7. Multi-factor Risk Assessment
    risk = assess_stock_risk(
        annualized_volatility=stats["annualized_volatility_pct"],
        atr_percent=latest_ind["atr_percent"],
        max_drawdown=stats["max_drawdown_pct"],
        beta=stats["beta"],
        trend_bias=latest_ind["trend_bias"],
        volume_ratio=latest_ind["volume_ratio"]
    )

    # 8. Machine Learning Prediction & Forecast Trajectory
    prediction = generate_stock_predictions(hist_df)

    # 9. Market Scenarios & Actionable Strategy Setup
    scenarios_and_strategy = generate_market_scenarios(
        current_price=quote["current_price"],
        nearest_support=sr_levels["nearest_support"],
        secondary_support=sr_levels["secondary_support"],
        nearest_resistance=sr_levels["nearest_resistance"],
        secondary_resistance=sr_levels["secondary_resistance"],
        trend_bias=latest_ind["trend_bias"],
        rsi=latest_ind["rsi_14"],
        macd_bias=latest_ind["macd_bias"],
        atr=latest_ind["atr_14"]
    )

    # 10. Generate chart payload and dashboard cards
    display_df = hist_df
    display_indicators = indicators
    slice_map = {"1d": 5, "5d": 5, "1mo": 22, "3mo": 66, "6mo": 132}
    if period in slice_map:
        n = min(len(hist_df), slice_map[period])
        display_df = hist_df.iloc[-n:]
        sliced_series = {k: v[-n:] if isinstance(v, list) else v for k, v in indicators.get("series", {}).items()}
        display_indicators = {"latest": indicators["latest"], "series": sliced_series}

    chart_payload = build_candlestick_chart_payload(display_df, display_indicators, sr_levels, prediction)

    result = {
        "quote": quote,
        "indicators": indicators,
        "support_resistance": sr_levels,
        "statistics": stats,
        "risk": risk,
        "prediction": prediction,
        "scenarios": scenarios_and_strategy["scenarios"],
        "strategy": scenarios_and_strategy["strategy"],
        "historical_series": display_indicators["series"],
        "chart_payload": chart_payload
    }
    result["dashboard_cards"] = build_dashboard_cards(result)

    # Cache for 120 seconds
    cache.set(cache_key, result, ttl=120)
    return result
