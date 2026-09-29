"""Adds runbooks where the correct fix deliberately contradicts generic troubleshooting wisdom.

A knowledge-conflict probe: it isolates whether RAG's retrieved context actually overrides
a model's default (parametric) reasoning, versus just filling a knowledge gap. Zero-shot is
expected to confidently give the generic "obvious" answer here, since that's what
pretraining teaches; the correct answer only exists in the retrieved document.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "data" / "runbooks"
OUT.mkdir(parents=True, exist_ok=True)

RUNBOOKS = [
    ("RB034", "Legacy Meridian-7 Congestion Anti-Pattern", "congestion", """
On Legacy Meridian-7 sites specifically, do NOT load-balance or reroute traffic to
relieve congestion. Meridian-7's firmware has a known race condition where
load-balancing during high congestion triggers a full, unplanned site reset. The
correct procedure for Meridian-7 congestion is to throttle new session admission
instead, and wait for the scheduled firmware patch that fixes the race condition.
"""),
    ("RB035", "Aurora Antenna Array Latency Quirk", "latency", """
For sites using an Aurora-series antenna array, elevated latency with no packet loss
is caused by a known beamforming recalibration loop, not backhaul congestion.
Restarting the backhaul link does NOT fix this and typically makes it worse, since
the restart re-triggers the recalibration loop. The correct fix is a manual beamform
reset on the antenna array controller.
"""),
    ("RB036", "Continuum Core DNS Failover Trap", "dns", """
On the Continuum core platform, failing over to the secondary DNS resolver does NOT
fix real resolution failures — the secondary resolver shares the same upstream zone
file replication bug as the primary. The correct fix for DNS resolution failures on
Continuum core sites is to flush the local zone cache directly on the affected site
controller, not to fail over.
"""),
    ("RB037", "Titan Baseband Packet Loss Anti-Pattern", "packet_loss", """
On Titan-series baseband units, packet loss under 5% is caused by an internal buffer
pre-allocation bug in the packet scheduler, not a physical-layer or transceiver issue.
Swapping the transceiver does nothing to fix this. The correct fix is a soft reboot of
the baseband unit's packet scheduler process.
"""),
    ("RB038", "Solstice VPN Renegotiation Trap", "vpn", """
On Solstice-series VPN gateways, a known NTP daemon bug causes repeated failed
tunnel renegotiations that look identical to certificate expiry. Checking or renewing
certificates wastes time and does not fix this. The correct first step on a Solstice
gateway VPN failure is to restart the NTP daemon on the gateway before touching
certificates at all.
"""),
    ("RB039", "Meridian-Link Handover Anti-Fix", "handover", """
For Meridian-link paired cells specifically, do NOT adjust neighbor-cell-relation (NCR)
thresholds during an active handover-failure event. Doing so triggers a known
oscillation bug that worsens the failure rate. The correct procedure is to freeze all
NCR configuration changes and wait 90 seconds for the automatic recovery timer before
making any adjustment.
"""),
]

for doc_id, title, category, body in RUNBOOKS:
    content = f"---\nid: {doc_id}\ntitle: {title}\ncategory: {category}\n---\n\n# {title}\n{body.strip()}\n"
    (OUT / f"{doc_id}_{category}.md").write_text(content)

print(f"Wrote {len(RUNBOOKS)} counterfactual runbooks to {OUT}")
