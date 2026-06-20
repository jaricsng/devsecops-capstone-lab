# Risk Register

> Template. Owner: `TODO-risk-owner` · Review: quarterly + on significant change.
> Score = Likelihood (1–5) × Impact (1–5). Treat: Mitigate / Accept / Transfer / Avoid.

Seeded with ShopKit's real risks (from `SECURITY-FINDINGS.md` + architecture).
Replace/extend for your app.

| # | Risk | L | I | Score | Treatment | Owner | Status |
|---|------|---|---|-------|-----------|-------|--------|
| R1 | Leaked JWT can't be revoked (stateless) | 3 | 3 | 9 | Mitigate: short TTL + refresh + revocation list | `TODO` | Open (accepted in reference) |
| R2 | No login rate limiting → brute force / credential stuffing | 3 | 3 | 9 | Mitigate: gateway rate limit + lockout | `TODO` | Open |
| R3 | Missing security headers (CSP/HSTS/etc.) | 3 | 2 | 6 | Mitigate: security-headers middleware / edge | `TODO` | Open |
| R4 | Cloud SQL public IP (mitigated by Auth Proxy + TLS) | 2 | 4 | 8 | Mitigate: private IP + VPC connector in prod | `TODO` | Open (accepted in reference) |
| R5 | Dependency/base-image CVE introduced | 3 | 3 | 9 | Mitigate: pip/npm audit + Trivy gates + Dependabot | Platform | **Controlled** |
| R6 | Secret committed to git | 2 | 5 | 10 | Mitigate: detect-secrets (pre-commit + CI) | Platform | **Controlled** |
| R7 | Backward-incompatible migration breaks rolling deploy | 2 | 4 | 8 | Mitigate: expand/contract + `check_migrations.py` gate | Platform | **Controlled** |
| R8 | Vendor outage (Stripe/GCP) | 2 | 4 | 8 | Transfer/Accept: SLAs; degrade gracefully | `TODO` | Open |
| R9 | Data breach of PII/financial data | 2 | 5 | 10 | Mitigate: encryption, access control, audit logging, IR plan | `TODO` | Open |

## How to run it

1. Identify risks (this list + brainstorm per feature; pair with `/threat-model`).
2. Score and prioritize; decide treatment + owner + due date.
3. Track "Controlled" ones to a verifiable control (CI gate, policy).
4. Re-review quarterly; add new risks from incidents, pen-tests, and changes.
