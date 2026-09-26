"""One-off generator for the synthetic ops-KPI CSV (not part of the app runtime)."""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "data" / "ops_kpis.csv"
rng = np.random.default_rng(42)

SITES = [f"site_{i:02d}" for i in range(1, 21)]
HOURS = 24 * 14  # two weeks, hourly
START = datetime(2026, 9, 1)

rows = []
for site in SITES:
    base_latency = rng.uniform(20, 60)
    base_throughput = rng.uniform(80, 300)
    base_loss = rng.uniform(0.05, 0.3)
    for h in range(HOURS):
        ts = START + timedelta(hours=h)
        latency = base_latency + rng.normal(0, 3)
        throughput = base_throughput + rng.normal(0, 15)
        loss = max(0.0, base_loss + rng.normal(0, 0.05))
        incident_label = "none"

        if rng.random() < 0.03:
            kind = rng.choice(["latency_spike", "packet_loss", "link_down", "congestion"])
            if kind == "latency_spike":
                latency *= rng.uniform(3, 6)
            elif kind == "packet_loss":
                loss += rng.uniform(2, 8)
            elif kind == "link_down":
                throughput *= 0.05
                latency *= 4
                loss += 10
            elif kind == "congestion":
                throughput *= 0.4
                latency *= 2
            incident_label = kind

        rows.append({
            "timestamp": ts.isoformat(),
            "site_id": site,
            "latency_ms": round(max(latency, 1), 2),
            "throughput_mbps": round(max(throughput, 0), 2),
            "packet_loss_pct": round(max(loss, 0), 3),
            "incident_label": incident_label,
        })

df = pd.DataFrame(rows)
df.to_csv(OUT, index=False)
print(f"Wrote {len(df)} rows to {OUT}; incidents: {(df.incident_label != 'none').sum()}")
