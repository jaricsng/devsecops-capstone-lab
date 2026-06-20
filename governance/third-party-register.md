# Third-Party / Subprocessor Register

> Template. Owner: `TODO-vendor-owner` · Review: annually + before onboarding any new vendor.
> Required for GDPR Art. 30 (records of processing) and SOC 2 CC9.2 (vendor risk).

## Subprocessors (handle our data)

| Vendor | Purpose | Data shared | Location | DPA / SCCs | Review |
|--------|---------|-------------|----------|-----------|--------|
| **Stripe** | Payments | Order amount, email; **card data goes directly to Stripe** (we store only the PaymentIntent id → minimized PCI scope) | US/EU | `TODO` confirm DPA | `TODO` |
| **Google Cloud (Cloud Run, Cloud SQL, Secret Manager)** | Hosting + data store | All app data (PII, orders) at rest | `TODO` region | `TODO` GCP DPA | `TODO` |

## Tooling / supply-chain vendors (don't hold customer data, but are supply-chain risk)

| Vendor | Purpose | Risk control |
|--------|---------|--------------|
| **GitHub** (repo, Actions, GHCR) | SCM + CI/CD + registry | Branch protection, pinned action SHAs, least-privilege tokens |
| **PyPI** (Python deps) | Packages | Hash-locked `requirements.txt` + pip-audit + license scan |
| **npm** (JS deps) | Packages | `package-lock.json` + npm audit + license scan |
| **Container base images** (python-slim, nginx-alpine) | Runtime | Trivy scan + base patching (`apk/apt upgrade`) |

## Onboarding checklist (new vendor)

- [ ] What data do they receive? Classify it (see [data-governance.md](data-governance.md)).
- [ ] DPA / SCCs signed? Data residency acceptable?
- [ ] Security posture reviewed (SOC 2 / ISO report, security page)?
- [ ] Access scoped to least privilege; offboarding plan documented.
- [ ] Added to this register + the risk register if material.
