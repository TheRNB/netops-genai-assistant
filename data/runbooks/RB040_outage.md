---
id: RB040
title: Full Site Outage Recovery Playbook
category: outage
---

# Full Site Outage Recovery Playbook
Scope: this playbook covers full-site outages where a site is unreachable on both the
user and management planes, and is the authoritative procedure for restoring service
end to end. It supersedes any single-symptom runbook when the outage is total rather
than partial.

Phase 1 — Immediate triage (first 5 minutes): Confirm the outage is total by attempting
management-plane access via at least two independent paths (primary OOB, secondary
cellular backup). If either path responds, this is not a total outage — fall back to
the specific link-down or hardware-fault runbook instead. If both paths are unreachable,
declare a sev-1 and page the on-call site-reliability engineer immediately, not just the
NOC queue.

Phase 2 — Root-cause classification (5 to 20 minutes): Check, in this order: (a) utility
power status for the site, including battery/generator telemetry if any telemetry is
still reaching the NMS; (b) the last five alarms received before the outage, which often
indicate thermal, power, or hardware-fault codes; (c) whether a scheduled maintenance
window was active at the time, which can indicate human error rather than a fault. Do
not skip ahead to dispatch before completing this classification pass, since dispatch
without a root-cause hypothesis wastes a truck roll.

Phase 3 — Recovery actions: If power is the root cause and the site has no working
telemetry, dispatch a field technician with a portable generator regardless of ETA on
utility restoration — do not wait to see if utility power returns on its own. If the
root cause is a crashed baseband unit with power otherwise healthy, attempt a remote
power-cycle via the site's independent power controller (if present) before dispatching;
many sites have a controller that survives a baseband crash. If neither power nor a
simple power-cycle resolves it, this becomes a hardware dispatch — treat the ETA to
restoration as the technician's travel time plus a fixed 45-minute on-site diagnostic
allowance, and communicate that ETA to stakeholders rather than a vaguer estimate.

Phase 4 — Rollback criteria: If a scheduled change was active when the outage began,
the default action is rollback, not forward-fix, unless the change owner can produce a
specific forward-fix plan within 15 minutes of the outage being declared. This 15-minute
window exists specifically to prevent an outage from being extended by an open-ended
attempt to patch forward when a known-good rollback exists.

Post-incident: every full-site outage requires a post-incident review within 2 business
days, regardless of how quickly it was resolved, because total outages have historically
been the leading indicator of a systemic issue even when the immediate fix was routine.
