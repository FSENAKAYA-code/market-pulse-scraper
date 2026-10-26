"""Transparent descriptive price summaries; this module makes no web requests."""

from collections.abc import Iterable
from statistics import median


def summarize_prices(prices: Iterable[float]) -> dict[str, float]:
    values = [float(value) for value in prices]
    if not values:
        raise ValueError("at least one price is required")
    if any(value <= 0 for value in values):
        raise ValueError("prices must be positive")
    return {"median": median(values), "minimum": min(values), "maximum": max(values), "count": float(len(values))}
