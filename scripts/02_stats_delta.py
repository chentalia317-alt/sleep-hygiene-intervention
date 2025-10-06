# 读取 combined_dataset.csv 后：
summary_rows = []
for m in ["kss_mean","sleep_duration_h"]:
    if m not in df.columns: 
        continue
    # 每人的Δ
    base = df[df["phase"]=="baseline"].groupby("participant_id")[m].mean()
    inter = df[df["phase"]=="intervention"].groupby("participant_id")[m].mean()
    d = (inter - base).dropna()

    # 带组别
    groups = (df[df["phase"]=="intervention"]
              .groupby("participant_id")["group"].agg(lambda s: s.mode().iat[0]))
    d = d.to_frame("delta").join(groups, how="inner")

    a = d.loc[d["group"]=="A","delta"].dropna()
    b = d.loc[d["group"]=="B","delta"].dropna()

    from scipy import stats
    t_p = stats.ttest_ind(a, b, equal_var=False, nan_policy="omit").pvalue

    summary_rows.append({
        "metric": m,
        "n_A": len(a), "n_B": len(b),
        "mean_delta_A": a.mean(), "mean_delta_B": b.mean(),
        "t_p": t_p
    })

pd.DataFrame(summary_rows).to_csv("refactor_outputs/results_summary.csv", index=False)
print("[OK] saved refactor_outputs/results_summary.csv")