import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# 读取合并后的总表
df = pd.read_csv("data/cleaned/combined_dataset.csv")

# —— 统一 participant_id：P001、P002 这种
def norm_pid(x: str):
    s = str(x).strip().replace(" ", "").upper()
    if s.startswith("P"):
        s = s[1:]
    digits = "".join(ch for ch in s if ch.isdigit())
    if digits == "":
        return np.nan
    return f"P{int(digits):03d}"

df["participant_id"] = df["participant_id"].apply(norm_pid)

# —— 计算睡眠时长（分钟），处理跨夜
def hhmm_to_min(x):
    try:
        h, m = map(int, str(x).split(":"))
        return h * 60 + m
    except:
        return np.nan

df["sleep_onset_min"] = df["sleep_onset_time"].apply(hhmm_to_min)
df["wake_min"]        = df["wake_time"].apply(hhmm_to_min)
df["sleep_duration_min"] = df["wake_min"] - df["sleep_onset_min"]
df.loc[df["sleep_duration_min"] < 0, "sleep_duration_min"] += 24 * 60  # 跨夜补 24h
df["sleep_duration_hr"] = df["sleep_duration_min"] / 60.0

# —— 每日 KSS 均值
df["kss_mean"] = df[["kss_morning","kss_afternoon","kss_evening"]].mean(axis=1)

# 诊断交集
base_ids = set(df.loc[df["phase"]=="baseline","participant_id"].dropna().unique())
intv_ids = set(df.loc[df["phase"]=="intervention","participant_id"].dropna().unique())
print("Baseline n IDs:", len(base_ids), "Intervention n IDs:", len(intv_ids), "Intersection:", len(base_ids & intv_ids))

# ========= 关键修复：baseline 聚合不带 group，之后再从干预期补回 group =========
# 1) 不带 group 的聚合（防止 baseline 因 NaN group 被丢）
agg = (df.groupby(["participant_id","phase"])
         .agg(kss_mean=("kss_mean","mean"),
              sleep_mean=("sleep_duration_min","mean"))
         .reset_index())

base = agg[agg["phase"]=="baseline"].copy()
intv = agg[agg["phase"]=="intervention"].copy()

# 2) 从干预期取 participant_id → group(A/B) 映射
group_map = (df.loc[df["phase"]=="intervention", ["participant_id","group"]]
               .dropna()
               .drop_duplicates())

# 3) 合并 baseline 与 intervention，再补回 group
merged = base.merge(
    intv[["participant_id","kss_mean","sleep_mean"]],
    on="participant_id",
    how="inner",
    suffixes=("_base","_int")
).merge(group_map, on="participant_id", how="left")

# 4) 计算 Δ 指标（分钟转小时）
merged["delta_kss"]   = merged["kss_mean_int"]  - merged["kss_mean_base"]
merged["delta_sleep"] = (merged["sleep_mean_int"] - merged["sleep_mean_base"]) / 60.0

print("合并完成，示例数据：")
print(merged[["participant_id","group","delta_kss","delta_sleep"]].head())
print("A_n / B_n:", (merged["group"]=="A").sum(), (merged["group"]=="B").sum())

# ===== 统计检验 =====
a_k = merged.loc[merged["group"]=="A","delta_kss"].dropna()
b_k = merged.loc[merged["group"]=="B","delta_kss"].dropna()
a_s = merged.loc[merged["group"]=="A","delta_sleep"].dropna()
b_s = merged.loc[merged["group"]=="B","delta_sleep"].dropna()

t1, p1 = stats.ttest_ind(a_k, b_k, equal_var=False)
t2, p2 = stats.ttest_ind(a_s, b_s, equal_var=False)

print("\n=== ΔKSS (intervention - baseline) ===")
print(f"A mean: {a_k.mean():.3f}, B mean: {b_k.mean():.3f}, t={t1:.3f}, p={p1:.4f}")
print("Sig." if p1 < 0.05 else "NS")

print("\n=== ΔSleep duration (h) (intervention - baseline) ===")
print(f"A mean: {a_s.mean():.3f}, B mean: {b_s.mean():.3f}, t={t2:.3f}, p={p2:.4f}")
print("Sig." if p2 < 0.05 else "NS")

# ===== 导出每人 Δ 表 =====
out_csv = "data/cleaned/delta_by_participant.csv"
merged.to_csv(out_csv, index=False, encoding="utf-8-sig")
print("saved:", out_csv)

# ===== 画图（英文标签避免中文字体告警）=====
plt.figure(figsize=(6,5))
plt.boxplot([a_k, b_k], labels=["A: Fixed window","B: No device"])
plt.title("ΔKSS (Intervention - Baseline)")
plt.ylabel("KSS change (lower is better)")
plt.grid(True, axis="y", linestyle="--", alpha=0.6)
plt.savefig("data/cleaned/delta_kss_boxplot.png", dpi=300, bbox_inches="tight")
plt.close()

plt.figure(figsize=(6,5))
plt.boxplot([a_s, b_s], labels=["A: Fixed window","B: No device"])
plt.title("ΔSleep duration (h) (Intervention - Baseline)")
plt.ylabel("Sleep duration change (hours)")
plt.grid(True, axis="y", linestyle="--", alpha=0.6)
plt.savefig("data/cleaned/delta_sleep_boxplot.png", dpi=300, bbox_inches="tight")
plt.close()

print("saved plots: delta_kss_boxplot.png, delta_sleep_boxplot.png")