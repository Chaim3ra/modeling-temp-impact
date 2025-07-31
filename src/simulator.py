from dataloader import load_all_tickers
from impact_model import compute_slippage
from pathlib import Path
from datetime import datetime

import pandas as pd


output_dir = Path("data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

# order sizes to simulate
SIZES = [5, 50, 100, 500, 1000]


def simulate_impacts():
    records = []
    tickers = load_all_tickers("data/raw/")
    for ticker, df in tickers.items():
        print("simulating from ticker: ", ticker)
        for _, row in df.iterrows():
            asks   = list(zip(row["ask_prices"], row["ask_sizes"]))
            mid    = row["mid_price"]
            spread = row["spread"]

            for x in SIZES:
                try:
                    slippage = compute_slippage(asks, mid, x)
                    records.append({
                        "ticker": ticker,
                        "ts": row["ts_event"],
                        "size": x,
                        "slippage": slippage,
                        "spread": spread
                    })
                except ValueError:
                    # skip if not enough depth
                    continue

    impacts = pd.DataFrame(records)
    # produces (x, g_t(x)) samples

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"impacts_{timestamp}.csv"
    impacts.to_csv(output_file, index=False)


if __name__ == "__main__":
    simulate_impacts()