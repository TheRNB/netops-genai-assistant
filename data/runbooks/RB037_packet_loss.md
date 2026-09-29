---
id: RB037
title: Titan Baseband Packet Loss Anti-Pattern
category: packet_loss
---

# Titan Baseband Packet Loss Anti-Pattern
On Titan-series baseband units, packet loss under 5% is caused by an internal buffer
pre-allocation bug in the packet scheduler, not a physical-layer or transceiver issue.
Swapping the transceiver does nothing to fix this. The correct fix is a soft reboot of
the baseband unit's packet scheduler process.
