"""
Signal & Strategy Interpretation Engine:
Combines technical indicators, support/resistance, and risk into educational market scenarios.
Never issues raw blind BUY/SELL orders; frames transparent Bullish/Neutral/Bearish scenarios.
"""

from typing import Dict, Any, List
from utils.helpers import safe_float

def generate_market_scenarios(
    current_price: float,
    nearest_support: float,
    secondary_support: float,
    nearest_resistance: float,
    secondary_resistance: float,
    trend_bias: str,
    rsi: float,
    macd_bias: str,
    atr: float
) -> Dict[str, Any]:
    """
    Generate calibrated educational scenarios: Bullish, Neutral, and Bearish with exact price levels.
    """
    # Target calculations based on ATR and resistances
    bull_target_1 = nearest_resistance
    bull_target_2 = secondary_resistance if secondary_resistance > nearest_resistance else round(nearest_resistance + 1.5 * atr, 2)
    
    bear_target_1 = nearest_support
    bear_target_2 = secondary_support if secondary_support < nearest_support else round(nearest_support - 1.5 * atr, 2)
    
    # 1. Bullish Scenario
    bullish_scenario = {
        "title": "Bullish Scenario (Upside Continuation)",
        "condition": f"If price decisively breaks and sustains above {nearest_resistance:.2f} with above-average volume",
        "target_zone": f"{bull_target_1:.2f} - {bull_target_2:.2f}",
        "invalidation": f"Rejection at resistance or slip back below {current_price - (0.7 * atr):.2f}",
        "probability_bias": "Favorable" if (trend_bias == "Bullish" and rsi < 68) else "Moderate"
    }

    # 2. Neutral Scenario
    neutral_scenario = {
        "title": "Neutral Scenario (Consolidation & Range)",
        "condition": f"If price remains bounded between {nearest_support:.2f} and {nearest_resistance:.2f}",
        "action": "Price continues sideways accumulation; range-trading strategies typically active between the boundaries",
        "breakout_level": f"{nearest_resistance:.2f}",
        "breakdown_level": f"{nearest_support:.2f}"
    }

    # 3. Bearish Scenario
    bearish_scenario = {
        "title": "Bearish Scenario (Pullback / Breakdown)",
        "condition": f"If price breaks below primary support at {nearest_support:.2f} under distribution volume",
        "target_zone": f"{bear_target_1:.2f} - {bear_target_2:.2f}",
        "risk_warning": f"Failure to hold {nearest_support:.2f} opens pathway toward secondary support at {secondary_support:.2f}"
    }

    # Determine overall structural stance
    bull_score = 0
    bear_score = 0

    if trend_bias == "Bullish":
        bull_score += 2
    elif trend_bias == "Bearish":
        bear_score += 2

    if macd_bias == "Bullish":
        bull_score += 1
    elif macd_bias == "Bearish":
        bear_score += 1

    if 50 <= rsi <= 68:
        bull_score += 1
    elif rsi > 70:
        bear_score += 1  # Overbought pullback risk
    elif rsi < 40:
        bear_score += 1

    if bull_score >= 3:
        overall_stance = "Bullish" if bull_score == 3 else "Strong Bullish"
        color = "green"
    elif bear_score >= 3:
        overall_stance = "Bearish" if bear_score == 3 else "Strong Bearish"
        color = "red"
    else:
        overall_stance = "Neutral / Consolidating"
        color = "gray"

    # Educational Setup Architecture (Educational only)
    entry_lower = round(max(nearest_support, current_price - 0.5 * atr), 2)
    entry_upper = round(current_price, 2)
    entry_zone = f"{entry_lower:.2f} - {entry_upper:.2f}" if overall_stance in ["Bullish", "Strong Bullish"] else f"Wait for confirmation at {nearest_support:.2f}"
    
    stop_loss_concept = round(nearest_support - (0.5 * atr), 2)
    risk_distance = max(0.01, current_price - stop_loss_concept)
    reward_distance = max(0.01, bull_target_1 - current_price)
    rr_ratio = round(reward_distance / risk_distance, 1)

    strategy_setup = {
        "overall_stance": overall_stance,
        "stance_color": color,
        "entry_zone": entry_zone,
        "support_level": nearest_support,
        "resistance_level": nearest_resistance,
        "target_zone": f"{bull_target_1:.2f} - {bull_target_2:.2f}",
        "invalidation_level": stop_loss_concept,
        "risk_reward_ratio": f"1 : {rr_ratio}",
        "time_horizon": "Short-to-Medium Term (5 - 20 trading sessions)",
        "disclaimer": "Educational model-derived scenario analysis. Does not constitute personal financial, investment, or trading advice."
    }

    return {
        "scenarios": {
            "bullish": bullish_scenario,
            "neutral": neutral_scenario,
            "bearish": bearish_scenario
        },
        "strategy": strategy_setup
    }
