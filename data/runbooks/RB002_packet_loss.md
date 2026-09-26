---
id: RB002
title: Packet Loss on Access Link
category: packet_loss
---

# Packet Loss on Access Link
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
