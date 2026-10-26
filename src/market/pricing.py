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


def suggest_price(
    competitor_prices: Iterable[float],
    *,
    unit_cost: float,
    minimum_margin: float = 0.1,
    maximum_margin: float = 0.5,
) -> float:
    """Return a bounded, explainable reference price; never changes a listing."""
    if unit_cost <= 0 or not 0 <= minimum_margin <= maximum_margin:
        raise ValueError("cost must be positive and margins ordered in [0, 1]")
    values = [float(value) for value in competitor_prices]
    if not values or any(value <= 0 for value in values):
        raise ValueError("positive competitor prices are required")
    floor = unit_cost * (1 + minimum_margin)
    ceiling = unit_cost * (1 + maximum_margin)
    return float(min(max(median(values), floor), ceiling))
