"""Generates eval/qa_set.json (RAG eval) and eval/incidents.json (triage eval)."""
import json
from pathlib import Path

EVAL_DIR = Path(__file__).resolve().parent.parent / "eval"
EVAL_DIR.mkdir(exist_ok=True)

QA_SET = [
    {"question": "What should I check first for high latency on a cell site?", "reference_answer": "Check backhaul link utilization for the site over the last 24 hours.", "gold_doc_id": "RB001_latency"},
    {"question": "What causes high latency on a cell while throughput stays normal?", "reference_answer": "Backhaul congestion, an overloaded baseband unit, or a QoS policy deprioritizing user-plane traffic.", "gold_doc_id": "RB001_latency"},
    {"question": "What does sustained packet loss above 1% on an access link usually indicate?", "reference_answer": "Physical layer errors, interface buffer overflow during bursts, or a faulty transceiver.", "gold_doc_id": "RB002_packet_loss"},
    {"question": "How do I diagnose packet loss on an access interface?", "reference_answer": "Check interface error counters like CRC errors and optical power levels on the transceiver.", "gold_doc_id": "RB002_packet_loss"},
    {"question": "A cell site shows link down in the NMS, what's the first thing to check?", "reference_answer": "Confirm power status at the site (mains, battery, generator).", "gold_doc_id": "RB003_link_down"},
    {"question": "What should happen if a site has a redundant backhaul path during a link-down event?", "reference_answer": "The redundant path should fail over; if it doesn't, escalate as a failover-mechanism defect.", "gold_doc_id": "RB003_link_down"},
    {"question": "Why does throughput drop only during peak hours on a healthy-looking cell?", "reference_answer": "Cell or backhaul capacity insufficient for peak demand, or a neighboring cell outage shifting load.", "gold_doc_id": "RB004_congestion"},
    {"question": "Subscribers report no internet but radio and backhaul look healthy, what should I check?", "reference_answer": "Check DNS query success rate and resolver health, since this points to DNS resolution failure.", "gold_doc_id": "RB005_dns"},
    {"question": "What can cause a BGP session to repeatedly flap?", "reference_answer": "An unstable physical link, MTU mismatch, keepalive timer misconfiguration, or router CPU exhaustion.", "gold_doc_id": "RB006_bgp"},
    {"question": "Voice calls sound choppy but latency and loss look fine, what's the likely cause?", "reference_answer": "Excessive jitter, often from insufficient QoS prioritization for RTP traffic.", "gold_doc_id": "RB007_jitter"},
    {"question": "What distinguishes a handover-related VoLTE call drop from a core-related one?", "reference_answer": "Drops clustering at cell edges point to handover issues; uniform drops point to the IMS core/signaling.", "gold_doc_id": "RB008_volte"},
    {"question": "What should I check when handover failures spike between two specific neighboring cells?", "reference_answer": "Verify the neighbor-cell-relation table and handover thresholds for that pair, and check for RF interference.", "gold_doc_id": "RB009_handover"},
    {"question": "How do I tell an unplanned cell outage apart from a simple link-down state?", "reference_answer": "In a total outage the site is unreachable even on the management plane, not just showing link down.", "gold_doc_id": "RB010_outage"},
    {"question": "Several co-located cells lose backhaul at once, what's the likely cause?", "reference_answer": "A physical fiber cut or a patch-panel/connector failure at an aggregation point.", "gold_doc_id": "RB011_backhaul"},
    {"question": "A cell shows persistently weak RSRP even though the site is powered and healthy, what should I suspect?", "reference_answer": "Antenna misalignment (tilt/azimuth drift) or a damaged antenna/feeder.", "gold_doc_id": "RB012_rf"},
    {"question": "What does it mean when a cell's PRB utilization sustains above 90%?", "reference_answer": "It's a capacity threshold breach that degrades throughput for all attached subscribers.", "gold_doc_id": "RB013_capacity"},
    {"question": "What should I check for elevated RRC connection setup failures?", "reference_answer": "Check whether failures correlate with PRB congestion or uplink interference, and check for a recent baseband software change.", "gold_doc_id": "RB014_signaling"},
    {"question": "An eNodeB loses its S1 connection to the core, what should I check first?", "reference_answer": "Check transport-layer reachability to the MME first, at the IP layer.", "gold_doc_id": "RB015_core"},
    {"question": "Throughput is degraded but PRB and backhaul utilization look normal, what should I check?", "reference_answer": "Segment by device type and check whether a MIMO/carrier-aggregation feature is disabled.", "gold_doc_id": "RB016_throughput"},
    {"question": "A site-to-site VPN tunnel is down, what's the first thing to check?", "reference_answer": "Check IKE phase 1/phase 2 negotiation logs for the specific failure reason.", "gold_doc_id": "RB017_vpn"},
    {"question": "New devices can't get an IP address at a site, what should I check?", "reference_answer": "Check DHCP pool utilization for exhaustion and check for a rogue DHCP server on the segment.", "gold_doc_id": "RB018_dhcp"},
    {"question": "What can cause NTP synchronization failures on network elements?", "reference_answer": "The configured NTP source being unreachable, a firewall change blocking UDP/123, or the source itself drifting.", "gold_doc_id": "RB019_ntp"},
    {"question": "A baseband unit keeps rebooting every few minutes, what should I check?", "reference_answer": "Pull crash logs and compare the firmware version against known-issue advisories, especially after a recent upgrade.", "gold_doc_id": "RB020_firmware"},
    {"question": "A site shuts down during hot weather and recovers when it cools, what's the likely cause?", "reference_answer": "HVAC/cooling failure or blocked ventilation causing a thermal shutdown.", "gold_doc_id": "RB021_power"},
    {"question": "A site briefly drops with mains-loss and battery-engage alarms, what should I check first?", "reference_answer": "Check for a known utility power outage in the area before assuming a hardware fault.", "gold_doc_id": "RB022_power"},
    {"question": "A microwave backhaul link degrades during rain and recovers afterward, what's the cause?", "reference_answer": "Rain fade or fog attenuation exceeding the link's fade margin.", "gold_doc_id": "RB023_backhaul"},
    {"question": "Some sessions behind a load balancer fail while others succeed, what should I check?", "reference_answer": "Check per-backend error rate and health-check status to find the specific unhealthy backend.", "gold_doc_id": "RB024_core"},
    {"question": "A previously stable IPsec tunnel suddenly fails with no config changes, what's the most common cause?", "reference_answer": "An expired X.509 certificate used for IKE authentication on one of the endpoints.", "gold_doc_id": "RB025_security"},
    {"question": "What's a common cause of clock drift alarms cascading into authentication failures?", "reference_answer": "NTP synchronization failure, since certificate/time-window checks depend on accurate clocks.", "gold_doc_id": "RB019_ntp"},
    {"question": "What's the difference between rain fade and antenna misalignment on a microwave link?", "reference_answer": "Rain fade correlates with weather and recovers after it clears; misalignment persists regardless of weather.", "gold_doc_id": "RB023_backhaul"},
]

