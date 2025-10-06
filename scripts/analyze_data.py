import pandas as pd
import numpy as np

# 读取数据
df = pd.read_csv("data/cleaned/combined_dataset.csv")

# 计算每个被试的平均KSS
avg_kss = df.groupby("participant_id")[["kss_morning", "kss_afternoon", "kss_evening"]].mean().reset_index()
avg_kss["kss_mean_all"] = avg_kss[["kss_morning", "kss_afternoon", "kss_evening"]].mean(axis=1)

# 计算睡眠时长均值
if "sleep_duration_hr" in df.columns:
    sleep_stats = df.groupby("participant_id")["sleep_duration_hr"].mean().reset_index().rename(columns={"sleep_duration_hr": "sleep_duration_mean"})
    result = pd.merge(avg_kss, sleep_stats, on="participant_id", how="left")
else:
    result = avg_kss.copy()

# 结果
out = "data/cleaned/summary_by_participant.csv"
result.to_csv(out, index=False, encoding="utf-8-sig")
print(f"分析完成！结果已输出到：{out}")