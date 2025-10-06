import pandas as pd
import numpy as np
from pathlib import Path

# 定义文件路径
cleaned = Path("data/cleaned")

# 读取三份清洗后的数据
base = pd.read_csv(cleaned / "baseline_cleaned_v7.csv")
a = pd.read_csv(cleaned / "intervention_A_cleaned.csv")
b = pd.read_csv(cleaned / "intervention_B_cleaned.csv")

# 添加来源标识
base["phase"] = "baseline"
a["phase"] = "intervention"
b["phase"] = "intervention"

base["group"] = np.nan
a["group"] = "A"
b["group"] = "B"

# 统一列
cols = list(set(base.columns) | set(a.columns) | set(b.columns))
base = base.reindex(columns=cols)
a = a.reindex(columns=cols)
b = b.reindex(columns=cols)

# 合并
df = pd.concat([base, a, b], ignore_index=True)
# 计算睡眠时长（分钟和小时）
import numpy as np
def hhmm_to_min(x):
    try:
        h, m = map(int, str(x).split(":"))
        return h * 60 + m
    except:
        return np.nan

df["sleep_onset_min"] = df["sleep_onset_time"].apply(hhmm_to_min)
df["wake_min"] = df["wake_time"].apply(hhmm_to_min)
df["sleep_duration_min"] = df["wake_min"] - df["sleep_onset_min"]
df.loc[df["sleep_duration_min"] < 0, "sleep_duration_min"] += 24 * 60
df["sleep_duration_hr"] = df["sleep_duration_min"] / 60
# 输出
out = cleaned / "combined_dataset.csv"
df.to_csv(out, index=False, encoding="utf-8-sig")
print(f"合并完成：{out}")
print(f"行数：{len(df)}, 列数：{len(df.columns)}")
print("phase/group 列分布：")
print(df.groupby(['phase','group']).size())