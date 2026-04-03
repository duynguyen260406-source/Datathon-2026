# 2026 Wildfire Survival Forecasting

This repository is the working project space for the 2026 wildfire-risk datathon task.

## Task Definition

Using only the first 5 hours after wildfire ignition, predict the probability that a fire will come within 5 km of an evacuation zone centroid by four operational horizons:

- `prob_12h`
- `prob_24h`
- `prob_48h`
- `prob_72h`

This is a right-censored survival problem, not a plain classification task. The training targets are:

- `event`: `1` if the fire reaches the 5 km threshold within the 72-hour window, else `0`
- `time_to_hit_hours`: observed hit time when `event = 1`, otherwise the censoring time inside the observation window

## Data Contract

- Raw CSV files in `data/raw/` are read-only and should never be edited by hand.
- `train.csv` is the source-of-truth training table.
- `test.csv` is the source-of-truth inference table.
- `train.csv` and `test.csv` share 35 columns.
- The two columns that appear only in training are `event` and `time_to_hit_hours`.
- The tracked schema reference lives in `configs/schema_reference.csv`.

## Current Snapshot

- Training shape: `221 x 37`
- Test shape: `95 x 35`
- Shared schema: `35` columns
- Modeling features: `34`
- Identifier column: `event_id`
- Missing values: `0` in train, `0` in test
- Event rate: `31.22%`
- Censoring rate: `68.78%`

See `EDA_SUMMARY.md` for the first-pass exploratory findings and `notebooks/EDA.ipynb` for the reproducible notebook.

## Project Layout

- `data/raw/`: raw input data kept out of version control
- `data/processed/`: cleaned and engineered datasets kept out of version control
- `notebooks/`: exploratory notebooks
- `src/`: project source code
- `configs/`: experiment and pipeline configuration files
- `models/`: trained model artifacts kept out of version control
- `outputs/`: generated outputs kept out of version control
- `tests/`: tests for data and modeling code

## Working Rule

Keep reusable logic in `src/` and use notebooks only for exploration and validation.
