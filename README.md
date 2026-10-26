# market-pulse-scraper

> Educational portfolio scaffold by Fatma Sena Kaya · **Data collection and pricing**

Responsible public-price collection and transparent pricing analysis

## Scope and status

This repository is a reproducible learning project scaffold, not a production service. It contains an executable baseline, clear data boundaries, and extension points. Results are meaningful only when run on documented, appropriate data. No dataset, model weight, credential, or private record is included.

## Quick start

Requires Python 3.12 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run python scripts/train.py
uv run pytest
uv run ruff check .
```

The demo uses generated toy data only. Replace it with data you are allowed to use, record its source and license, and keep private or raw data out of Git.

## Data and evaluation

- Expected input: Public pages whose terms permit collection, or a user-supplied CSV.
- The pricing model keeps rows in timestamp order and uses the earliest 60% for training, the next 20% for validation, and the latest 20% for final testing. It does not shuffle future prices into the past. Its reference-price function enforces explicit cost and margin bounds and does not alter listings.
- Fit preprocessing steps on training data only. Use validation results for model selection; report the test result once for the chosen configuration.
- Check the project's `src/market/` code and tests before adapting it to real data.

## Domain workflow

- Static HTTPX/Requests and asynchronous HTTPX adapters require HTTPS and an explicit hostname allowlist and refuse redirects. Optional Selenium is limited to trusted allowlisted sites and checks the final browser host. The FastAPI service reads its allowlist from `MARKET_ALLOWED_HOSTS` (comma-separated hostnames).
- Check each site's terms and robots policy before collection. The project does not bypass access controls or crawl automatically. API requests are one-page extraction requests. Treat the Selenium helper as a local learning adapter, not a hardened browser sandbox.
- Convert authorized observations into a timestamped CSV with a `next_price` target for `uv run python scripts/train.py --data-csv PATH`. Evaluation is chronological 60/20/20. The bounded pricing heuristic only returns a reference value; it does not change listings.
- Run the local API with `MARKET_ALLOWED_HOSTS=example.org uv run python scripts/serve.py`.

## Repository layout

```text
data/       empty raw/ and processed/ locations; contents are ignored by Git
models/     empty local model-output location; model weights are ignored
scripts/    runnable demo entry points
src/        importable project code
tests/      small deterministic unit tests
```

## Responsible use

Price monitoring and baseline forecasting

## Roadmap

1. Add a documented, licensed dataset adapter.
2. Add domain-specific preprocessing and baselines.
3. Tune against validation data and report held-out test metrics with limitations.
4. Add deployment only after privacy, security, and monitoring review.

## Author

Fatma Sena Kaya · [GitHub](https://github.com/FSENAKAYA-code) · [LinkedIn](https://www.linkedin.com/in/sena-kaya-8634ba383/)
