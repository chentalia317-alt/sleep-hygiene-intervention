import pandas as pd
from scipy import stats

# 读取合并后的大表
df = pd.read_csv("data/cleaned/combined_dataset.csv")

# 只看干预期（A/B组在这里才有group）
df = df[df["phase"] == "intervention"].copy()

# 确保有 group 列（A/B），如果有缺失就丢弃
df = df.dropna(subset=["group"])

# 计算每日的 kss_mean（早中晚平均）
df["kss_mean"] = df[["kss_morning", "kss_afternoon", "kss_evening"]].mean(axis=1)

# 分组描述统计
summary = df.groupby("group")["kss_mean"].agg(["mean", "std", "count"])
print("\n=== 各组平均KSS（干预期） ===")
print(summary)

# A vs B 独立样本 t 检验（Welch）
a_values = df.loc[df["group"] == "A", "kss_mean"].dropna()
b_values = df.loc[df["group"] == "B", "kss_mean"].dropna()

t_stat, p_value = stats.ttest_ind(a_values, b_values, equal_var=False, nan_policy="omit")
print("\n=== 独立样本 t 检验（干预期 A vs B） ===")
print(f"t = {t_stat:.3f}, p = {p_value:.4f}")
print("差异显著（p < 0.05）" if p_value < 0.05 else "差异不显著（p ≥ 0.05）")

# 可选：保存分组统计
summary.to_csv("data/cleaned/group_kss_summary_intervention.csv", encoding="utf-8-sig")
print("\n📁 已保存：data/cleaned/group_kss_summary_intervention.csv")