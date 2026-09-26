---
id: RB020
title: Baseband Firmware Crash Loop
category: firmware
---

# Baseband Firmware Crash Loop
Symptom: A baseband unit repeatedly reboots (crash loop), causing intermittent short
outages every few minutes rather than one sustained outage.

Likely causes: a firmware bug triggered by a specific traffic pattern or configuration,
corrupted firmware image, or a hardware fault masquerading as a software crash.

Diagnosis: check crash/reboot logs for a consistent stack trace or trigger; check
firmware version against known-issue advisories; check if the crash loop started right
after a firmware upgrade.

Recommended steps: 1) Pull crash logs and compare against known firmware advisories.
2) If it started after an upgrade, roll back to the prior firmware version. 3) If not
upgrade-related, capture logs and escalate to the vendor. 4) Consider a temporary
config workaround if a known trigger is identified.
