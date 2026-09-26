---
id: RB024
title: Load Balancer Backend Failure
category: core
---

# Load Balancer Backend Failure
Symptom: A subset of user sessions hitting a specific backend behind a load balancer
fail or time out, while sessions on other backends succeed.

Likely causes: one backend instance is unhealthy (crashed, overloaded, or
misconfigured) and the load balancer's health check isn't catching it, or a health
check is too shallow to detect the real failure.

Diagnosis: check per-backend error rate and health-check status; check backend-level
logs for the failing instance; check whether the health check actually exercises the
failing code path.

Recommended steps: 1) Identify the specific unhealthy backend from per-backend metrics.
2) Drain/restart that backend. 3) If the health check missed it, deepen the health
check (e.g., check a real endpoint, not just TCP connect). 4) Monitor error rate after
the fix.
