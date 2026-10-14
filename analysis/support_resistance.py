"""
Support and Resistance Engine:
Calculates classic pivot points, local swing clusters, and breakout/breakdown zones.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List
from utils.helpers import safe_float

def calculate_pivot_points(prev_high: float, prev_low: float, prev_close: float) -> Dict[str, float]:
    """Calculate standard floor pivot points."""
    pivot = (prev_high + prev_low + prev_close) / 3.0
    r1 = (2 * pivot) - prev_low
    s1 = (2 * pivot) - prev_high
    r2 = pivot + (prev_high - prev_low)
    s2 = pivot - (prev_high - prev_low)
    r3 = prev_high + 2 * (pivot - prev_low)
    s3 = prev_low - 2 * (prev_high - pivot)

    return {
        "pivot": round(pivot, 2),
        "r1": round(r1, 2),
        "r2": round(r2, 2),
        "r3": round(r3, 2),
        "s1": round(s1, 2),
        "s2": round(s2, 2),
        "s3": round(s3, 2)
    }

def find_swing_levels(df: pd.DataFrame, window: int = 10) -> tuple:
    """Find local swing highs and swing lows from historical OHLCV data."""
    highs = df["High"].values
    lows = df["Low"].values
    n = len(df)
    
    resistance_levels = []
    support_levels = []
    
    for i in range(window, n - window):
        # Local peak
        if highs[i] == max(highs[i - window : i + window + 1]):
            resistance_levels.append(float(highs[i]))
        # Local trough
        if lows[i] == min(lows[i - window : i + window + 1]):
            support_levels.append(float(lows[i]))
            
    return resistance_levels, support_levels

def cluster_levels(levels: List[float], tolerance_pct: float = 0.015) -> List[float]:
    """Group close price levels together into significant horizontal price zones."""
    if not levels:
        return []
    sorted_levels = sorted(levels)
    clusters = []
    current_cluster = [sorted_levels[0]]
    
    for lvl in sorted_levels[1:]:
        if (lvl - current_cluster[-1]) / current_cluster[-1] <= tolerance_pct:
            current_cluster.append(lvl)
        else:
            clusters.append(float(np.mean(current_cluster)))
            current_cluster = [lvl]
    if current_cluster:
        clusters.append(float(np.mean(current_cluster)))
        
    return [round(x, 2) for x in clusters]

def compute_support_resistance(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Compute comprehensive support, resistance, pivots, and breakout/breakdown levels.
    """
    if len(df) < 5:
        raise ValueError("Insufficient data to compute support and resistance.")

    current_price = safe_float(df["Close"].iloc[-1])
    prev_high = safe_float(df["High"].iloc[-2]) if len(df) > 1 else safe_float(df["High"].iloc[-1])
    prev_low = safe_float(df["Low"].iloc[-2]) if len(df) > 1 else safe_float(df["Low"].iloc[-1])
    prev_close = safe_float(df["Close"].iloc[-2]) if len(df) > 1 else current_price

    pivots = calculate_pivot_points(prev_high, prev_low, prev_close)

    # Historical swing clusters
    swing_res, swing_sup = find_swing_levels(df, window=7)
    res_clusters = cluster_levels(swing_res)
    sup_clusters = cluster_levels(swing_sup)

    # Levels strictly above current price = resistances
    resistances_above = [r for r in res_clusters if r > current_price]
    # Levels strictly below current price = supports
    supports_below = [s for s in sup_clusters if s < current_price]

    # Nearest major levels
    nearest_resistance = resistances_above[0] if resistances_above else pivots["r1"]
    secondary_resistance = resistances_above[1] if len(resistances_above) > 1 else pivots["r2"]
    
    nearest_support = supports_below[-1] if supports_below else pivots["s1"]
    secondary_support = supports_below[-2] if len(supports_below) > 1 else pivots["s2"]

    # In case pivot points are closer or swing levels were empty
    if nearest_resistance <= current_price:
        nearest_resistance = max(pivots["r1"], round(current_price * 1.015, 2))
    if nearest_support >= current_price:
        nearest_support = min(pivots["s1"], round(current_price * 0.985, 2))

    dist_to_res_pct = ((nearest_resistance - current_price) / current_price) * 100
    dist_to_sup_pct = ((current_price - nearest_support) / current_price) * 100

    return {
        "current_price": current_price,
        "nearest_support": round(nearest_support, 2),
        "secondary_support": round(secondary_support, 2),
        "nearest_resistance": round(nearest_resistance, 2),
        "secondary_resistance": round(secondary_resistance, 2),
        "distance_to_resistance_pct": round(dist_to_res_pct, 2),
        "distance_to_support_pct": round(dist_to_sup_pct, 2),
        "breakout_zone": f"Above {nearest_resistance:.2f}",
        "breakdown_zone": f"Below {nearest_support:.2f}",
        "consolidation_range": f"{nearest_support:.2f} - {nearest_resistance:.2f}",
        "pivots": pivots
    }
