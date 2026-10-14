"""
Machine Learning Model Training Engine:
Builds leakage-free engineered features and trains an ensemble of Gradient Boosting
and Regularized Ridge Regression models evaluated with TimeSeriesSplit.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import TimeSeriesSplit
from analysis.indicators import calculate_rsi, calculate_sma, calculate_ema, calculate_macd, calculate_bollinger_bands, calculate_atr
from model.evaluation import compute_all_metrics
from utils.helpers import safe_float

def build_features(df: pd.DataFrame) -> tuple:
    """
    Extract strictly backward-looking engineered features from historical OHLCV data.
    Ensures zero future information is present in the feature matrix.
    """
    close = df["Close"]
    volume = df["Volume"]

    # Returns
    ret_1d = close.pct_change(1)
    ret_3d = close.pct_change(3)
    ret_5d = close.pct_change(5)

    # Moving averages
    sma_20 = calculate_sma(close, 20)
    sma_50 = calculate_sma(close, 50)
    sma20_dist = (close / (sma_20 + 1e-9)) - 1.0
    sma50_dist = (close / (sma_50 + 1e-9)) - 1.0

    # EMA
    ema_9 = calculate_ema(close, 9)
    ema_20 = calculate_ema(close, 20)
    ema_ratio = (ema_9 / (ema_20 + 1e-9)) - 1.0

    # RSI
    rsi = calculate_rsi(close, 14) / 100.0  # Scale 0-1

    # MACD
    _, _, macd_hist = calculate_macd(close, 12, 26, 9)
    macd_hist_norm = macd_hist / (close + 1e-9)

    # Bollinger Bands
    _, _, _, _, bb_pct_b = calculate_bollinger_bands(close, 20, 2.0)

    # ATR
    atr = calculate_atr(df, 14)
    atr_norm = atr / (close + 1e-9)

    # Volatility
    vol_20d = ret_1d.rolling(window=20).std()

    # Volume ratio
    vol_sma = calculate_sma(volume, 20)
    vol_ratio = (volume / (vol_sma + 1e-9)).clip(0, 5)

    # Momentum
    mom_10d = ((close - close.shift(10)) / (close.shift(10) + 1e-9))

    features_df = pd.DataFrame({
        "ret_1d": ret_1d,
        "ret_3d": ret_3d,
        "ret_5d": ret_5d,
        "sma20_dist": sma20_dist,
        "sma50_dist": sma50_dist,
        "ema_ratio": ema_ratio,
        "rsi": rsi,
        "macd_hist_norm": macd_hist_norm,
        "bb_pct_b": bb_pct_b,
        "atr_norm": atr_norm,
        "vol_20d": vol_20d,
        "vol_ratio": vol_ratio,
        "mom_10d": mom_10d
    }, index=df.index)

    return features_df, atr_norm.iloc[-1]

def train_and_evaluate_horizon(
    features_df: pd.DataFrame,
    close: pd.Series,
    horizon_days: int = 5
) -> Dict[str, Any]:
    """
    Train horizon model with strict walk-forward cross validation.
    Returns model, out-of-fold metrics, and latest prediction.
    """
    # Target: forward return over horizon_days
    forward_return = (close.shift(-horizon_days) / close) - 1.0

    # Combine and drop NaNs for training
    valid_mask = ~(features_df.isna().any(axis=1) | forward_return.isna())
    X = features_df[valid_mask].values
    y = forward_return[valid_mask].values

    if len(X) < 40:
        raise ValueError("Insufficient sample size to train prediction model.")

    # TimeSeriesSplit cross validation (3 folds)
    tscv = TimeSeriesSplit(n_splits=3)
    oof_preds = []
    oof_true = []

    for train_idx, val_idx in tscv.split(X):
        X_train, y_train = X[train_idx], y[train_idx]
        X_val, y_val = X[val_idx], y[val_idx]

        model_gb = GradientBoostingRegressor(n_estimators=45, max_depth=3, learning_rate=0.05, random_state=42)
        model_ridge = Ridge(alpha=1.0)

        model_gb.fit(X_train, y_train)
        model_ridge.fit(X_train, y_train)

        pred_val = 0.6 * model_gb.predict(X_val) + 0.4 * model_ridge.predict(X_val)
        oof_preds.extend(pred_val)
        oof_true.extend(y_val)

    metrics = compute_all_metrics(np.array(oof_true), np.array(oof_preds))

    # Retrain on all available valid data
    final_gb = GradientBoostingRegressor(n_estimators=50, max_depth=3, learning_rate=0.05, random_state=42)
    final_ridge = Ridge(alpha=1.0)
    final_gb.fit(X, y)
    final_ridge.fit(X, y)

    # Latest row features (today's market close)
    latest_features = features_df.iloc[-1:].values
    pred_return = float(0.6 * final_gb.predict(latest_features)[0] + 0.4 * final_ridge.predict(latest_features)[0])

    # Residual standard deviation for confidence cone
    residuals = np.array(oof_true) - np.array(oof_preds)
    residual_std = float(np.std(residuals))

    return {
        "predicted_return": pred_return,
        "residual_std": residual_std,
        "metrics": metrics,
        "sample_size": len(X)
    }
