import numpy as np

def norm_pid(x: str):
    """标准化 participant_id，例如 'p1' -> 'P001'"""
    s = str(x).strip().replace(" ", "").upper()
    if s.startswith("P"):
        s = s[1:]
    digits = "".join(ch for ch in s if ch.isdigit())
    return f"P{int(digits):03d}" if digits.isdigit() else np.nan

def harmonize_columns(df):
    """统一列名并生成 kss_mean"""
    if "sleep_duration_hr" in df.columns and "sleep_duration_h" not in df.columns:
        df = df.rename(columns={"sleep_duration_hr":"sleep_duration_h"})
    kss_cols = [c for c in ["kss_morning","kss_afternoon","kss_evening"] if c in df.columns]
    if kss_cols:
        df["kss_mean"] = df[kss_cols].mean(axis=1)
    return df