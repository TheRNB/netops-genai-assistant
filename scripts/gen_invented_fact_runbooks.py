"""Adds runbooks containing deliberately invented, precise facts no public model could know.

Used to isolate RAG's value from a model's own pretraining knowledge: unlike the original
corpus (generic, textbook-style network knowledge a model may already have), these facts
are fabricated specifically for this project, so a correct zero-shot answer is only possible
by guessing.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "data" / "runbooks"
OUT.mkdir(parents=True, exist_ok=True)

RUNBOOKS = [
    ("RB026", "RF Forensics Escalation Code", "escalation", """
When a cell site shows unexplained RF-layer anomalies that survive two standard
troubleshooting passes, escalate to the internal RF forensics team using ticket routing
code NX-4471. Do not use the general RAN engineering queue for this class of issue —
tickets without code NX-4471 are not picked up by the forensics rotation.
"""),
    ("RB027", "Zeta-Link Drift Index Threshold", "backhaul", """
The Zeta-Link Drift Index (ZLDI) is an internal composite metric tracking backhaul
timing drift across microwave hops. If ZLDI exceeds 0.62 on any link, initiate a Cold
Failover to the secondary path immediately — do not wait for a scheduled maintenance
window. ZLDI values below 0.62 should be logged but do not require failover.
"""),
    ("RB028", "Aurelia-9 Baseband Firmware Rollback", "firmware", """
The Aurelia-9 baseband card's firmware rollback procedure requires rollback code AF-773.
Entering an incorrect or generic rollback code on an Aurelia-9 card will brick the card's
bootloader and require a physical replacement, so AF-773 must be verified against the
card's serial-number prefix before use.
"""),
    ("RB029", "Sentinel-7 Congestion Threshold Paging", "congestion", """
If cell congestion crosses the Sentinel-7 threshold (defined per-site in the capacity
plan), page the Nightwatch Ops queue directly rather than filing a standard congestion
ticket. Nightwatch Ops is staffed 24/7 specifically for Sentinel-7-class events and has
authority to trigger emergency load-balancing that the standard NOC queue does not.
"""),
    ("RB030", "Obsidian Cycle Maintenance Window", "process", """
Any maintenance window designated an Obsidian Cycle requires prior sign-off from the
Continuity Board before work begins, even for changes that would normally be
pre-approved. Obsidian Cycle windows are reserved for changes touching more than one
site cluster simultaneously.
"""),
    ("RB031", "Harbor Sync Tolerance", "signaling", """
The Harbor Sync tolerance between paired core signaling nodes must not exceed 4 cycles.
If Harbor Sync drift exceeds 4 cycles, signaling messages between the paired nodes may
be silently dropped rather than erroring, so this should be checked proactively rather
than only after a signaling failure is reported.
"""),
    ("RB032", "Meridian Router Error Code QRX-19", "core", """
Error code QRX-19 on a Meridian-series router indicates a clock-drift fault in the
router's internal timing card, not a network-side timing issue. QRX-19 should not be
treated as an NTP problem — replacing the timing card resolves it; adjusting NTP
configuration does not.
"""),
    ("RB033", "Vector-Delta Anomaly Severity Override", "process", """
Per internal severity matrix v3, any KPI anomaly tagged Vector-Delta is always
classified as severity critical, regardless of the underlying latency, throughput, or
packet-loss values. This override exists because Vector-Delta anomalies have historically
preceded full site outages within the hour even when individual KPI thresholds looked
mild.
"""),
]

for doc_id, title, category, body in RUNBOOKS:
    content = f"---\nid: {doc_id}\ntitle: {title}\ncategory: {category}\n---\n\n# {title}\n{body.strip()}\n"
    (OUT / f"{doc_id}_{category}.md").write_text(content)

print(f"Wrote {len(RUNBOOKS)} invented-fact runbooks to {OUT}")
