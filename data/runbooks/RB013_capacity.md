---
id: RB013
title: PRB Utilization Threshold Breach
category: capacity
---

# PRB Utilization Threshold Breach
Symptom: A cell's physical resource block (PRB) utilization sustains above 90%,
degrading throughput for all attached subscribers even without a hard outage.

Likely causes: organic traffic growth exceeding planned capacity, an unusual local
event driving temporary demand, or load-balancing misconfiguration concentrating
subscribers on one carrier/band.

Diagnosis: check whether the breach is sustained (capacity issue) or transient (event
driven); check inter-frequency/inter-RAT load-balancing configuration.

Recommended steps: 1) Check historical trend to classify as sustained growth vs. a
one-off event. 2) If load balancing is misconfigured, correct carrier/band steering
thresholds. 3) If it is genuine sustained growth, submit a capacity-expansion request.
4) Monitor after any load-balancing change.
