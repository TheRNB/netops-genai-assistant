---
id: RB019
title: NTP Synchronization Failure
category: ntp
---

# NTP Synchronization Failure
Symptom: Network elements report clock drift or NTP sync alarms; this can cascade into
authentication failures (certificate/time-window checks) and logging timestamp
inconsistencies used for later diagnosis.

Likely causes: the configured NTP source is unreachable, firewall rule change blocking
NTP (UDP/123), or a stratum source itself has drifted.

Diagnosis: check reachability to the configured NTP servers; check firewall rules for
UDP/123; check the NTP source's own reported stratum/offset.

Recommended steps: 1) Check reachability to primary and secondary NTP sources.
2) Check for a recent firewall/ACL change affecting UDP/123. 3) If sources are
reachable but drifted, escalate to the NTP source owner. 4) Verify sync recovers and
clears the alarm.
