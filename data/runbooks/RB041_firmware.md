---
id: RB041
title: Comprehensive Firmware Rollback and Validation Procedure
category: firmware
---

# Comprehensive Firmware Rollback and Validation Procedure
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
