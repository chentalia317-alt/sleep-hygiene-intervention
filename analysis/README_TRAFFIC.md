# GitHub Traffic Analytics

Run weekly to accumulate 14-day API windows into a long-term time series.

Quickstart:
1) Create a GitHub Personal Access Token with repo/traffic read.
2) export GITHUB_TOKEN="ghp_xxx..."
3) pip install -r analytics/requirements.txt
4) python analytics/github_traffic_tracker.py --owner <OWNER> --repo <REPO> --outdir analytics/traffic_out --label "<label>"