---
id: RB036
title: Continuum Core DNS Failover Trap
category: dns
---

# Continuum Core DNS Failover Trap
On the Continuum core platform, failing over to the secondary DNS resolver does NOT
fix real resolution failures — the secondary resolver shares the same upstream zone
file replication bug as the primary. The correct fix for DNS resolution failures on
Continuum core sites is to flush the local zone cache directly on the affected site
controller, not to fail over.
