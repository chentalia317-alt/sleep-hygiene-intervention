import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import argparse
import pandas as pd
from pathlib import Path
from src.ids_and_columns import norm_pid, harmonize_columns

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", default="data/cleaned/baseline_cleaned_v7.csv")
    ap.add_argument("--a", default="data/cleaned/intervention_A_cleaned.csv")
    ap.add_argument("--b", default="data/cleaned/intervention_B_cleaned.csv")
    ap.add_argument("--out", default="refactor_outputs/combined_dataset.csv")
    args = ap.parse_args()

    base = pd.read_csv(args.baseline)
    A = pd.read_csv(args.a)
    B = pd.read_csv(args.b)

    for df in (base, A, B):
        if "participant_id" in df.columns:
            df["participant_id"] = df["participant_id"].map(norm_pid)

    base["phase"] = "baseline"
    A["phase"] = "intervention"; A["group"] = "A"
    B["phase"] = "intervention"; B["group"] = "B"

    base = harmonize_columns(base)
    A = harmonize_columns(A)
    B = harmonize_columns(B)

    # 对齐列集合
    common = set(base.columns) | set(A.columns) | set(B.columns)
    base = base.reindex(columns=sorted(common))
    A    = A.reindex(columns=sorted(common))
    B    = B.reindex(columns=sorted(common))

    combined = pd.concat([base, A, B], ignore_index=True)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    combined.to_csv(args.out, index=False, encoding="utf-8-sig")
    print(f"[OK] saved {args.out}")