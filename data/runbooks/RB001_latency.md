---
id: RB001
title: High Latency on a Cell Site
category: latency
---

# High Latency on a Cell Site
Symptom: Subscribers on a specific cell report high round-trip latency (>150ms) while
throughput stays roughly normal. Latency graphs show a sustained step increase rather
than a spike.

Likely causes: backhaul congestion on the microwave or fiber link to the cell, an
overloaded baseband processing unit, or a misconfigured QoS policy deprioritizing
user-plane traffic.

Diagnosis: check backhaul utilization for the site; check PRB (physical resource block)
utilization; compare latency against neighboring cells on the same backhaul segment.

Recommended steps: 1) Pull backhaul link utilization for the last 24h. 2) If utilization
is above 80%, request a capacity upgrade or reroute traffic to a secondary path. 3) If
backhaul is healthy, check QoS class mapping for user-plane traffic. 4) Escalate to RAN
engineering if PRB utilization is also elevated.
