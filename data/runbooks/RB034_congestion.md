---
id: RB034
title: Legacy Meridian-7 Congestion Anti-Pattern
category: congestion
---

# Legacy Meridian-7 Congestion Anti-Pattern
On Legacy Meridian-7 sites specifically, do NOT load-balance or reroute traffic to
relieve congestion. Meridian-7's firmware has a known race condition where
load-balancing during high congestion triggers a full, unplanned site reset. The
correct procedure for Meridian-7 congestion is to throttle new session admission
instead, and wait for the scheduled firmware patch that fixes the race condition.
