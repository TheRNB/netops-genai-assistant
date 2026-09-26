---
id: RB006
title: BGP Session Flapping
category: bgp
---

# BGP Session Flapping
Symptom: A BGP peering session between the edge router and a peer/upstream repeatedly
goes down and comes back up (flapping), causing intermittent routing instability.

Likely causes: unstable physical link, MTU mismatch on the peering interface, keepalive
timer misconfiguration, or CPU exhaustion on the router control plane.

Diagnosis: check interface error counters on the peering link; check BGP hold-timer and
keepalive settings; check router CPU utilization during flap events.

Recommended steps: 1) Check the physical link for errors. 2) Verify MTU matches on both
ends. 3) If CPU is spiking, check for a control-plane DoS or excessive route churn.
4) If the link is clean, review timer settings and route-dampening configuration.
