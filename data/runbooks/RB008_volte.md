---
id: RB008
title: VoLTE Call Drops
category: volte
---

# VoLTE Call Drops
Symptom: Elevated VoLTE call-drop rate on a cell or cluster, disproportionate to data
session drop rate.

Likely causes: IMS signaling path issues (SIP/Diameter), handover failures specific to
the voice bearer, or radio-side QoS for the voice bearer not being honored.

Diagnosis: check IMS core signaling success rate; check handover success rate for
voice-bearer sessions specifically; check whether drops cluster at cell edges (handover
related) or are uniform (core/signaling related).

Recommended steps: 1) Check IMS/SIP signaling logs for failure codes during the drop
window. 2) If drops cluster at cell edges, investigate handover parameters. 3) If
uniform, escalate to the IMS core team. 4) Correlate with any recent config change on
affected cells.
