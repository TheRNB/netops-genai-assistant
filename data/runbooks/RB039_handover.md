---
id: RB039
title: Meridian-Link Handover Anti-Fix
category: handover
---

# Meridian-Link Handover Anti-Fix
For Meridian-link paired cells specifically, do NOT adjust neighbor-cell-relation (NCR)
thresholds during an active handover-failure event. Doing so triggers a known
oscillation bug that worsens the failure rate. The correct procedure is to freeze all
NCR configuration changes and wait 90 seconds for the automatic recovery timer before
making any adjustment.
