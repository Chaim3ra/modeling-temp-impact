# modeling-temp-impact
R&amp;D for market‐microstructure and optimal trade execution.

## Repository Structure

```
.
├── data/
│   ├── raw/                   # original MBP-10 CSV snapshots (not tracked)
│   └── processed/             # outputs from simulation (impacts_<TIMESTAMP>.csv, m)
├── notebooks/
│   └── impact-analysis.ipynb  # EDA & model fitting (linear, power-law, AC quadratic)
├── res/
│   └── images/                # figures used in the write-up
├── src/
│   ├── dataloader.py          # load MBP-10 CSVs into DataFrames
│   ├── impact_model.py        # compute slippage g_t(x) by “walking the book”
│   ├── simulator.py           # running order size simulations to generate temp impact
│   └── optimizer.py            # CVXPY solver for optimal slices (Almgren–Chriss)
├── write-up.tex                # LaTeX write-up
└── README.md                  # this file
```


## Setup

1. Clone this repo and enter its directory:
   ```bash
   git clone https://github.com/Chaim3ra/modeling-temp-impact.git
   cd modeling-temp-impact
   ```
2. Create and activate a Python 3 virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   _And, optionally for non‐convex solves(if using power-law model):_
   ```bash
   pip install dccp
   ```



## Modeling Temporary Impact $g(x$)

1. **Load raw snapshots**  
   Place your MBP-10 CSV files under `data/raw/` (organized by ticker/date).
      ```bash
   python src/dataloader.py
   ```


2. **Simulate slippage**  
   ```bash
   python src/simulator.py
   ```


   This generates a csv file `data/processed/impacts_<TIMESTAMP>.csv` in the following format:
   | Column     | Type       | Description                                                       |
   |------------|------------|-------------------------------------------------------------------|
   | `ticker`   | `string`   | Ticker symbol (e.g. `CRWV`, `FROG`, `SOUN`)                       |
   | `ts`       | `datetime` | Matching‐engine‐received timestamp (from `ts_event`)              |
   | `size`     | `integer`  | Order size in shares                                              |
   | `slippage` | `float`    | Temporary impact per share: average execution price minus mid‐price |
   | `spread`   | `float`    | Instantaneous bid–ask spread at the time of simulation            |


3. **Explore & fit**  
   Open the notebook:
   ```bash
   jupyter lab notebooks/impact_analysis.ipynb
   ```
   - EDA (mean and median slippage curves)  
   - Model fitting (linear, power-law, AC-quadratic)






## Data

- **Raw:** `data/raw/<TICKER>/*.csv`
- **Processed:** `data/processed/impacts_<TIMESTAMP>.csv`