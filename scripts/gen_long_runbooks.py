"""Adds a few genuinely long, multi-section runbooks that require real multi-chunk splitting.

Most runbooks in this corpus are short, single-topic notes that fit in one chunk. In a
real deployment, some procedures (full outage recovery, security incident response) run
several pages — this simulates that mix so chunking logic is actually exercised, rather
than every document conveniently fitting in a single chunk.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "data" / "runbooks"
OUT.mkdir(parents=True, exist_ok=True)

RUNBOOKS = [
    ("RB040", "Full Site Outage Recovery Playbook", "outage", """
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
"""),
    ("RB041", "Comprehensive Firmware Rollback and Validation Procedure", "firmware", """
Scope: use this procedure whenever a firmware rollback is being considered on any RAN or
core network element, not just baseband units. Rollback is a higher-risk operation than
it appears, and skipping validation steps has historically caused secondary outages.

Pre-checks before rollback: confirm the target rollback firmware version is still
supported by checking the vendor's active-support matrix, not just whether the image
file is available locally — an unsupported image can be present on disk long after
support has lapsed. Confirm there is no in-flight configuration change that assumes the
current (higher) firmware version's feature set; rolling back under an incompatible
config can leave the element in a state that neither firmware version's expected
configuration schema matches.

Rollback steps, baseband family: 1) Drain active sessions from the unit gracefully over
a 2-minute window rather than an immediate hard drain, to avoid a spike of dropped calls
counted against the site's KPIs. 2) Apply the rollback image. 3) Do not restart
automatically — perform a manual restart only after confirming the image checksum
matches the vendor's published value for that exact version. 4) Allow the unit 10
minutes post-restart before validation, since some counters take that long to
stabilize after a firmware change.

Rollback steps, core signaling family: core elements require a paired-node rollback,
not a single-node rollback, because paired signaling nodes running different firmware
versions have a known compatibility gap during the transition window. Roll back the
standby node first, validate it independently against a synthetic signaling test, and
only then fail over and roll back the former active node.

Validation matrix: after any rollback, validate in this order: (a) the element rejoins
its management-plane inventory correctly; (b) synthetic call/session tests succeed at a
baseline rate matching the pre-rollback 24-hour average; (c) no new alarm classes appear
that were not present before the rollback. A rollback is only considered complete once
all three pass — a rollback that restores service but introduces a new alarm class is
not yet complete and should not be marked closed.

Escalation: if validation fails at any stage, do not attempt a second rollback attempt
on the same element without escalating to firmware engineering first, since a failed
rollback followed immediately by another rollback attempt has, more than once, left an
element in an unrecoverable bootloader state requiring physical replacement.
"""),
    ("RB042", "Multi-Site Capacity Escalation and Load-Shed Procedure", "capacity", """
Scope: this procedure applies when capacity pressure affects more than one site
simultaneously — for example during a regional event, a multi-site outage shifting
load, or a genuine regional traffic surge. Single-site capacity issues should use the
standard PRB-utilization-threshold runbook instead; this procedure is specifically for
coordinated, multi-site responses.

Trigger conditions: this procedure is invoked when three or more sites in the same
region cross their individual capacity thresholds within the same 30-minute window.
A single site crossing threshold, even if severe, does not invoke this procedure —
only correlated, multi-site pressure does, since the response here involves
region-wide load-shedding that would be disproportionate for an isolated event.

Load-shed tiers: Tier 1 (mild, most sites under 90 percent): deprioritize
non-guaranteed background data traffic classes only; voice and guaranteed-bitrate
traffic are unaffected. Tier 2 (moderate, most sites 90 to 95 percent): additionally
cap best-effort data sessions per subscriber to a fixed rate, applied region-wide, not
just at the affected sites, to smooth the transition rather than creating a sharp
boundary at the region's edge. Tier 3 (severe, sites above 95 percent, or Tier 2 failing
to stabilize within 15 minutes): temporarily reduce new session admission for
non-priority traffic classes region-wide; this tier requires sign-off from the regional
operations manager, not just the on-call engineer, because it has visible subscriber
impact beyond the immediately affected sites.

Communication plan: at Tier 2 and above, notify the customer-communications team before
implementing the load-shed, not after, since Tier 2 and Tier 3 actions are visible to
subscribers as a service-quality change and an unexplained change generates more support
volume than a communicated one, even when the underlying capacity event was unavoidable.

Rollback: load-shedding should be rolled back tier by tier as pressure subsides, waiting
at least 10 minutes at each tier before stepping down further, to avoid oscillating
between tiers if the underlying pressure is still fluctuating near a threshold boundary.
"""),
    ("RB043", "Security Incident Containment and Recovery Runbook", "security", """
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
"""),
]

for doc_id, title, category, body in RUNBOOKS:
    content = f"---\nid: {doc_id}\ntitle: {title}\ncategory: {category}\n---\n\n# {title}\n{body.strip()}\n"
    (OUT / f"{doc_id}_{category}.md").write_text(content)

print(f"Wrote {len(RUNBOOKS)} long-form runbooks to {OUT}")
