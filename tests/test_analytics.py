import pandas as pd

from src.analytics import flag_anomalies, load_kpis, run
from src.config import REPORTS_DIR


def test_flag_anomalies_catches_known_incidents():
    df = flag_anomalies(load_kpis())
    labeled = df[df["incident_label"] != "none"]
    assert labeled["flagged"].mean() > 0.8  # most injected anomalies should be caught


def test_flag_anomalies_does_not_flag_normal_rows_much():
    df = flag_anomalies(load_kpis())
    normal = df[df["incident_label"] == "none"]
    assert normal["flagged"].mean() < 0.1  # z>3 should be rare on normal rows


def test_flag_anomalies_synthetic_spike_is_flagged():
    rows = [{"timestamp": f"2026-01-01T{h:02d}:00:00", "site_id": "site_x", "latency_ms": 50.0,
              "throughput_mbps": 100.0, "packet_loss_pct": 0.2, "incident_label": "none"} for h in range(20)]
    rows.append({"timestamp": "2026-01-01T20:00:00", "site_id": "site_x", "latency_ms": 500.0,
                 "throughput_mbps": 100.0, "packet_loss_pct": 0.2, "incident_label": "none"})
    df = pd.DataFrame(rows)
    flagged = flag_anomalies(df)
    assert flagged.iloc[-1]["flagged"]
    assert not flagged.iloc[0]["flagged"]


def test_run_produces_reports():
    run()
    assert (REPORTS_DIR / "kpi_trend_anomalies.png").exists()
    assert (REPORTS_DIR / "incidents_per_site.png").exists()
    assert (REPORTS_DIR / "incident_type_breakdown.png").exists()
    assert (REPORTS_DIR / "insights.txt").exists()
