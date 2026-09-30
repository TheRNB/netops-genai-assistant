import matplotlib

matplotlib.use("Agg")  # must run before importing pyplot to force the non-interactive backend

import matplotlib.pyplot as plt
import pandas as pd

from src.config import OPS_KPI_CSV, REPORTS_DIR

METRICS = ["latency_ms", "throughput_mbps", "packet_loss_pct"]
Z_THRESHOLD = 3.0  # per-site z-score cutoff; simpler and more interpretable than IsolationForest for a stationary hourly baseline per site


def load_kpis() -> pd.DataFrame:
    df = pd.read_csv(OPS_KPI_CSV, parse_dates=["timestamp"])
    return df


def flag_anomalies(df: pd.DataFrame, threshold: float = Z_THRESHOLD) -> pd.DataFrame:
    df = df.copy()
    for metric in METRICS:
        grouped = df.groupby("site_id")[metric]
        z = (df[metric] - grouped.transform("mean")) / grouped.transform("std")
        df[f"{metric}_z"] = z
    df["flagged"] = (df[[f"{m}_z" for m in METRICS]].abs() > threshold).any(axis=1)
    return df


def profile_sites(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("site_id")[METRICS].agg(["mean", "std"])


def top_anomalous_sites(df: pd.DataFrame, n: int = 5) -> pd.Series:
    return df[df["flagged"]].groupby("site_id").size().sort_values(ascending=False).head(n)


def plot_kpi_trend(df: pd.DataFrame, site_id: str, out_path):
    site_df = df[df["site_id"] == site_id]
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(site_df["timestamp"], site_df["latency_ms"], label="latency_ms")
    anomalies = site_df[site_df["flagged"]]
    ax.scatter(anomalies["timestamp"], anomalies["latency_ms"], color="red", label="flagged anomaly", zorder=3)
    ax.set_title(f"Latency trend with flagged anomalies — {site_id}")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def plot_incidents_per_site(df: pd.DataFrame, out_path):
    counts = df[df["flagged"]].groupby("site_id").size().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 4))
    counts.plot(kind="bar", ax=ax)
    ax.set_title("Flagged anomalies per site")
    ax.set_ylabel("count")
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def plot_incident_type_breakdown(df: pd.DataFrame, out_path):
    counts = df[df["incident_label"] != "none"]["incident_label"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 6))
    counts.plot(kind="pie", ax=ax, autopct="%1.0f%%")
    ax.set_title("Incident type breakdown")
    ax.set_ylabel("")
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def write_insights(df: pd.DataFrame, out_path):
    top_sites = top_anomalous_sites(df)
    lines = ["Top anomalous sites (by flagged-row count):"]
    lines += [f"  {site}: {count}" for site, count in top_sites.items()]
    lines.append("")
    lines.append(f"Total rows: {len(df)}, flagged: {int(df['flagged'].sum())} ({df['flagged'].mean():.2%})")
    lines.append(f"Incident types present: {sorted(df[df['incident_label'] != 'none']['incident_label'].unique())}")
    out_path.write_text("\n".join(lines))


def run():
    REPORTS_DIR.mkdir(exist_ok=True)
    df = flag_anomalies(load_kpis())
    sample_site = df["site_id"].iloc[0]
    plot_kpi_trend(df, sample_site, REPORTS_DIR / "kpi_trend_anomalies.png")
    plot_incidents_per_site(df, REPORTS_DIR / "incidents_per_site.png")
    plot_incident_type_breakdown(df, REPORTS_DIR / "incident_type_breakdown.png")
    write_insights(df, REPORTS_DIR / "insights.txt")
    print((REPORTS_DIR / "insights.txt").read_text())


if __name__ == "__main__":
    run()
