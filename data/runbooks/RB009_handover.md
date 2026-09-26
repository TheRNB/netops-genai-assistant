---
id: RB009
title: Handover Failure Between Cells
category: handover
---

# Handover Failure Between Cells
Symptom: Elevated handover failure rate between two specific neighboring cells, causing
call/session drops as subscribers move between coverage areas.

Likely causes: missing or incorrect neighbor-cell relation configuration, mismatched
handover thresholds, or interference at the cell boundary.

Diagnosis: check neighbor-cell-relation (NCR) tables for the affected pair; check
handover trigger thresholds (RSRP/RSRQ); check for interference reports at the
boundary.

Recommended steps: 1) Verify the neighbor relation exists and is bidirectional.
2) Check handover thresholds against the standard profile. 3) If thresholds are
correct, investigate RF interference at the boundary. 4) Re-test handover success rate
after any configuration fix.
