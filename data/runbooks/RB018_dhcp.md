---
id: RB018
title: DHCP Pool Exhaustion
category: dhcp
---

# DHCP Pool Exhaustion
Symptom: New devices at a site fail to obtain an IP address while already-connected
devices are unaffected; DHCP server logs show pool exhaustion or NAK responses.

Likely causes: lease pool sized too small for current device density, leases not being
reclaimed (short-lived devices holding long leases), or a rogue/duplicate DHCP server.

Diagnosis: check current pool utilization and lease duration; check for an unexpected
second DHCP server on the segment; check device churn rate at the site.

Recommended steps: 1) Check pool utilization; if near 100%, this confirms exhaustion.
2) Check for a rogue DHCP server on the VLAN. 3) If legitimate exhaustion, expand the
pool or shorten lease time. 4) Monitor pool utilization after the change.
