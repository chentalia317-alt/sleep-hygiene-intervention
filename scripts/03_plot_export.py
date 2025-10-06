# 读取 combined_dataset.csv 后：对每个 m 计算Δ/人，再分别画 A/B boxplot图
for m, ylabel in [("kss_mean","KSS change"), ("sleep_duration_h","Sleep duration change (h)")]:
    if m not in df.columns: continue
    base = df[df["phase"]=="baseline"].groupby("participant_id")[m].mean()
    inter = df[df["phase"]=="intervention"].groupby("participant_id")[m].mean()
    d = (inter - base).dropna().to_frame("delta")
    groups = (df[df["phase"]=="intervention"]
              .groupby("participant_id")["group"].agg(lambda s: s.mode().iat[0]))
    d = d.join(groups, how="inner")
    a, b = d.loc[d["group"]=="A","delta"], d.loc[d["group"]=="B","delta"]

    import matplotlib.pyplot as plt
    import pathlib
    out = pathlib.Path("refactor_outputs/figures"); out.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(6,5))
    plt.boxplot([a, b], labels=["A: Fixed window","B: No device"])
    plt.title(f"Δ{m} (intervention - baseline)")
    plt.ylabel(ylabel); plt.grid(True, axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout(); plt.savefig(out / f"delta_{m}.png", dpi=200); plt.close()
print("[OK] figures saved")