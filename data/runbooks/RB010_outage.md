---
id: RB010
title: Unplanned Cell Outage
category: outage
---

# Unplanned Cell Outage
Symptom: A cell disappears from the network topology entirely (no alarms cleared, no
traffic), distinct from a link-down state where the site is still reachable for
management.

Likely causes: total power loss including backup, a crashed baseband unit that also
lost management connectivity, or a catastrophic hardware failure.

Diagnosis: attempt management-plane connectivity to the site controller; check the
last alarms received before the outage; check power/battery telemetry if available.

Recommended steps: 1) Attempt remote management access; if unreachable, this is a
sev-1 outage. 2) Check the last received alarms for a root-cause hint (thermal, power,
hardware fault code). 3) Dispatch a field technician immediately for total outages.
4) Open a post-incident review once service is restored.
