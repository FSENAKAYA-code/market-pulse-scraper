"""ASGI entry point with an operator-configured host allowlist."""

import os

from market.collector import create_app

allowed_hosts = {
    host.strip().lower()
    for host in os.environ.get("MARKET_ALLOWED_HOSTS", "").split(",")
    if host.strip()
}
app = create_app(allowed_hosts=allowed_hosts)
