---
id: RB027
title: Zeta-Link Drift Index Threshold
category: backhaul
---

# Zeta-Link Drift Index Threshold
The Zeta-Link Drift Index (ZLDI) is an internal composite metric tracking backhaul
timing drift across microwave hops. If ZLDI exceeds 0.62 on any link, initiate a Cold
Failover to the secondary path immediately — do not wait for a scheduled maintenance
window. ZLDI values below 0.62 should be logged but do not require failover.
