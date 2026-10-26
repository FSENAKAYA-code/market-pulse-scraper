"""Explicit, host-allowlisted HTML fetch and parse helpers; never auto-run."""

from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup


def fetch_html(url: str, *, allowed_hosts: set[str], timeout: float = 10.0) -> str:
    """Fetch a public page only when its host is explicitly allowlisted."""
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname:
        raise ValueError("only absolute HTTPS URLs are accepted")
    if parsed.hostname.lower() not in {host.lower() for host in allowed_hosts}:
        raise ValueError("URL host is not in the explicit allowlist")
    if timeout <= 0:
        raise ValueError("timeout must be positive")
    response = httpx.get(
        url,
        timeout=timeout,
        follow_redirects=False,
        headers={"User-Agent": "SenaKayaPortfolioResearch/0.1 (polite, one-off fetch)"},
    )
    response.raise_for_status()
    return response.text


def extract_text(html: str, css_selector: str) -> list[str]:
    """Extract non-empty visible text from matching elements in supplied HTML."""
    if not css_selector.strip():
        raise ValueError("css_selector must not be empty")
    soup = BeautifulSoup(html, "html.parser")
    return [
        element.get_text(" ", strip=True)
        for element in soup.select(css_selector)
        if element.get_text(strip=True)
    ]