INCIDENTS = [
    {"incident_text": "Site 03 backhaul link shows link down, radio hardware still alarming healthy.", "expected_cause": "backhaul_failure", "expected_severity": "critical"},
    {"incident_text": "Cell at site 07 has latency over 200ms for the last hour, throughput looks normal.", "expected_cause": "latency", "expected_severity": "medium"},
    {"incident_text": "Site 12 packet loss climbed to 4% over the last 15 minutes.", "expected_cause": "packet_loss", "expected_severity": "high"},
    {"incident_text": "Subscribers at site 05 report no internet access, backhaul and radio both look healthy.", "expected_cause": "dns", "expected_severity": "medium"},
    {"incident_text": "Site 09 throughput dropped to 40% of baseline only between 6pm and 9pm.", "expected_cause": "congestion", "expected_severity": "medium"},
    {"incident_text": "Site 14 has gone completely unreachable, including on the management plane.", "expected_cause": "outage", "expected_severity": "critical"},
    {"incident_text": "Handover success rate between site 02 and site 03 dropped sharply this morning.", "expected_cause": "handover", "expected_severity": "high"},
    {"incident_text": "VoLTE call drop rate at site 08 is elevated, drops concentrated near the cell edge.", "expected_cause": "handover", "expected_severity": "high"},
    {"incident_text": "Site 16 PRB utilization has been above 92% for six straight hours.", "expected_cause": "capacity", "expected_severity": "medium"},
    {"incident_text": "Site 11 baseband unit has rebooted five times in the last twenty minutes.", "expected_cause": "firmware", "expected_severity": "critical"},
    {"incident_text": "Site 04 dropped briefly with a mains-power-loss alarm then battery engaged, now back on mains.", "expected_cause": "power", "expected_severity": "low"},
    {"incident_text": "Site 19 microwave backhaul RSL has been degraded since the storm started an hour ago.", "expected_cause": "backhaul_fade", "expected_severity": "medium"},
    {"incident_text": "Site 06 RRC connection setup failure rate spiked right after last night's firmware push.", "expected_cause": "signaling", "expected_severity": "high"},
    {"incident_text": "A site-to-site VPN tunnel between site 10 and the core has been down for 30 minutes.", "expected_cause": "vpn", "expected_severity": "high"},
    {"incident_text": "Site 17 IPsec tunnel to the core failed to renegotiate this morning, no config changes reported.", "expected_cause": "security_cert", "expected_severity": "high"},
]

(EVAL_DIR / "qa_set.json").write_text(json.dumps(QA_SET, indent=2))
(EVAL_DIR / "incidents.json").write_text(json.dumps(INCIDENTS, indent=2))
print(f"Wrote {len(QA_SET)} QA pairs and {len(INCIDENTS)} incidents")
