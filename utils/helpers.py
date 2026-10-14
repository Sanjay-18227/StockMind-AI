"""
Utility helpers for StockMind AI: Caching, currency formatting, market hours detection, and safe math.
"""

import time
import math
from datetime import datetime
import pytz
from typing import Any, Optional, Dict

class TTLCache:
    """Thread-safe simple in-memory TTL cache."""
    def __init__(self, default_ttl: int = 180):
        self._data: Dict[str, Any] = {}
        self._expiry: Dict[str, float] = {}
        self._default_ttl = default_ttl

    def get(self, key: str) -> Optional[Any]:
        now = time.time()
        if key in self._expiry:
            if now < self._expiry[key]:
                return self._data[key]
            # expired
            self._data.pop(key, None)
            self._expiry.pop(key, None)
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        duration = ttl if ttl is not None else self._default_ttl
        self._data[key] = value
        self._expiry[key] = time.time() + duration

    def clear(self) -> None:
        self._data.clear()
        self._expiry.clear()

# Global cache instance
cache = TTLCache(default_ttl=180)


def safe_float(val: Any, default: float = 0.0) -> float:
    """Safely convert value to float, handling None, NaN, inf."""
    if val is None:
        return default
    try:
        f = float(val)
        if math.isnan(f) or math.isinf(f):
            return default
        return f
    except (ValueError, TypeError):
        return default


def format_currency(value: float, currency_symbol: str = "₹") -> str:
    """Format price to localized currency string."""
    val = safe_float(value)
    if currency_symbol == "₹":
        # Indian lakh/crore or standard 2 decimals
        return f"₹{val:,.2f}"
    elif currency_symbol == "$":
        return f"${val:,.2f}"
    return f"{currency_symbol}{val:,.2f}"


def format_large_number(val: float, currency: str = "INR") -> str:
    """Format large numbers like market cap and volume (Cr, L for INR; B, M for USD)."""
    val = safe_float(val)
    if val == 0:
        return "N/A"

    if currency == "INR":
        if val >= 1e7:
            return f"₹{val / 1e7:,.2f} Cr"
        elif val >= 1e5:
            return f"₹{val / 1e5:,.2f} L"
        else:
            return f"₹{val:,.2f}"
    else:
        if val >= 1e12:
            return f"${val / 1e12:,.2f} T"
        elif val >= 1e9:
            return f"${val / 1e9:,.2f} B"
        elif val >= 1e6:
            return f"${val / 1e6:,.2f} M"
        elif val >= 1e3:
            return f"${val / 1e3:,.2f} K"
        else:
            return f"${val:,.2f}"


def format_percent(val: float, include_sign: bool = True) -> str:
    """Format percentage with sign and 2 decimal places."""
    v = safe_float(val)
    sign = "+" if (include_sign and v > 0) else ""
    return f"{sign}{v:.2f}%"


def get_market_status(ticker: str) -> Dict[str, Any]:
    """
    Determine if the market for the ticker is currently open, closed, or pre/post market.
    """
    ticker_upper = ticker.upper()
    is_indian = ticker_upper.endswith(".NS") or ticker_upper.endswith(".BO") or ticker_upper in ["^NSEI", "^BSESN", "^NSEBANK"]

    if is_indian:
        tz = pytz.timezone("Asia/Kolkata")
        now = datetime.now(tz)
        weekday = now.weekday()  # 0=Monday, 6=Sunday
        # Indian market hours: 09:15 to 15:30 IST Mon-Fri
        is_weekend = weekday >= 5
        curr_min = now.hour * 60 + now.minute
        open_min = 9 * 60 + 15
        close_min = 15 * 60 + 30

        if is_weekend:
            status = "CLOSED"
            detail = "Weekend (NSE/BSE Closed)"
        elif curr_min < open_min:
            status = "PRE_MARKET" if curr_min >= 9 * 60 else "CLOSED"
            detail = "Before Regular Trading Hours (Opens at 09:15 IST)"
        elif curr_min <= close_min:
            status = "OPEN"
            detail = "Live Trading (Closes at 15:30 IST)"
        else:
            status = "CLOSED"
            detail = "Market Closed (Regular session ended at 15:30 IST)"

        return {
            "is_open": status == "OPEN",
            "status": status,
            "detail": detail,
            "timezone": "Asia/Kolkata (IST)",
            "local_time": now.strftime("%Y-%m-%d %H:%M:%S IST")
        }
    else:
        # US Market
        tz = pytz.timezone("America/New_York")
        now = datetime.now(tz)
        weekday = now.weekday()
        is_weekend = weekday >= 5
        curr_min = now.hour * 60 + now.minute
        open_min = 9 * 60 + 30
        close_min = 16 * 60

        if is_weekend:
            status = "CLOSED"
            detail = "Weekend (US Markets Closed)"
        elif curr_min < open_min:
            status = "PRE_MARKET" if curr_min >= 4 * 60 else "CLOSED"
            detail = "Pre-Market Session (Opens at 09:30 EDT/EST)"
        elif curr_min <= close_min:
            status = "OPEN"
            detail = "Live Trading (Closes at 16:00 EDT/EST)"
        else:
            status = "AFTER_HOURS" if curr_min <= 20 * 60 else "CLOSED"
            detail = "After-Hours Session (Closed at 16:00 EDT/EST)"

        return {
            "is_open": status == "OPEN",
            "status": status,
            "detail": detail,
            "timezone": "America/New_York (ET)",
            "local_time": now.strftime("%Y-%m-%d %H:%M:%S ET")
        }
