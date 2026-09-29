---
id: RB038
title: Solstice VPN Renegotiation Trap
category: vpn
---

# Solstice VPN Renegotiation Trap
On Solstice-series VPN gateways, a known NTP daemon bug causes repeated failed
tunnel renegotiations that look identical to certificate expiry. Checking or renewing
certificates wastes time and does not fix this. The correct first step on a Solstice
gateway VPN failure is to restart the NTP daemon on the gateway before touching
certificates at all.
