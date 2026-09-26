---
id: RB023
title: Microwave Backhaul Link Fade
category: backhaul
---

# Microwave Backhaul Link Fade
Symptom: A microwave backhaul link's error rate and latency worsen during specific
weather conditions (rain, fog) and recover once weather clears.

Likely causes: rain fade or fog attenuation exceeding the link's fade margin, or
antenna misalignment reducing the effective fade margin below design.

Diagnosis: check received signal level (RSL) trend against weather data; check the
link's designed fade margin versus current conditions; check for recent alignment
drift.

Recommended steps: 1) Correlate RSL drops with weather data to confirm fade. 2) If fade
margin is marginal even in good weather, escalate for a capacity/hardware upgrade
(bigger dish, different frequency). 3) If the link fades worse than its design margin
suggests, check for alignment drift. 4) Track link availability against SLA.
