"""
Statistical Analysis Engine:
Calculates returns, volatility, drawdowns, Sharpe ratio, Beta, Correlation,
historical distributions, positive/negative days, and volume metrics.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Optional
from scipy import stats
from utils.helpers import safe_float

def compute_historical_statistics(df: pd.DataFrame, benchmark_df: Optional[pd.DataFrame] = None, risk_free_rate: float = 0.065) -> Dict[str, Any]:
    """
    Perform deep statistical analysis on historical price data.
    """
    if df.empty or len(df) < 10:
        raise ValueError("Insufficient historical data for statistical analysis.")

    close = df["Close"]
    volume = df["Volume"]

    # Daily returns
    daily_returns = close.pct_change().dropna()
    total_days = len(daily_returns)
    if total_days == 0:
        raise ValueError("No returns available.")

    # Positive and negative day metrics
    pos_days = (daily_returns > 0).sum()
    neg_days = (daily_returns < 0).sum()
    flat_days = (daily_returns == 0).sum()
    pos_day_pct = (pos_days / total_days) * 100
    neg_day_pct = (neg_days / total_days) * 100

    # Return aggregations
    avg_daily_return = daily_returns.mean()
    daily_vol = daily_returns.std()
    annualized_vol = daily_vol * np.sqrt(252) * 100
    annualized_return = ((1 + avg_daily_return) ** 252 - 1) * 100

    # 1-week (5d) and 1-month (21d) returns
    return_5d = ((close.iloc[-1] / close.iloc[-6]) - 1) * 100 if len(close) >= 6 else (close.pct_change().iloc[-1] * 100)
    return_21d = ((close.iloc[-1] / close.iloc[-22]) - 1) * 100 if len(close) >= 22 else return_5d
    return_1y = ((close.iloc[-1] / close.iloc[0]) - 1) * 100 if len(close) >= 200 else return_21d

    # Drawdown calculation
    cumulative_max = close.cummax()
    drawdown_series = (close - cumulative_max) / cumulative_max
    max_drawdown_pct = safe_float(drawdown_series.min() * 100)
    current_drawdown_pct = safe_float(drawdown_series.iloc[-1] * 100)

    # Sharpe ratio
    daily_rf = (1 + risk_free_rate) ** (1 / 252) - 1
    excess_returns = daily_returns - daily_rf
    sharpe_ratio = (excess_returns.mean() / (daily_returns.std() + 1e-9)) * np.sqrt(252)

    # Rolling volatility (20 days)
    rolling_vol_20d = daily_returns.rolling(window=20).std() * np.sqrt(252) * 100
    latest_rolling_vol = safe_float(rolling_vol_20d.iloc[-1], annualized_vol)

    # Beta and Correlation with Benchmark
    beta = 1.0
    correlation = 1.0
    if benchmark_df is not None and not benchmark_df.empty:
        try:
            bm_close = benchmark_df["Close"]
            aligned = pd.concat([close, bm_close], axis=1, join="inner").dropna()
            if len(aligned) > 20:
                stock_ret = aligned.iloc[:, 0].pct_change().dropna()
                bm_ret = aligned.iloc[:, 1].pct_change().dropna()
                
                # Covariance & Variance
                cov_matrix = np.cov(stock_ret, bm_ret)
                bm_var = cov_matrix[1, 1]
                stock_bm_cov = cov_matrix[0, 1]
                
                if bm_var > 1e-9:
                    beta = float(stock_bm_cov / bm_var)
                
                corr = np.corrcoef(stock_ret, bm_ret)[0, 1]
                if not np.isnan(corr):
                    correlation = float(corr)
        except Exception:
            pass

    # Historical price distribution metrics
    skewness = safe_float(stats.skew(daily_returns))
    kurt = safe_float(stats.kurtosis(daily_returns))
    quantiles = {
        "p5": round(safe_float(np.percentile(daily_returns * 100, 5)), 2),
        "p25": round(safe_float(np.percentile(daily_returns * 100, 25)), 2),
        "median": round(safe_float(np.percentile(daily_returns * 100, 50)), 2),
        "p75": round(safe_float(np.percentile(daily_returns * 100, 75)), 2),
        "p95": round(safe_float(np.percentile(daily_returns * 100, 95)), 2)
    }

    # Volume statistics
    vol_mean = safe_float(volume.mean())
    vol_median = safe_float(volume.median())
    vol_std = safe_float(volume.std())
    latest_vol = safe_float(volume.iloc[-1])
    vol_spike_ratio = (latest_vol / (vol_mean + 1e-9))

    return {
        "sample_trading_days": int(total_days),
        "return_5d_pct": round(return_5d, 2),
        "return_21d_pct": round(return_21d, 2),
        "return_1y_pct": round(return_1y, 2),
        "annualized_return_pct": round(annualized_return, 2),
        "daily_volatility_pct": round(daily_vol * 100, 2),
        "annualized_volatility_pct": round(annualized_vol, 2),
        "rolling_volatility_20d_pct": round(latest_rolling_vol, 2),
        "max_drawdown_pct": round(max_drawdown_pct, 2),
        "current_drawdown_pct": round(current_drawdown_pct, 2),
        "sharpe_ratio": round(safe_float(sharpe_ratio), 2),
        "beta": round(beta, 2),
        "correlation_with_benchmark": round(correlation, 2),
        "positive_days_pct": round(pos_day_pct, 1),
        "negative_days_pct": round(neg_day_pct, 1),
        "flat_days_pct": round((flat_days / total_days) * 100, 1),
        "skewness": round(skewness, 2),
        "kurtosis": round(kurt, 2),
        "quantiles": quantiles,
        "volume_stats": {
            "mean": int(vol_mean),
            "median": int(vol_median),
            "std": int(vol_std),
            "latest": int(latest_vol),
            "spike_ratio": round(vol_spike_ratio, 2)
        },
        "drawdown_series": [round(safe_float(x) * 100, 2) for x in drawdown_series.tail(60)]
    }
