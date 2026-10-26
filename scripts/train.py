"""Run a synthetic chronological price forecast; no pages are fetched."""

import argparse

import numpy as np

from market.price_model import fit_price_baseline


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-csv", help="optional local CSV with numeric features and target")
    parser.add_argument("--target", default="next_price")
    args = parser.parse_args()
    rng = np.random.default_rng(42)
    time_index = np.arange(500, dtype=float)
    X = np.column_stack([time_index, rng.uniform(0.5, 1.5, 500)])
    y = 20 + 0.03 * time_index + 2 * X[:, 1] + rng.normal(0, 0.5, 500)
    if args.data_csv:
        import pandas as pd

        frame = pd.read_csv(args.data_csv)
        if args.target not in frame:
            raise ValueError(f"target column {args.target!r} is missing")
        if "timestamp" in frame:
            frame = frame.sort_values("timestamp").drop(columns="timestamp")
        y = frame.pop(args.target).to_numpy(dtype=float)
        X = frame.select_dtypes(include="number").to_numpy(dtype=float)
    print(fit_price_baseline(X, y))


if __name__ == "__main__":
    main()
