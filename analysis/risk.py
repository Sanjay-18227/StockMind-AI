"""
Risk Analysis Engine:
Quantifies portfolio and stock risk into Low / Medium / High / Very High.
Evaluates Volatility, ATR%, Drawdown, Beta, Trend Instability, and Volume Liquidity.
Explains the precise mathematical drivers of the risk score.
"""

from typing import Dict, Any, List
from utils.helpers import safe_float

def assess_stock_risk(
    annualized_volatility: float,
    atr_percent: float,
    max_drawdown: float,
    beta: float,
    trend_bias: str,
    volume_ratio: float
) -> Dict[str, Any]:
    """
    Compute structured, multi-factor risk assessment.
    Returns: Risk level, 0-100 risk score, risk factors, and clear plain-language rationale.
    """
    score = 0.0
    drivers: List[str] = []

    # 1. Volatility contribution (0 to 25 points)
    # Low: < 20%, Med: 20-35%, High: 35-50%, Extreme: > 50%
    if annualized_volatility < 20.0:
        score += 5
    elif annualized_volatility < 35.0:
        score += 15
        drivers.append(f"Moderate annualized volatility ({annualized_volatility:.1f}%)")
    elif annualized_volatility < 50.0:
        score += 22
        drivers.append(f"Elevated annualized volatility ({annualized_volatility:.1f}%)")
    else:
        score += 25
        drivers.append(f"High historical volatility ({annualized_volatility:.1f}%) creates sharp price swings")

    # 2. Drawdown contribution (0 to 25 points)
    # max_drawdown is negative (e.g., -15.4%)
    abs_dd = abs(max_drawdown)
    if abs_dd < 10.0:
        score += 4
    elif abs_dd < 20.0:
        score += 12
    elif abs_dd < 35.0:
        score += 19
        drivers.append(f"Significant maximum drawdown history ({max_drawdown:.1f}%) from peak")
    else:
        score += 25
        drivers.append(f"Severe drawdown of {max_drawdown:.1f}%, indicating deep vulnerability during market corrections")

    # 3. ATR % contribution (0 to 20 points)
    if atr_percent < 1.5:
        score += 4
    elif atr_percent < 3.0:
        score += 10
    elif atr_percent < 4.5:
        score += 16
        drivers.append(f"Daily price range (ATR) is wide at {atr_percent:.1f}% of stock price")
    else:
        score += 20
        drivers.append(f"Extremely wide daily price range (ATR {atr_percent:.1f}%), indicating high intraday variance")

    # 4. Beta contribution (0 to 15 points)
    if beta < 0.8:
        score += 3
    elif beta <= 1.2:
        score += 7
    elif beta <= 1.6:
        score += 12
        drivers.append(f"High market sensitivity (Beta {beta:.2f}), amplifying market-wide fluctuations")
    else:
        score += 15
        drivers.append(f"Aggressive market sensitivity (Beta {beta:.2f}), swinging much faster than the index")

    # 5. Trend & Volume instability (0 to 15 points)
    if trend_bias == "Bearish":
        score += 12
        drivers.append("Downtrend structure puts downward pressure on price levels")
    elif trend_bias == "Neutral / Mixed":
        score += 6
        drivers.append("Range-bound chop presents whipsaw risk")
    else:
        score += 2

    if volume_ratio > 2.5:
        score += 3
        drivers.append("Abnormally heavy volume turnover detected")

    total_score = min(100.0, max(5.0, score))

    # Categorize Risk Level
    if total_score < 30.0:
        risk_level = "Low"
        badge_color = "green"
        summary = "Low risk profile with stable volatility, modest historical drawdowns, and disciplined price structure."
    elif total_score < 55.0:
        risk_level = "Medium"
        badge_color = "amber"
        summary = "Moderate risk profile typical of mature equities. Balanced price swings within acceptable standard deviations."
    elif total_score < 75.0:
        risk_level = "High"
        badge_color = "orange"
        summary = "Elevated risk profile. Notable historical drawdown or high volatility may cause sudden short-term pullbacks."
    else:
        risk_level = "Very High"
        badge_color = "red"
        summary = "Very high risk profile characterized by acute volatility, deep drawdowns, or aggressive beta."

    # Build human explanation
    if not drivers:
        drivers.append("Stable volatility and normal trading range relative to historical benchmarks.")

    explanation = (
        f"Risk Rating: {risk_level} (Score {int(total_score)}/100).\n"
        f"{summary}\n"
        f"Key Factors: {'; '.join(drivers)}."
    )

    return {
        "risk_level": risk_level,
        "risk_score": int(total_score),
        "badge_color": badge_color,
        "summary": summary,
        "drivers": drivers,
        "explanation": explanation,
        "metrics": {
            "volatility": round(annualized_volatility, 2),
            "max_drawdown": round(max_drawdown, 2),
            "atr_pct": round(atr_percent, 2),
            "beta": round(beta, 2)
        }
    }
