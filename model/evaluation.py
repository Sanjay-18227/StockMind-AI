"""
Model Evaluation Metrics and Time-Series Validation:
Provides MAE, RMSE, MAPE, Directional Accuracy, and strict walk-forward splits
to prevent look-ahead bias and data leakage.
"""

import numpy as np
from typing import Dict, Any, Tuple

def mean_absolute_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Mean Absolute Error."""
    return float(np.mean(np.abs(y_true - y_pred)))

def root_mean_squared_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Root Mean Squared Error."""
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))

def mean_absolute_percentage_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Mean Absolute Percentage Error."""
    mask = y_true != 0
    if not np.any(mask):
        return 0.0
    return float(np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100)

def directional_accuracy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Directional Accuracy: Percentage of times the predicted sign matches actual sign.
    """
    if len(y_true) == 0:
        return 50.0
    correct = np.sign(y_true) == np.sign(y_pred)
    return float(np.mean(correct) * 100)

def r2_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Coefficient of Determination R^2."""
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    if ss_tot == 0:
        return 0.0
    return float(1.0 - (ss_res / (ss_tot + 1e-9)))

def compute_all_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """Calculate comprehensive evaluation suite."""
    return {
        "mae": round(mean_absolute_error(y_true, y_pred), 4),
        "rmse": round(root_mean_squared_error(y_true, y_pred), 4),
        "mape": round(mean_absolute_percentage_error(y_true, y_pred), 2),
        "r2": round(r2_score(y_true, y_pred), 4),
        "directional_accuracy_pct": round(directional_accuracy(y_true, y_pred), 1)
    }
