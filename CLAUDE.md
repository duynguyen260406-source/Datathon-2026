# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Task

Right-censored survival analysis. Predict calibrated probabilities that a wildfire reaches within 5 km of an evacuation zone centroid by four horizons: `prob_12h`, `prob_24h`, `prob_48h`, `prob_72h`. Features are computed from the first 5 hours after ignition only.

**Evaluation metric:** `Hybrid Score = 0.3 × C-index + 0.7 × (1 − Weighted Brier Score)`
Weighted Brier = `0.3 × Brier@24h + 0.4 × Brier@48h + 0.3 × Brier@72h`

## Commands

Run scripts from the project root (scripts use `Path(__file__).resolve().parents[1]` to locate data):

```bash
# Regenerate fold assignments (only if training data changes)
python src/create_folds.py

# Planned pipeline scripts (to be implemented per PLAN.md)
python src/train.py       # OOF training for full model zoo
python src/predict.py     # Refit on full train, write test predictions
python src/ensemble.py    # Combine calibrated predictions → submission.csv
```

Run tests (pytest, once tests/ is populated):
```bash
pytest tests/
```

## Architecture

### Data Contract
- `data/raw/` is **read-only** — never edit by hand
- `train.csv` (221 × 37): 34 modeling features + `event_id` + `event` + `time_to_hit_hours`
- `test.csv` (95 × 35): same 34 features + `event_id`, no targets
- `configs/schema_reference.csv`: tracked column schema
- No missing values in either split; no shared `event_id`s

### Validation
- **Fixed 5-fold CV only** — `configs/folds_v1.csv`, seed `20260324`, never reshuffle
- Stratified by `event` × within-event quantile bin of `time_to_hit_hours`
- All model comparisons must use these exact fold assignments

### Censor-Aware Horizon Labeling
For a horizon H, a row is:
- **positive** if `event=1` and `time_to_hit_hours <= H`
- **negative** if `time_to_hit_hours > H`
- **excluded** if `event=0` and `time_to_hit_hours <= H`

This exclusion rule must be applied to both training labels for horizon models and Brier score evaluation.

### Planned Pipeline (`src/`)
Per `PLAN.md`:
- `train.py` — fold training, writes OOF predictions + per-fold metrics
- `predict.py` — full-train refit, writes per-model test predictions
- `ensemble.py` — grid-searches nonnegative weights (0.0–1.0, step 0.1) over OOF hybrid score, writes `submission.csv`

Model zoo:
- **Survival models** (via `lifelines`): penalized Cox PH, Weibull AFT, Log-Normal AFT
- **Horizon models** (one per horizon): LightGBM, CatBoost, elastic-net logistic regression

### Preprocessing
- Fold-local z-score scaling; zero-variance columns get scale `1`
- No feature engineering in v1 — only the 34 existing numeric features

### Calibration
Platt-style logistic calibrator fitted on pooled OOF predictions (evaluable rows only), applied before ensemble search.

### Urgency Score for C-index
Convert four cumulative horizon probs to interval masses over `[0-12], (12-24], (24-48], (48-72], >72`, compute expected-time proxy, use negative expected time as the C-index ranking score.

### Final Output Constraints
- All probabilities finite and in `[0, 1]`
- Monotonic across horizons: `prob_12h ≤ prob_24h ≤ prob_48h ≤ prob_72h` (enforce via `cummax`)
- Submission columns: `event_id, prob_12h, prob_24h, prob_48h, prob_72h` — must match `data/raw/sample_submission.csv` exactly

## Key Rules
- Select models/ensembles by **pooled OOF hybrid score**, not single-fold results
- Prefer lower weighted Brier over higher C-index when hybrid scores are close (calibration is 70% of the metric)
- Keep at least one true survival model in the final candidate pool
- No feature engineering until the multi-model baseline is end-to-end working
- If a survival model fails to converge, retry once with stronger regularization; on second failure, exclude from ensemble rather than blocking the run
- `notebooks/` is for exploration only; reusable logic lives in `src/`
