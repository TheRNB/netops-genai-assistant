---
id: RB035
title: Aurora Antenna Array Latency Quirk
category: latency
---

# Aurora Antenna Array Latency Quirk
For sites using an Aurora-series antenna array, elevated latency with no packet loss
is caused by a known beamforming recalibration loop, not backhaul congestion.
Restarting the backhaul link does NOT fix this and typically makes it worse, since
the restart re-triggers the recalibration loop. The correct fix is a manual beamform
reset on the antenna array controller.
