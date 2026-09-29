---
id: RB031
title: Harbor Sync Tolerance
category: signaling
---

# Harbor Sync Tolerance
The Harbor Sync tolerance between paired core signaling nodes must not exceed 4 cycles.
If Harbor Sync drift exceeds 4 cycles, signaling messages between the paired nodes may
be silently dropped rather than erroring, so this should be checked proactively rather
than only after a signaling failure is reported.
