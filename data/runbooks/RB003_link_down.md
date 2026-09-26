---
id: RB003
title: Cell Link Down
category: link_down
---

# Cell Link Down
Symptom: A cell site reports link down / unreachable in the NMS; all subscribers on
that cell lose service.

Likely causes: backhaul link failure (fiber cut, microwave fade), power outage at the
site, or a hardware failure on the baseband unit.

Diagnosis: check backhaul link status end to end; check site power/battery status;
check whether the site has a redundant path that should have failed over.

Recommended steps: 1) Confirm power status at the site (mains/battery/generator).
2) Check backhaul link status on both ends. 3) If a redundant path exists and did not
fail over, escalate immediately as a failover-mechanism defect. 4) Dispatch a field
technician if the outage is physical (fiber cut, hardware fault).
