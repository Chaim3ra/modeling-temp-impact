# modeling-temp-impact
R&amp;D for modeling temporary impact. 

## Repository Structure

```
.
├── data/
│   ├── raw/                   # original MBP-10 CSV snapshots (not tracked)
│   └── processed/             # outputs from simulation (impacts.csv, median_slippage_by_size.csv)
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

2. **Simulate slippage**  
   ```bash
   python src/impact_model.py \
     --input-dir data/raw/CRWV \
     --output-file data/processed/impacts-<TIMESTAMP>.csv \
     --sizes 5 50 100 500 1000
   ```
   Or rerun with a log-spaced grid:
   ```bash
   python src/impact_model.py \
     --input-dir data/raw/CRWV \
     --output-file data/processed/impacts-<TIMESTAMP>.csv \
     --sizes $(python - <<'EOF'
        import numpy as npprint(*np.unique(np.logspace(np.log10(50),np.log10(5000),7).astype(int)))
        EOF
   )
   ```

3. **Explore & fit**  
   Open the notebook:
   ```bash
   jupyter lab notebooks/impact-analysis.ipynb
   ```
   - Section 4: EDA (raw and median slippage curves)  
   - Section 5: Model fitting (linear, power-law, AC-quadratic)






## Data

- **Raw:** `data/raw/<TICKER>/*.csv`
- **Processed:** `data/processed/impacts_<TIMESTAMP>.csv`