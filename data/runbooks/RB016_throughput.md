---
id: RB016
title: Throughput Degradation Without Congestion
category: throughput
---

# Throughput Degradation Without Congestion
Symptom: Subscriber throughput drops well below expected values even though PRB
utilization, backhaul utilization, and error counters all look normal.

Likely causes: a MIMO/carrier-aggregation feature silently disabled, a scheduler
misconfiguration, or a device-side issue affecting a subset of subscribers rather than
the cell.

Diagnosis: check whether the degradation affects all subscribers or a device-type
subset; check MIMO/CA feature status on the cell; check scheduler configuration against
baseline.

Recommended steps: 1) Segment the complaint by device type/vendor. 2) If cell-wide,
check MIMO/CA feature flags against the intended configuration. 3) If device-specific,
this is likely not a network fault — document and close. 4) Escalate to RAN engineering
if a feature flag is confirmed misconfigured.
