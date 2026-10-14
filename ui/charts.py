"""
Chart Generation Engine:
Produces structured chart data for Interactive Candlestick charts, Overlays (SMA, EMA, Bollinger Bands),
Volume profiles, Forecast Trajectories with Uncertainty Cones, and Normalized Comparison graphs.
"""

from typing import Dict, Any, List, Optional

def build_candlestick_chart_payload(hist_df, indicators_dict: Dict[str, Any], sr_dict: Dict[str, Any], prediction_dict: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Format OHLCV, indicator lines, S&R lines, and forecast trajectory for frontend rendering.
    """
    dates = [d.strftime("%Y-%m-%d") for d in hist_df.index]
    opens = [round(float(x), 2) for x in hist_df["Open"]]
    highs = [round(float(x), 2) for x in hist_df["High"]]
    lows = [round(float(x), 2) for x in hist_df["Low"]]
    closes = [round(float(x), 2) for x in hist_df["Close"]]
    volumes = [int(x) for x in hist_df["Volume"]]

    series = indicators_dict.get("series", {})

    payload = {
        "dates": dates,
        "ohlc": {
            "open": opens,
            "high": highs,
            "low": lows,
            "close": closes
        },
        "volume": volumes,
        "overlays": {
            "sma_20": series.get("sma_20", []),
            "sma_50": series.get("sma_50", []),
            "ema_20": series.get("ema_20", []),
            "bb_upper": series.get("bb_upper", []),
            "bb_lower": series.get("bb_lower", [])
        },
        "oscillators": {
            "rsi": series.get("rsi", []),
            "macd": series.get("macd", []),
            "macd_signal": series.get("macd_signal", []),
            "macd_hist": series.get("macd_hist", [])
        },
        "key_levels": {
            "nearest_support": sr_dict.get("nearest_support"),
            "secondary_support": sr_dict.get("secondary_support"),
            "nearest_resistance": sr_dict.get("nearest_resistance"),
            "secondary_resistance": sr_dict.get("secondary_resistance")
        }
    }

    if prediction_dict and "trajectory" in prediction_dict:
        traj = prediction_dict["trajectory"]
        payload["forecast"] = {
            "dates": traj.get("dates", []),
            "prices": traj.get("prices", []),
            "upper_bounds": traj.get("upper_bounds", []),
            "lower_bounds": traj.get("lower_bounds", []),
            "direction": prediction_dict.get("direction", "SIDEWAYS"),
            "confidence": prediction_dict.get("confidence_score_pct", 50.0)
        }

    return payload

Optional_Dict = Optional[Dict[str, Any]]
