# Initial EDA Summary

## Dataset Snapshot

- Train shape: `221 x 37`
- Test shape: `95 x 35`
- Shared columns between train and test: `35`
- Train-only columns: `event`, `time_to_hit_hours`
- Identifier columns: `1`
- Target columns: `2`
- Modeling features: `34`

## Data Quality

- Total missing values in train: `0`
- Total missing values in test: `0`
- Duplicate `event_id` values in train: `0`
- Duplicate `event_id` values in test: `0`
- Shared `event_id` values across train and test: `0`
- No immediate imputation work is required for the baseline pipeline.

## Survival Target Snapshot

- Event rate: `31.22%`
- Censoring rate: `68.78%`
- `time_to_hit_hours` summary on train:
  - mean: `37.57`
  - std: `25.90`
  - min: `0.0012`
  - 25th percentile: `12.24`
  - median: `43.11`
  - 75th percentile: `63.94`
  - max: `66.99`

## Horizon-Level Labeling Context

These are useful checks for horizon-specific models before censor-aware filtering:

- By `12h`: observed positives `22.17%`, known negatives `75.11%`, censored at or before horizon `2.71%`
- By `24h`: observed positives `28.51%`, known negatives `60.18%`, censored at or before horizon `11.31%`
- By `48h`: observed positives `29.86%`, known negatives `45.25%`, censored at or before horizon `24.89%`
- By `72h`: observed positives `31.22%`, known negatives `0.00%`, censored at or before horizon `68.78%`

Implication: direct horizon models must handle censoring carefully, especially for the later horizons.

## Feature Inventory

Feature categories from metadata:

- Growth: `10`
- Distance: `9`
- Centroid kinematics: `5`
- Directionality: `4`
- Temporal coverage: `3`
- Temporal metadata: `3`

## Useful Early Slice

- `low_temporal_resolution_0_5h = 1` for `72.85%` of training rows.
- Event rate when `low_temporal_resolution_0_5h = 0`: `60.00%`
- Event rate when `low_temporal_resolution_0_5h = 1`: `20.50%`

Implication: temporal-resolution quality is likely an important baseline feature and a useful analysis slice for validation.

## First Train/Test Drift Check

The largest standardized mean shifts are still relatively modest in absolute scale, but the most different columns are concentrated in size, motion, and growth:

1. `area_first_ha` (`0.188`)
2. `event_start_dayofweek` (`0.149`)
3. `radial_growth_rate_m_per_h` (`0.144`)
4. `alignment_abs` (`0.136`)
5. `area_growth_rate_ha_per_h` (`0.135`)
6. `radial_growth_m` (`0.134`)
7. `centroid_speed_m_per_h` (`0.128`)
8. `area_growth_abs_0_5h` (`0.124`)
9. `log1p_growth` (`0.115`)
10. `centroid_displacement_m` (`0.115`)

Implication: start with a robust tabular baseline, then revisit calibration and shift-sensitive features after out-of-fold scoring is in place.
