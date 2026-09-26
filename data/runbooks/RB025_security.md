---
id: RB025
title: IPsec Tunnel Negotiation Failure After Cert Expiry
category: security
---

# IPsec Tunnel Negotiation Failure After Cert Expiry
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
