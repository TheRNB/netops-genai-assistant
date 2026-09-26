---
id: RB007
title: Excessive Jitter on Voice Traffic
category: jitter
---

# Excessive Jitter on Voice Traffic
Symptom: Voice call quality complaints (choppy audio) correlate with jitter measurements
above 30ms on the RTP path, even though loss and average latency look acceptable.

Likely causes: insufficient QoS prioritization for RTP traffic, queuing delay variance
on a congested link, or a routing path change mid-call.

Diagnosis: check QoS classification for RTP/voice traffic; check for competing bulk
traffic on the same queue; check for asymmetric or changing routing paths.

Recommended steps: 1) Verify voice traffic is in a priority queue end to end. 2) Check
for bulk-traffic contention on the same link and consider traffic shaping. 3) Check
routing stability on the voice path. 4) Re-test after any QoS change with a synthetic
call.
