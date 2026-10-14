"""
UI Component Payload Builders:
Constructs clean dictionary representations of dashboard cards, badges, and scenario pills
for the frontend interface.
"""

from typing import Dict, Any, List
from utils.helpers import format_currency, format_percent

def build_dashboard_cards(analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generate clean cards for:
    Current Price, Daily Change, Prediction, Trend, Risk, RSI, Volatility, Support, Resistance
    """
    q = analysis["quote"]
    ind = analysis["indicators"]["latest"]
    sr = analysis["support_resistance"]
    st = analysis["statistics"]
    rk = analysis["risk"]
    pr = analysis["prediction"]

    curr = format_currency(q["current_price"], q["currency_symbol"])
    chg = format_percent(q["change_percent"])
    is_positive = q["change"] >= 0

    cards = [
        {
            "id": "current_price",
            "title": "Current Price",
            "value": curr,
            "subtext": f"{chg} today",
            "tone": "positive" if is_positive else "negative",
            "badge": "Live / Last Close"
        },
        {
            "id": "daily_change",
            "title": "Daily Change",
            "value": f"{q['currency_symbol']}{q['change']:+,.2f}",
            "subtext": f"{chg} % move",
            "tone": "positive" if is_positive else "negative",
            "badge": "Session"
        },
        {
            "id": "prediction",
            "title": "AI 5D Prediction",
            "value": f"{q['currency_symbol']}{pr['forecasts']['5_day']['target_price']:,.2f}",
            "subtext": f"{pr['forecasts']['5_day']['predicted_return_pct']:+.2f}% ({pr['direction']})",
            "tone": pr["direction_color"],
            "badge": f"{pr['confidence_score_pct']}% Conf."
        },
        {
            "id": "trend",
            "title": "Market Trend",
            "value": ind["trend_bias"],
            "subtext": ind["ma_summary"],
            "tone": "positive" if ind["trend_bias"] == "Bullish" else ("negative" if ind["trend_bias"] == "Bearish" else "neutral"),
            "badge": "Moving Avgs"
        },
        {
            "id": "risk",
            "title": "Risk Rating",
            "value": rk["risk_level"],
            "subtext": f"Score {rk['risk_score']}/100",
            "tone": rk["badge_color"],
            "badge": "Multi-Factor"
        },
        {
            "id": "rsi",
            "title": "RSI (14)",
            "value": f"{ind['rsi_14']:.1f}",
            "subtext": ind["rsi_signal"],
            "tone": "positive" if ind["rsi_signal"] == "Bullish" else ("negative" if ind["rsi_signal"] == "Bearish" else "neutral"),
            "badge": "Momentum"
        },
        {
            "id": "volatility",
            "title": "Annual Volatility",
            "value": f"{st['annualized_volatility_pct']:.1f}%",
            "subtext": f"20D Rolling: {st['rolling_volatility_20d_pct']:.1f}%",
            "tone": "neutral",
            "badge": "Historical"
        },
        {
            "id": "support",
            "title": "Key Support",
            "value": format_currency(sr["nearest_support"], q["currency_symbol"]),
            "subtext": f"-{sr['distance_to_support_pct']:.1f}% from current",
            "tone": "positive",
            "badge": "Floor"
        },
        {
            "id": "resistance",
            "title": "Key Resistance",
            "value": format_currency(sr["nearest_resistance"], q["currency_symbol"]),
            "subtext": f"+{sr['distance_to_resistance_pct']:.1f}% from current",
            "tone": "negative",
            "badge": "Ceiling"
        }
    ]

    return cards
