"""One-off generator for synthetic runbook docs (not part of the app runtime)."""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "data" / "runbooks"
OUT.mkdir(parents=True, exist_ok=True)

RUNBOOKS = [
    ("RB001", "High Latency on a Cell Site", "latency", """
Symptom: Subscribers on a specific cell report high round-trip latency (>150ms) while
throughput stays roughly normal. Latency graphs show a sustained step increase rather
than a spike.

Likely causes: backhaul congestion on the microwave or fiber link to the cell, an
overloaded baseband processing unit, or a misconfigured QoS policy deprioritizing
user-plane traffic.

Diagnosis: check backhaul utilization for the site; check PRB (physical resource block)
utilization; compare latency against neighboring cells on the same backhaul segment.

Recommended steps: 1) Pull backhaul link utilization for the last 24h. 2) If utilization
is above 80%, request a capacity upgrade or reroute traffic to a secondary path. 3) If
backhaul is healthy, check QoS class mapping for user-plane traffic. 4) Escalate to RAN
engineering if PRB utilization is also elevated.
"""),
    ("RB002", "Packet Loss on Access Link", "packet_loss", """
Symptom: Packet loss percentage above 1% sustained for more than 10 minutes on an
access-link interface, often correlated with throughput drops and retransmissions.

Likely causes: physical layer errors (cable/connector degradation), interface buffer
overflow during traffic bursts, or a faulty SFP/transceiver.

Diagnosis: check interface error counters (CRC errors, input/output drops); check
whether loss correlates with peak-hour traffic bursts; check optical power levels on
the transceiver.

Recommended steps: 1) Check interface error counters via the NMS. 2) If CRC errors are
high, schedule a physical inspection or transceiver swap. 3) If loss only occurs during
bursts, increase buffer allocation or apply traffic shaping. 4) If unresolved, open a
hardware ticket.
"""),
    ("RB003", "Cell Link Down", "link_down", """
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
"""),
    ("RB004", "Network Congestion During Peak Hours", "congestion", """
Symptom: Throughput per subscriber drops and latency rises specifically during known
peak hours (e.g., evening), then recovers off-peak.

Likely causes: cell or backhaul capacity insufficient for peak demand; a temporary
event driving unusual load (large gathering, outage on a neighboring cell shifting
load).

Diagnosis: compare PRB utilization and backhaul utilization during the peak window
against capacity thresholds; check if a neighboring cell is down and shifting load.

Recommended steps: 1) Check neighboring cell status for shifted load. 2) If utilization
is structurally above threshold, flag for a capacity-planning request. 3) Consider
temporary load balancing across carriers/bands if supported. 4) Monitor after any
mitigation to confirm recovery.
"""),
    ("RB005", "DNS Resolution Failures", "dns", """
Symptom: Subscribers report "no internet" while the radio and backhaul links show
healthy; DNS query failure rate is elevated in logs.

Likely causes: DNS resolver overload, a misconfigured DNS forwarder, or an upstream
DNS provider outage.

Diagnosis: check DNS query success rate and response latency; check resolver CPU/memory;
test resolution against a secondary/public resolver from the same segment.

Recommended steps: 1) Check resolver health (CPU, memory, query queue). 2) If the
resolver is healthy but upstream fails, fail over to a secondary DNS provider.
3) If the resolver itself is overloaded, scale it or add a cache layer. 4) Notify NOC
of user-facing impact regardless of root cause found.
"""),
    ("RB006", "BGP Session Flapping", "bgp", """
Symptom: A BGP peering session between the edge router and a peer/upstream repeatedly
goes down and comes back up (flapping), causing intermittent routing instability.

Likely causes: unstable physical link, MTU mismatch on the peering interface, keepalive
timer misconfiguration, or CPU exhaustion on the router control plane.

Diagnosis: check interface error counters on the peering link; check BGP hold-timer and
keepalive settings; check router CPU utilization during flap events.

Recommended steps: 1) Check the physical link for errors. 2) Verify MTU matches on both
ends. 3) If CPU is spiking, check for a control-plane DoS or excessive route churn.
4) If the link is clean, review timer settings and route-dampening configuration.
"""),
    ("RB007", "Excessive Jitter on Voice Traffic", "jitter", """
Symptom: Voice call quality complaints (choppy audio) correlate with jitter measurements
above 30ms on the RTP path, even though loss and average latency look acceptable.

Likely causes: insufficient QoS prioritization for RTP traffic, queuing delay variance
on a congested link, or a routing path change mid-call.

Diagnosis: check QoS classification for RTP/voice traffic; check for competing bulk
traffic on the same queue; check for asymmetric or changing routing paths.

Recommended steps: 1) Verify voice traffic is in a priority queue end to end. 2) Check
for bulk-traffic contention on the same link and consider traffic shaping. 3) Check
routing stability on the voice path. 4) Re-test after any QoS change with a synthetic
call.
"""),
    ("RB008", "VoLTE Call Drops", "volte", """
Symptom: Elevated VoLTE call-drop rate on a cell or cluster, disproportionate to data
session drop rate.

Likely causes: IMS signaling path issues (SIP/Diameter), handover failures specific to
the voice bearer, or radio-side QoS for the voice bearer not being honored.

Diagnosis: check IMS core signaling success rate; check handover success rate for
voice-bearer sessions specifically; check whether drops cluster at cell edges (handover
related) or are uniform (core/signaling related).

Recommended steps: 1) Check IMS/SIP signaling logs for failure codes during the drop
window. 2) If drops cluster at cell edges, investigate handover parameters. 3) If
uniform, escalate to the IMS core team. 4) Correlate with any recent config change on
affected cells.
"""),
    ("RB009", "Handover Failure Between Cells", "handover", """
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
"""),
    ("RB010", "Unplanned Cell Outage", "outage", """
Symptom: A cell disappears from the network topology entirely (no alarms cleared, no
traffic), distinct from a link-down state where the site is still reachable for
management.

Likely causes: total power loss including backup, a crashed baseband unit that also
lost management connectivity, or a catastrophic hardware failure.

Diagnosis: attempt management-plane connectivity to the site controller; check the
last alarms received before the outage; check power/battery telemetry if available.

Recommended steps: 1) Attempt remote management access; if unreachable, this is a
sev-1 outage. 2) Check the last received alarms for a root-cause hint (thermal, power,
hardware fault code). 3) Dispatch a field technician immediately for total outages.
4) Open a post-incident review once service is restored.
"""),
    ("RB011", "Backhaul Fiber Cut", "backhaul", """
Symptom: Multiple co-located cells or an entire ring segment lose backhaul
simultaneously; radio hardware itself is powered and alarming "link down," not
"hardware fault."

Likely causes: a physical fiber cut (construction, weather, rodent damage) or a fiber
patch-panel/connector failure at an aggregation point.

Diagnosis: check optical power levels on both ends of the affected span; check whether
a ring/protection path took over; correlate with any nearby construction or maintenance
reports.

Recommended steps: 1) Check optical power/loss on the span; a large loss jump confirms
a physical break. 2) Confirm whether protection switching engaged; if not, escalate as
a protection-mechanism defect. 3) Dispatch a fiber crew to locate and splice the break.
4) Track restoration against the affected site list.
"""),
    ("RB012", "Antenna Misalignment", "rf", """
Symptom: A cell shows persistently weak RSRP/RSRQ for subscribers who should be well
within coverage, despite the site itself being healthy and powered.

Likely causes: physical antenna misalignment (tilt/azimuth drift) after
maintenance/weather, or a damaged antenna/feeder.

Diagnosis: compare current RF coverage pattern against the design baseline; check for
recent maintenance events at the site; check feeder VSWR (voltage standing wave ratio)
if available.

Recommended steps: 1) Compare live coverage pattern to the planned pattern. 2) Check
VSWR for feeder/antenna faults. 3) If VSWR is normal but coverage is off, dispatch a
technician to re-align tilt/azimuth. 4) Verify coverage recovers after adjustment.
"""),
    ("RB013", "PRB Utilization Threshold Breach", "capacity", """
Symptom: A cell's physical resource block (PRB) utilization sustains above 90%,
degrading throughput for all attached subscribers even without a hard outage.

Likely causes: organic traffic growth exceeding planned capacity, an unusual local
event driving temporary demand, or load-balancing misconfiguration concentrating
subscribers on one carrier/band.

Diagnosis: check whether the breach is sustained (capacity issue) or transient (event
driven); check inter-frequency/inter-RAT load-balancing configuration.

Recommended steps: 1) Check historical trend to classify as sustained growth vs. a
one-off event. 2) If load balancing is misconfigured, correct carrier/band steering
thresholds. 3) If it is genuine sustained growth, submit a capacity-expansion request.
4) Monitor after any load-balancing change.
"""),
    ("RB014", "RRC Connection Setup Failures", "signaling", """
Symptom: Elevated RRC (Radio Resource Control) connection setup failure rate, meaning
subscribers fail to establish a radio connection before any data session begins.

Likely causes: radio-side congestion (no resources to grant), interference raising the
failure rate, or a baseband software fault.

Diagnosis: check whether failures correlate with PRB congestion; check uplink
interference levels; check for a recent software/firmware change on the baseband.

Recommended steps: 1) Check PRB utilization at failure times. 2) Check uplink
interference (noise floor) trend. 3) If a recent software change coincides with the
onset, consider rollback. 4) Escalate to RAN engineering if none of the above explain
it.
"""),
    ("RB015", "S1 Interface Failure", "core", """
Symptom: An eNodeB loses its S1 connection to the core (MME), causing all attached
subscribers on that eNodeB to lose service simultaneously, similar to an outage but
with the radio hardware still alarming as healthy.

Likely causes: transport failure between eNodeB and MME, MME-side overload rejecting
new S1 setups, or a security/certificate mismatch (if S1 is IPsec-protected).

Diagnosis: check transport-layer reachability to the MME; check MME load/alarms;
check IPsec/certificate status if applicable.

Recommended steps: 1) Check transport reachability first (ping/traceroute at the IP
layer). 2) If reachable, check MME-side alarms/load. 3) If IPsec is in use, check
certificate validity and tunnel status. 4) Escalate to core-network team if MME-side.
"""),
    ("RB016", "Throughput Degradation Without Congestion", "throughput", """
Symptom: Subscriber throughput drops well below expected values even though PRB
utilization, backhaul utilization, and error counters all look normal.

Likely causes: a MIMO/carrier-aggregation feature silently disabled, a scheduler
misconfiguration, or a device-side issue affecting a subset of subscribers rather than
the cell.

Diagnosis: check whether the degradation affects all subscribers or a device-type
subset; check MIMO/CA feature status on the cell; check scheduler configuration against
baseline.

Recommended steps: 1) Segment the complaint by device type/vendor. 2) If cell-wide,
check MIMO/CA feature flags against the intended configuration. 3) If device-specific,
this is likely not a network fault — document and close. 4) Escalate to RAN engineering
if a feature flag is confirmed misconfigured.
"""),
    ("RB017", "Site-to-Site VPN Tunnel Down", "vpn", """
Symptom: A site-to-site VPN tunnel used for management or backhaul traffic between two
network segments is down, isolating traffic that depends on it.

Likely causes: IKE/IPsec phase negotiation failure due to a certificate or pre-shared
key mismatch, a public-IP change on one endpoint, or an MTU/fragmentation issue.

Diagnosis: check IKE phase 1/phase 2 negotiation logs; check for recent IP address
changes on either endpoint; check for fragmentation-related drops.

Recommended steps: 1) Check IKE negotiation logs for the specific failure reason.
2) If a certificate/key expired, rotate and re-establish. 3) If an endpoint IP changed,
update the peer configuration. 4) If negotiation succeeds but traffic still fails,
check MTU/fragmentation settings.
"""),
    ("RB018", "DHCP Pool Exhaustion", "dhcp", """
Symptom: New devices at a site fail to obtain an IP address while already-connected
devices are unaffected; DHCP server logs show pool exhaustion or NAK responses.

Likely causes: lease pool sized too small for current device density, leases not being
reclaimed (short-lived devices holding long leases), or a rogue/duplicate DHCP server.

Diagnosis: check current pool utilization and lease duration; check for an unexpected
second DHCP server on the segment; check device churn rate at the site.

Recommended steps: 1) Check pool utilization; if near 100%, this confirms exhaustion.
2) Check for a rogue DHCP server on the VLAN. 3) If legitimate exhaustion, expand the
pool or shorten lease time. 4) Monitor pool utilization after the change.
"""),
    ("RB019", "NTP Synchronization Failure", "ntp", """
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
"""),
    ("RB020", "Baseband Firmware Crash Loop", "firmware", """
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
"""),
    ("RB021", "Site Thermal Shutdown", "power", """
Symptom: A site shuts down or throttles during high-temperature periods, then recovers
once ambient temperature drops.

Likely causes: HVAC/cooling failure at the site, blocked ventilation, or a fan failure
inside the equipment cabinet.

Diagnosis: check site temperature telemetry against the shutdown threshold; check HVAC
status/alarms; check for physical obstruction reports.

Recommended steps: 1) Check temperature telemetry and HVAC alarm history. 2) If HVAC
failed, dispatch facilities/field technician urgently. 3) If HVAC is fine but airflow
is blocked, clear obstructions. 4) Consider temporary load-shedding if temperature is
still climbing.
"""),
    ("RB022", "Power Supply Failure with Battery Failover", "power", """
Symptom: A site briefly drops and recovers, with alarms indicating mains power loss
followed by battery-backup engagement, then mains restoration.

Likely causes: a genuine utility power outage, a faulty rectifier/power supply unit at
the site, or a tripped breaker.

Diagnosis: check utility outage reports for the area; check rectifier/PSU alarm history;
check battery state-of-health and how much runtime it provided.

Recommended steps: 1) Check for a known utility outage in the area first. 2) If no
utility outage, check rectifier/PSU alarms for a hardware fault. 3) Check battery
health — if runtime was short, batteries may need replacement. 4) Schedule PSU/battery
service if a recurring pattern is seen.
"""),
    ("RB023", "Microwave Backhaul Link Fade", "backhaul", """
Symptom: A microwave backhaul link's error rate and latency worsen during specific
weather conditions (rain, fog) and recover once weather clears.

Likely causes: rain fade or fog attenuation exceeding the link's fade margin, or
antenna misalignment reducing the effective fade margin below design.

Diagnosis: check received signal level (RSL) trend against weather data; check the
link's designed fade margin versus current conditions; check for recent alignment
drift.

Recommended steps: 1) Correlate RSL drops with weather data to confirm fade. 2) If fade
margin is marginal even in good weather, escalate for a capacity/hardware upgrade
(bigger dish, different frequency). 3) If the link fades worse than its design margin
suggests, check for alignment drift. 4) Track link availability against SLA.
"""),
    ("RB024", "Load Balancer Backend Failure", "core", """
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
"""),
    ("RB025", "IPsec Tunnel Negotiation Failure After Cert Expiry", "security", """
Symptom: A previously stable IPsec tunnel (e.g., for S1 or backhaul security) suddenly
fails to establish, with no configuration changes reported.

Likely causes: an X.509 certificate used for IKE authentication has expired, clock
drift on one endpoint pushing it outside the certificate's valid window, or a revoked
certificate.

Diagnosis: check certificate expiry dates on both endpoints; check for NTP/clock drift
(see the NTP runbook); check certificate revocation status if a CRL/OCSP is in use.

Recommended steps: 1) Check certificate expiry on both tunnel endpoints first — this is
the most common cause. 2) If not expired, check clock sync on both ends. 3) Renew and
redeploy the certificate if expired. 4) Re-test tunnel establishment and confirm it
stays up.
"""),
]

for doc_id, title, category, body in RUNBOOKS:
    content = f"---\nid: {doc_id}\ntitle: {title}\ncategory: {category}\n---\n\n# {title}\n{body.strip()}\n"
    (OUT / f"{doc_id}_{category}.md").write_text(content)

print(f"Wrote {len(RUNBOOKS)} runbooks to {OUT}")
