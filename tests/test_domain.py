import asyncio

import numpy as np
import pytest

from market.collector import (
    extract_text,
    fetch_html,
    fetch_html_async,
    fetch_rendered_html,
    fetch_with_requests,
)
from market.price_model import chronological_split, fit_price_baseline
from market.pricing import elasticity_reference_price, suggest_price, summarize_prices


def test_price_summary_is_deterministic():
    assert summarize_prices([10, 20, 30])["median"] == 20


def test_price_summary_rejects_invalid_values():
    with pytest.raises(ValueError):
        summarize_prices([0, 10])


def test_price_suggestion_obeys_margin_bounds():
    assert suggest_price([5, 6, 7], unit_cost=10) == 11
    assert suggest_price([100, 110], unit_cost=10) == 15
    assert elasticity_reference_price(unit_cost=10, price_elasticity=-2) == 15


def test_html_extraction_uses_supplied_markup_only():
    assert extract_text("<p class='price'> $12 </p><p>ignore</p>", ".price") == ["$12"]


def test_fetch_requires_explicit_allowlist_before_network_access():
    with pytest.raises(ValueError, match="allowlist"):
        fetch_html("https://example.com/item", allowed_hosts=set())


def test_all_fetch_adapters_check_allowlist_before_network_access():
    with pytest.raises(ValueError, match="allowlist"):
        fetch_with_requests("https://example.com/", allowed_hosts=set())
    with pytest.raises(ValueError, match="allowlist"):
        fetch_rendered_html("https://example.com/", allowed_hosts=set())


def test_async_fetch_checks_allowlist_before_network_access():
    with pytest.raises(ValueError, match="allowlist"):
        asyncio.run(fetch_html_async("https://example.com/", allowed_hosts=set()))


def test_price_model_uses_ordered_non_overlapping_splits():
    X = np.arange(100).reshape(50, 2)
    y = np.arange(50)
    train_x, val_x, test_x, train_y, val_y, test_y = chronological_split(X, y)
    assert train_y[-1] < val_y[0] < test_y[0]
    assert train_x[-1, 0] < val_x[0, 0] < test_x[0, 0]
    assert set(fit_price_baseline(X, y)) == {
        "train_loss_mae", "validation_loss_mae", "test_mae"
    }
