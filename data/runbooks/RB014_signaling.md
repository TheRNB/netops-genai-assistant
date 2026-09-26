---
id: RB014
title: RRC Connection Setup Failures
category: signaling
---

# RRC Connection Setup Failures
Symptom: Elevated RRC (Radio Resource Control) connection setup failure rate, meaning
subscribers fail to establish a radio connection before any data session begins.

Likely causes: radio-side congestion (no resources to grant), interference raising the
failure rate, or a baseband software fault.

Diagnosis: check whether failures correlate with PRB congestion; check uplink
interference levels; check for a recent software/firmware change on the baseband.

Recommended steps: 1) Check PRB utilization at failure times. 2) Check uplink
interference (noise floor) trend. 3) If a recent software change coincides with the
onset, consider rollback. 4) Escalate to RAN engineering if none of the above explain
it.
