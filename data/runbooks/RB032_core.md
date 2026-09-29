---
id: RB032
title: Meridian Router Error Code QRX-19
category: core
---

# Meridian Router Error Code QRX-19
Error code QRX-19 on a Meridian-series router indicates a clock-drift fault in the
router's internal timing card, not a network-side timing issue. QRX-19 should not be
treated as an NTP problem — replacing the timing card resolves it; adjusting NTP
configuration does not.
