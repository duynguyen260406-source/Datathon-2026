# 2026 Data Science Project

This repository contains the working structure for the 2026 data science project.

## Project Layout

- `data/raw/`: raw input data kept out of version control
- `data/processed/`: cleaned and engineered datasets kept out of version control
- `notebooks/`: exploratory notebooks
- `src/`: project source code
- `configs/`: experiment and pipeline configuration files
- `models/`: trained model artifacts kept out of version control
- `outputs/`: reports, predictions, and figures kept out of version control
- `tests/`: tests for data and modeling code

## Notes

- Raw datasets, processed data, model binaries, and generated outputs are ignored by git.
- Keep reusable logic in `src/` and use `notebooks/` for exploration only.
