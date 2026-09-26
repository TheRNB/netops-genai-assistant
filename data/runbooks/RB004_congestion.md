---
id: RB004
title: Network Congestion During Peak Hours
category: congestion
---

# Network Congestion During Peak Hours
Symptom: Throughput per subscriber drops and latency rises specifically during known
peak hours (e.g., evening), then recovers off-peak.

Likely causes: cell or backhaul capacity insufficient for peak demand; a temporary
event driving unusual load (large gathering, outage on a neighboring cell shifting
load).

Diagnosis: compare PRB utilization and backhaul utilization during the peak window
against capacity thresholds; check if a neighboring cell is down and shifting load.

Recommended steps: 1) Check neighboring cell status for shifted load. 2) If utilization
is structurally above threshold, flag for a capacity-planning request. 3) Consider
temporary load balancing across carriers/bands if supported. 4) Monitor after any
mitigation to confirm recovery.
