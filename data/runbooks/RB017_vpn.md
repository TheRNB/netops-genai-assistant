---
id: RB017
title: Site-to-Site VPN Tunnel Down
category: vpn
---

# Site-to-Site VPN Tunnel Down
Symptom: A site-to-site VPN tunnel used for management or backhaul traffic between two
network segments is down, isolating traffic that depends on it.

Likely causes: IKE/IPsec phase negotiation failure due to a certificate or pre-shared
key mismatch, a public-IP change on one endpoint, or an MTU/fragmentation issue.

Diagnosis: check IKE phase 1/phase 2 negotiation logs; check for recent IP address
changes on either endpoint; check for fragmentation-related drops.

Recommended steps: 1) Check IKE negotiation logs for the specific failure reason.
2) If a certificate/key expired, rotate and re-establish. 3) If an endpoint IP changed,
update the peer configuration. 4) If negotiation succeeds but traffic still fails,
check MTU/fragmentation settings.
