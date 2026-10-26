"""Chronological price baseline; model selection never uses the test period."""

import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error


def chronological_split(
    X: np.ndarray,
    y: np.ndarray,
    *,
    train_fraction: float = 0.6,
    validation_fraction: float = 0.2,
) -> tuple[np.ndarray, ...]:
    if X.ndim != 2 or y.ndim != 1 or len(X) != len(y):
        raise ValueError("X must be 2D, y 1D, and row counts must match")
    if not 0 < train_fraction < 1 or not 0 < validation_fraction < 1:
        raise ValueError("split fractions must be between zero and one")
    if train_fraction + validation_fraction >= 1:
        raise ValueError("a non-empty test fraction is required")
    train_end = int(len(y) * train_fraction)
    validation_end = int(len(y) * (train_fraction + validation_fraction))
    if train_end < 2 or validation_end <= train_end or validation_end >= len(y):
        raise ValueError("not enough ordered rows for three non-empty splits")
    return (
        X[:train_end], X[train_end:validation_end], X[validation_end:],
        y[:train_end], y[train_end:validation_end], y[validation_end:],
    )


def fit_price_baseline(
    X: np.ndarray, y: np.ndarray, *, random_state: int = 42
) -> dict[str, float]:
    """Fit on past rows, inspect validation MAE, refit train+validation, test last."""
    X_train, X_val, X_test, y_train, y_val, y_test = chronological_split(X, y)
    model = HistGradientBoostingRegressor(random_state=random_state)
    model.fit(X_train, y_train)
    validation_mae = mean_absolute_error(y_val, model.predict(X_val))
    model.fit(np.concatenate([X_train, X_val]), np.concatenate([y_train, y_val]))
    return {
        "validation_mae": float(validation_mae),
        "test_mae": float(mean_absolute_error(y_test, model.predict(X_test))),
    }
