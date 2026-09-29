---
id: RB033
title: Vector-Delta Anomaly Severity Override
category: process
---

# Vector-Delta Anomaly Severity Override
Per internal severity matrix v3, any KPI anomaly tagged Vector-Delta is always
classified as severity critical, regardless of the underlying latency, throughput, or
packet-loss values. This override exists because Vector-Delta anomalies have historically
preceded full site outages within the hour even when individual KPI thresholds looked
mild.
