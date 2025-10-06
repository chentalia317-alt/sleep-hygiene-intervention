# 读取 combined_dataset.csv - 计算每人 Δ=干预-基线 - A/B 组做 Welch t-test
import argparse
from pathlib import Path
import pandas as pd
from scipy import stats

def compute_summary(df: pd.DataFrame, metric: str) -> dict | None:
    if metric not in df.columns:
        return None
    base = df[df["phase"]=="baseline"].groupby("participant_id")[metric].mean()
    inter = df[df["phase"]=="intervention"].groupby("participant_id")[metric].mean()
    delta = (inter - base).dropna().to_frame("delta")
    # 干预期的组别众数作为参与者分组
    groups = (df[df["phase"]=="intervention"]
              .groupby("participant_id")["group"]
              .agg(lambda s: s.mode().iat[0] if not s.mode().empty else None))
    d = delta.join(groups, how="inner")
    a = d.loc[d["group"]=="A","delta"].dropna()
    b = d.loc[d["group"]=="B","delta"].dropna()
    pval = float(stats.ttest_ind(a, b, equal_var=False, nan_policy="omit").pvalue) if len(a)>0 and len(b)>0 else None
    return {
        "metric": metric,
        "n_A": int(len(a)), "n_B": int(len(b)),
        "mean_delta_A": float(a.mean()) if len(a) else None,
        "mean_delta_B": float(b.mean()) if len(b) else None,
        "t_p": pval,
    }

def main(infile: str, outfile: str):
    df = pd.read_csv(infile)
    # 统一列名（如果有）
    if "sleep_duration_hr" in df.columns and "sleep_duration_h" not in df.columns:
        df = df.rename(columns={"sleep_duration_hr": "sleep_duration_h"})
    rows = []
    for m in ["kss_mean","sleep_duration_h"]:
        res = compute_summary(df, m)
        if res: rows.append(res)
    out = pd.DataFrame(rows)
    Path(outfile).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(outfile, index=False, encoding="utf-8-sig")
    print(f"[OK] saved {outfile}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--infile", default="refactor_outputs/combined_dataset.csv")
    ap.add_argument("--out", default="refactor_outputs/results_summary.csv")
    args = ap.parse_args()
    main(args.infile, args.out)