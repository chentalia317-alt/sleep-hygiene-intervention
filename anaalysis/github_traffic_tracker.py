import argparse
import json
import os
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import requests

API_BASE = "https://api.github.com"
API_VERSION = "2022-11-28"

def _headers():
    token = os.getenv("GITHUB_TOKEN", "").strip()
    if not token:
        raise RuntimeError("Missing env var GITHUB_TOKEN. Please set it to a personal access token.")
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": API_VERSION,
        "User-Agent": "traffic-tracker-script"
    }

def fetch_traffic(owner: str, repo: str, per: str = "day"):
    s = requests.Session()
    s.headers.update(_headers())
    views_url = f"{API_BASE}/repos/{owner}/{repo}/traffic/views?per={per}"
    clones_url = f"{API_BASE}/repos/{owner}/{repo}/traffic/clones?per={per}"
    rv = {}
    r1 = s.get(views_url, timeout=30)
    if r1.status_code == 200:
        rv["views"] = r1.json()
    else:
        raise RuntimeError(f"Views fetch failed: {r1.status_code} {r1.text}")
    r2 = s.get(clones_url, timeout=30)
    if r2.status_code == 200:
        rv["clones"] = r2.json()
    else:
        raise RuntimeError(f"Clones fetch failed: {r2.status_code} {r2.text}")
    return rv

def rows_from_payload(payload):
    rows = {}
    for entry in payload.get("views", {}).get("views", []):
        ts = entry.get("timestamp")
        date = ts[:10] if ts else None
        if not date: continue
        rows[date] = {"date": date, "views_total": entry.get("count", 0),
                      "views_unique": entry.get("uniques", 0),
                      "clones_total": 0, "clones_unique": 0}
    for entry in payload.get("clones", {}).get("clones", []):
        ts = entry.get("timestamp")
        date = ts[:10] if ts else None
        if not date: continue
        if date not in rows:
            rows[date] = {"date": date, "views_total": 0, "views_unique": 0,
                          "clones_total": entry.get("count", 0),
                          "clones_unique": entry.get("uniques", 0)}
        else:
            rows[date]["clones_total"] = entry.get("count", 0)
            rows[date]["clones_unique"] = entry.get("uniques", 0)
    return pd.DataFrame([rows[k] for k in sorted(rows.keys())])

def merge_into_csv(df_new: pd.DataFrame, csv_path: Path):
    cols = ["date","views_total","views_unique","clones_total","clones_unique"]
    df_new = df_new[cols].drop_duplicates(subset=["date"])
    if csv_path.exists():
        df_old = pd.read_csv(csv_path, dtype={"date": str})
        df = pd.concat([df_old, df_new], ignore_index=True)
        df = df.sort_values("date").drop_duplicates(subset=["date"], keep="last")
    else:
        df = df_new
    df = df.sort_values("date")
    df.to_csv(csv_path, index=False)
    return df

def plot_series(df: pd.DataFrame, outdir: Path, label: str = ""):
    if df.empty: return
    # Views
    plt.figure()
    plt.plot(pd.to_datetime(df["date"]), df["views_total"], label="Total views")
    plt.plot(pd.to_datetime(df["date"]), df["views_unique"], label="Unique visitors")
    title = "GitHub Views Over Time" + (f" – {label}" if label else "")
    plt.title(title); plt.xlabel("Date"); plt.ylabel("Count"); plt.legend(); plt.tight_layout()
    plt.savefig(outdir / "traffic_views.png", dpi=200); plt.close()
    # Clones
    plt.figure()
    plt.plot(pd.to_datetime(df["date"]), df["clones_total"], label="Total clones")
    plt.plot(pd.to_datetime(df["date"]), df["clones_unique"], label="Unique cloners")
    title = "GitHub Clones Over Time" + (f" – {label}" if label else "")
    plt.title(title); plt.xlabel("Date"); plt.ylabel("Count"); plt.legend(); plt.tight_layout()
    plt.savefig(outdir / "traffic_clones.png", dpi=200); plt.close()

def main():
    parser = argparse.ArgumentParser(description="Track GitHub traffic and plot trends.")
    parser.add_argument("--owner", required=True, help="Repo owner/org (e.g., 'chentailia317-alt')")
    parser.add_argument("--repo", required=True, help="Repo name (e.g., 'sleep-hygiene-intervention')")
    parser.add_argument("--outdir", default="traffic_out", help="Output dir (default: traffic_out)")
    parser.add_argument("--label", default="", help="Figure title label")
    parser.add_argument("--no-plots", action="store_true", help="Skip plotting")
    parser.add_argument("--verbose", action="store_true", help="Verbose logs")
    args = parser.parse_args()

    outdir = Path(args.outdir); outdir.mkdir(parents=True, exist_ok=True)
    csv_path = outdir / "traffic_history.csv"

    payload = fetch_traffic(args.owner, args.repo, per="day")
    if args.verbose:
        print(json.dumps(payload.get("views", {}), indent=2)[:500] + " ...")
        print(json.dumps(payload.get("clones", {}), indent=2)[:500] + " ...")

    df_new = rows_from_payload(payload)
    df = merge_into_csv(df_new, csv_path)

    if not args.no_plots:
        plot_series(df, outdir, label=args.label or args.repo)

    if not df.empty:
        last_date = df["date"].iloc[-1]
        print(f"[✓] Updated through {last_date}")
        print(f"[i] CSV: {csv_path}")
        print(f"[i] PNG: {outdir/'traffic_views.png'}, {outdir/'traffic_clones.png'}")
    else:
        print("[!] No data rows. Check API permissions or repo visibility.")

if __name__ == "__main__":
    main()
