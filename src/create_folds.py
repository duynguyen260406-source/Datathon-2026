from pathlib import Path
import random

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TRAIN_PATH = PROJECT_ROOT / "data" / "raw" / "train.csv"
OUTPUT_PATH = PROJECT_ROOT / "configs" / "folds_v1.csv"
SEED = 20260324
N_FOLDS = 5
N_BINS = 4


def quantile_bins(series: pd.Series, n_bins: int) -> pd.Series:
    ranks = series.rank(method="first")
    return pd.qcut(ranks, q=min(n_bins, len(series)), labels=False, duplicates="drop")


def build_folds(train_df: pd.DataFrame) -> pd.DataFrame:
    folds = train_df[["event_id", "event", "time_to_hit_hours"]].copy()
    folds["time_bin_within_event"] = (
        folds.groupby("event", group_keys=False)["time_to_hit_hours"]
        .apply(lambda s: quantile_bins(s, N_BINS))
        .astype(int)
    )
    folds["stratum"] = (
        folds["event"].astype(str)
        + "_q"
        + (folds["time_bin_within_event"] + 1).astype(str)
    )
    folds["fold"] = -1

    rng = random.Random(SEED)
    fold_counts = {fold: 0 for fold in range(N_FOLDS)}
    grouped = sorted(
        folds.groupby("stratum").groups.items(),
        key=lambda item: (-len(item[1]), item[0]),
    )

    for _, row_indices in grouped:
        row_indices = list(row_indices)
        rng.shuffle(row_indices)
        fold_order = sorted(fold_counts, key=lambda fold: (fold_counts[fold], fold))

        for index, row_idx in enumerate(row_indices):
            fold = fold_order[index % N_FOLDS]
            folds.at[row_idx, "fold"] = fold
            fold_counts[fold] += 1

    return folds.sort_values(["fold", "stratum", "event_id"]).reset_index(drop=True)


def summarize_folds(folds: pd.DataFrame) -> pd.DataFrame:
    return (
        folds.groupby("fold")
        .agg(
            rows=("event_id", "size"),
            event_count=("event", "sum"),
            censor_count=("event", lambda s: int((s == 0).sum())),
            event_rate=("event", "mean"),
            mean_time_to_hit=("time_to_hit_hours", "mean"),
        )
        .round(4)
    )


def main() -> None:
    train_df = pd.read_csv(TRAIN_PATH)
    folds = build_folds(train_df)

    if len(folds) != len(train_df):
        raise ValueError("Fold file row count does not match training data row count.")
    if folds["event_id"].duplicated().any():
        raise ValueError("Duplicate event_id values detected in fold assignments.")
    if (folds["fold"] < 0).any():
        raise ValueError("Some rows were not assigned to a fold.")

    folds.to_csv(OUTPUT_PATH, index=False)

    print("Saved:", OUTPUT_PATH)
    print(summarize_folds(folds).to_string())


if __name__ == "__main__":
    main()
