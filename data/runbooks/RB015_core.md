---
id: RB015
title: S1 Interface Failure
category: core
---

# S1 Interface Failure
Symptom: An eNodeB loses its S1 connection to the core (MME), causing all attached
subscribers on that eNodeB to lose service simultaneously, similar to an outage but
with the radio hardware still alarming as healthy.

Likely causes: transport failure between eNodeB and MME, MME-side overload rejecting
new S1 setups, or a security/certificate mismatch (if S1 is IPsec-protected).

Diagnosis: check transport-layer reachability to the MME; check MME load/alarms;
check IPsec/certificate status if applicable.

Recommended steps: 1) Check transport reachability first (ping/traceroute at the IP
layer). 2) If reachable, check MME-side alarms/load. 3) If IPsec is in use, check
certificate validity and tunnel status. 4) Escalate to core-network team if MME-side.
