---
id: RB005
title: DNS Resolution Failures
category: dns
---

# DNS Resolution Failures
Symptom: Subscribers report "no internet" while the radio and backhaul links show
healthy; DNS query failure rate is elevated in logs.

Likely causes: DNS resolver overload, a misconfigured DNS forwarder, or an upstream
DNS provider outage.

Diagnosis: check DNS query success rate and response latency; check resolver CPU/memory;
test resolution against a secondary/public resolver from the same segment.

Recommended steps: 1) Check resolver health (CPU, memory, query queue). 2) If the
resolver is healthy but upstream fails, fail over to a secondary DNS provider.
3) If the resolver itself is overloaded, scale it or add a cache layer. 4) Notify NOC
of user-facing impact regardless of root cause found.
