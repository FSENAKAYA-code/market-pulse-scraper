import pytest

from market.collector import extract_text, fetch_html
from market.pricing import summarize_prices


def test_price_summary_is_deterministic():
    assert summarize_prices([10, 20, 30])["median"] == 20


def test_price_summary_rejects_invalid_values():
    with pytest.raises(ValueError):
        summarize_prices([0, 10])


def test_html_extraction_uses_supplied_markup_only():
    assert extract_text("<p class='price'> $12 </p><p>ignore</p>", ".price") == ["$12"]


def test_fetch_requires_explicit_allowlist_before_network_access():
    with pytest.raises(ValueError, match="allowlist"):
        fetch_html("https://example.com/item", allowed_hosts=set())
