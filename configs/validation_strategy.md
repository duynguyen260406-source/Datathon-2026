# Validation Strategy

## Frozen Setup

- Validation type: fixed cross-validation
- Number of folds: `5`
- Random seed: `20260324`
- Assignment file: `configs/folds_v1.csv`

## Why This Strategy

The training set only has `221` rows, so a single holdout would be too noisy for model comparison. A fixed 5-fold split gives more stable feedback and lets every row act as validation exactly once.

## How Rows Are Stratified

Each row is assigned to a stratum using:

1. `event`
2. a within-event quantile bin of `time_to_hit_hours`

That creates strata such as:

- `0_q1` to `0_q4` for censored rows
- `1_q1` to `1_q4` for hit rows

This keeps each fold similar in both event rate and target-time difficulty.

## Team Rule

Do not reshuffle or regenerate the fold file while comparing models. Every experiment should train and validate on the exact same `configs/folds_v1.csv` assignments unless the training dataset itself changes.

## Current Fold Balance

| Fold | Rows | Events | Censored | Event Rate | Mean Time To Hit |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0 | 45 | 14 | 31 | 0.3111 | 36.8607 |
| 1 | 44 | 13 | 31 | 0.2955 | 37.2653 |
| 2 | 44 | 14 | 30 | 0.3182 | 37.3707 |
| 3 | 44 | 14 | 30 | 0.3182 | 37.9734 |
| 4 | 44 | 14 | 30 | 0.3182 | 38.3841 |
