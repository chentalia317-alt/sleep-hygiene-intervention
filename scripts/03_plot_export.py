# 读取 combined_dataset.csv - 为每人计算 Δ - 绘制 A/B 组箱线图
import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

def deltas_by_group(df: pd.DataFrame, metric: str):
    base = df[df["phase"]=="baseline"].groupby("participant_id")[metric].mean()
    inter = df[df["phase"]=="intervention"].groupby("participant_id")[metric].mean()
    delta = (inter - base).dropna().to_frame("delta")
    groups = (df[df["phase"]=="intervention"]
              .groupby("participant_id")["group"]
              .agg(lambda s: s.mode().iat[0] if not s.mode().empty else None))
    d = delta.join(groups, how="inner")
    a = d.loc[d["group"]=="A","delta"].dropna()
    b = d.loc[d["group"]=="B","delta"].dropna()
    return a, b

def make_box(a, b, title, ylabel, outpath: Path):
    outpath.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(6,5))
    plt.boxplot([a, b], labels=["A: Fixed window","B: No device"])
    plt.title(title)
    plt.ylabel(ylabel)
    plt.grid(True, axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()
    print(f"[OK] saved {outpath}")

def main(infile: str, figdir: str):
    df = pd.read_csv(infile)
    if "sleep_duration_hr" in df.columns and "sleep_duration_h" not in df.columns:
        df = df.rename(columns={"sleep_duration_hr": "sleep_duration_h"})
    figdir = Path(figdir)
    # KSS
    if "kss_mean" in df.columns:
        a,b = deltas_by_group(df, "kss_mean")
        make_box(a, b, "ΔKSS (Intervention - Baseline)", "KSS change (lower is better)", figdir/"delta_kss_boxplot.png")
    # Sleep duration (hours)
    if "sleep_duration_h" in df.columns:
        a,b = deltas_by_group(df, "sleep_duration_h")
        make_box(a, b, "ΔSleep duration (Intervention - Baseline)", "Hours change", figdir/"delta_sleep_boxplot.png")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--infile", default="refactor_outputs/combined_dataset.csv")
    ap.add_argument("--figdir", default="refactor_outputs/figures")
    args = ap.parse_args()
    main(args.infile, args.figdir)