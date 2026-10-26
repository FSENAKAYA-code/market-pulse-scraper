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


async def fetch_html_async(
    url: str, *, allowed_hosts: set[str], timeout: float = 10.0
) -> str:
    """Asynchronously fetch one HTTPS page from an explicit host allowlist."""
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname:
        raise ValueError("only absolute HTTPS URLs are accepted")
    if parsed.hostname.lower() not in {host.lower() for host in allowed_hosts}:
        raise ValueError("URL host is not in the explicit allowlist")
    if timeout <= 0:
        raise ValueError("timeout must be positive")
    async with httpx.AsyncClient(
        timeout=timeout,
        follow_redirects=False,
        headers={"User-Agent": "SenaKayaPortfolioResearch/0.1 (polite, one-off fetch)"},
    ) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text


def fetch_with_requests(url: str, *, allowed_hosts: set[str], timeout: float = 10.0) -> str:
    """Synchronous Requests adapter with the same host and scheme restrictions."""
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname:
        raise ValueError("only absolute HTTPS URLs are accepted")
    if parsed.hostname.lower() not in {host.lower() for host in allowed_hosts}:
        raise ValueError("URL host is not in the explicit allowlist")
    if timeout <= 0:
        raise ValueError("timeout must be positive")
    import requests

    response = requests.get(
        url,
        timeout=timeout,
        allow_redirects=False,
        headers={"User-Agent": "SenaKayaPortfolioResearch/0.1 (polite, one-off fetch)"},
    )
    response.raise_for_status()
    return response.text


def fetch_rendered_html(url: str, *, allowed_hosts: set[str], timeout: int = 15) -> str:
    """Optional Selenium adapter for authorized pages requiring JavaScript."""
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname:
        raise ValueError("only absolute HTTPS URLs are accepted")
    if parsed.hostname.lower() not in {host.lower() for host in allowed_hosts}:
        raise ValueError("URL host is not in the explicit allowlist")
    if timeout <= 0:
        raise ValueError("timeout must be positive")
    try:
        from selenium import webdriver
    except ImportError as exc:
        raise RuntimeError("install Selenium and a compatible browser driver") from exc
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    try:
        driver.set_page_load_timeout(timeout)
        driver.get(url)
        final = urlparse(driver.current_url)
        if final.hostname is None or final.hostname.lower() not in {
            host.lower() for host in allowed_hosts
        }:
            raise ValueError("browser navigation ended outside the explicit host allowlist")
        return driver.page_source
    finally:
        driver.quit()


def create_app(*, allowed_hosts: set[str]):
    """Build a small read-only FastAPI extraction endpoint with fixed host policy."""
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel

    app = FastAPI(title="Market Pulse Extractor", version="0.1.0")

    class ExtractRequest(BaseModel):
        url: str
        css_selector: str

    @app.post("/extract")
    async def extract(request: ExtractRequest) -> dict[str, list[str]]:
        try:
            html = await fetch_html_async(request.url, allowed_hosts=allowed_hosts)
            return {"items": extract_text(html, request.css_selector)}
        except (ValueError, httpx.HTTPError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    return app
