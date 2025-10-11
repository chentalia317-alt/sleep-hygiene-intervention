#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_figures.py
Create three figures from a sleep-intervention dataset:
  1) KSS mean trend by Day (±1 SD)
  2) Sleep Duration mean trend by Day (±1 SD)
  3) Compliance rate trend by Day (% Completed)

Default columns (can be changed by CLI):
  Day, KSS, SleepDuration, Completed (0/1)
Usage (example):
  python generate_figures.py --csv processed/processed_data.csv --outdir figures --baseline_days 5
"""

import argparse
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Quick config (optional)
DEFAULT_CSV = "processed/processed_data.csv"
DEFAULT_OUTDIR = "figures"
DEFAULT_DAY = "Day"
DEFAULT_KSS = "KSS"
DEFAULT_SLEEP = "SleepDuration"
DEFAULT_COMPLETED = "Completed"
DEFAULT_BASELINE_DAYS = 5  # set to None if you don't want shading

def coerce_day(series: pd.Series) -> pd.Series:
    """Coerce Day labels to ordered numeric 1..N, preserving original order when non-numeric."""
    try:
        return pd.to_numeric(series, errors='raise')
    except Exception:
        cats = pd.Categorical(series, ordered=True)
        mapping = {cat: i+1 for i, cat in enumerate(cats.categories)}
        return series.map(mapping)

def summarize_by_day(df: pd.DataFrame, day_col: str, value_col: str) -> pd.DataFrame:
    g = df.groupby(day_col)[value_col]
    mean = g.mean()
    std = g.std(ddof=1)
    n = g.count()
    out = pd.DataFrame({"mean": mean, "std": std, "n": n}).reset_index()
    return out

def plot_with_band(day, mean, std, ylabel, title, outfile, annotate_phases=None):
    plt.figure()
    plt.plot(day, mean, marker='o')
    if std is not None:
        lower, upper = mean - std, mean + std
        plt.fill_between(day, lower, upper, alpha=0.2)
    plt.xlabel("Day")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True, alpha=0.4, linestyle='--')
    if annotate_phases:
        ax = plt.gca()
        for (start, end, label) in annotate_phases:
            ax.axvspan(start, end, alpha=0.08)
            ax.text((start + end) / 2.0, ax.get_ylim()[1] * 0.95, label,
                    ha='center', va='top', fontsize=9)
    plt.tight_layout()
    os.makedirs(os.path.dirname(outfile), exist_ok=True)
    plt.savefig(outfile, dpi=300)
    plt.close()

def main():
    p = argparse.ArgumentParser(description="Generate KSS, SleepDuration, and Compliance figures.")
    p.add_argument("--csv", default=DEFAULT_CSV, help="Path to CSV file")
    p.add_argument("--outdir", default=DEFAULT_OUTDIR, help="Output directory")
    p.add_argument("--day_column", default=DEFAULT_DAY, help="Day column")
    p.add_argument("--kss_column", default=DEFAULT_KSS, help="KSS column")
    p.add_argument("--sleep_column", default=DEFAULT_SLEEP, help="Sleep duration (hours) column")
    p.add_argument("--completed_column", default=DEFAULT_COMPLETED, help="0/1 completion column")
    p.add_argument("--baseline_days", type=int,
                   default=(DEFAULT_BASELINE_DAYS if DEFAULT_BASELINE_DAYS is not None else 0),
                   help="Number of baseline days; 0 to disable shading")
    args = p.parse_args()

    df = pd.read_csv(args.csv)

    # Prepare Day
    if args.day_column not in df.columns:
        raise ValueError(f"Day column '{args.day_column}' not found.")
    df["_DayNumeric"] = coerce_day(df[args.day_column])

    # (1) KSS trend
    if args.kss_column in df.columns:
        kss = summarize_by_day(df, "_DayNumeric", args.kss_column).sort_values("_DayNumeric")
        phases = None
        if args.baseline_days and args.baseline_days > 0:
            max_day = int(kss["_DayNumeric"].max())
            b_end = min(args.baseline_days, max_day)
            phases = [(1, b_end, "Baseline"), (b_end, max_day, "Intervention")]
        plot_with_band(
            day=kss["_DayNumeric"].values,
            mean=kss["mean"].values,
            std=kss["std"].values,
            ylabel="Mean KSS",
            title="Daily Mean KSS (±1 SD)",
            outfile=os.path.join(args.outdir, "KSS_trend.png"),
            annotate_phases=phases
        )
    else:
        print(f"[Skip] Missing column: {args.kss_column}")

    # (2) Sleep Duration trend
    if args.sleep_column in df.columns:
        slp = summarize_by_day(df, "_DayNumeric", args.sleep_column).sort_values("_DayNumeric")
        phases = None
        if args.baseline_days and args.baseline_days > 0:
            max_day = int(slp["_DayNumeric"].max())
            b_end = min(args.baseline_days, max_day)
            phases = [(1, b_end, "Baseline"), (b_end, max_day, "Intervention")]
        plot_with_band(
            day=slp["_DayNumeric"].values,
            mean=slp["mean"].values,
            std=slp["std"].values,
            ylabel="Sleep Duration (hours)",
            title="Daily Sleep Duration (±1 SD)",
            outfile=os.path.join(args.outdir, "SleepDuration_trend.png"),
            annotate_phases=phases
        )
    else:
        print(f"[Skip] Missing column: {args.sleep_column}")

    # (3) Compliance trend
    if args.completed_column in df.columns:
        comp = df.groupby("_DayNumeric")[args.completed_column].mean().reset_index().sort_values("_DayNumeric")
        phases = None
        if args.baseline_days and args.baseline_days > 0:
            max_day = int(comp["_DayNumeric"].max())
            b_end = min(args.baseline_days, max_day)
            phases = [(1, b_end, "Baseline"), (b_end, max_day, "Intervention")]

        plt.figure()
        plt.plot(comp["_DayNumeric"].values, (comp[args.completed_column].values * 100.0), marker='o')
        plt.xlabel("Day")
        plt.ylabel("Compliance Rate (%)")
        plt.title("Daily Compliance Rate")
        plt.grid(True, alpha=0.4, linestyle='--')
        if phases:
            ax = plt.gca()
            for (start, end, label) in phases:
                ax.axvspan(start, end, alpha=0.08)
                ax.text((start + end) / 2.0, ax.get_ylim()[1] * 0.95, label,
                        ha='center', va='top', fontsize=9)
        plt.tight_layout()
        os.makedirs(args.outdir, exist_ok=True)
        plt.savefig(os.path.join(args.outdir, "Compliance_rate_trend.png"), dpi=300)
        plt.close()
    else:
        print(f"[Skip] Missing column: {args.completed_column}")

    print(f"Figures saved to: {args.outdir}")

if __name__ == "__main__":
    main()