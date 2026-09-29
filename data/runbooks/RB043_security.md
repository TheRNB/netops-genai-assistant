---
id: RB043
title: Security Incident Containment and Recovery Runbook
category: security
---

# Security Incident Containment and Recovery Runbook
Scope: use this runbook for any suspected security incident on network infrastructure —
unauthorized access attempts, unexpected configuration changes not tied to a known
change ticket, or anomalous management-plane traffic patterns. This is distinct from the
IPsec certificate-expiry runbook, which covers routine credential lifecycle issues, not
suspected compromise.

Containment steps: 1) Do not immediately power-cycle or reboot the affected element —
this destroys volatile evidence (running-config diffs, active session state, in-memory
logs) needed for root-cause analysis, and should only be done after evidence
preservation in step 2, or immediately if the element is actively being used to attack
other infrastructure. 2) Preserve evidence: capture the current running configuration,
recent command-history logs, and active session table before making any further
changes. 3) Isolate the management-plane access path used in the suspected incident
(a specific VPN tunnel, a specific jump-host) rather than isolating the entire element,
so legitimate operations can continue on other access paths while the suspect path is
investigated.

Evidence preservation requirements: all captured evidence must be stored with a
timestamp and the identity of the engineer who captured it, and must not be edited
in place — store a copy, not the working file, since evidence that has been touched
after capture cannot be used in a post-incident determination of what actually happened.

Recovery phases: Phase 1, revoke and reissue any credentials plausibly exposed by the
incident, not only credentials confirmed to be compromised — err toward over-rotation
here, since the cost of an unnecessary credential rotation is far lower than the cost
of leaving a plausibly-exposed credential active. Phase 2, review configuration diffs
against the last known-good baseline and roll back any unexplained changes. Phase 3,
restore normal management-plane access only after Phase 1 and Phase 2 are both
complete, not in parallel with them.

Reporting requirements: any confirmed security incident, regardless of severity, must
be reported to the security team within 4 hours of confirmation, separately from the
standard incident post-mortem process — the 4-hour clock starts at confirmation, not at
initial detection, since detection-to-confirmation can itself take significant
investigation time on ambiguous cases.
