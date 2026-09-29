---
id: RB042
title: Multi-Site Capacity Escalation and Load-Shed Procedure
category: capacity
---

# Multi-Site Capacity Escalation and Load-Shed Procedure
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
