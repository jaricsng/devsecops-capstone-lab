# Compliance & Governance Mapping

What this capstone demonstrates in **technical controls**, mapped to common
frameworks — and, just as importantly, **what it does *not* cover** (the process
and evidence an organization must add). Compliance = controls **+ evidence +
process**; a repo can supply the first and some of the second, never the third.

> Framework abbreviations: **SOC 2** = Trust Services Criteria (CC = Common
> Criteria); **ISO** = ISO/IEC 27001:2022 Annex A; **CIS** = CIS Controls v8.
> Mappings are indicative (to teach the shape), not an audit attestation.

## Controls the capstone implements & verifies

| Control area | Where in the capstone | SOC 2 | ISO A.* | CIS |
|---|---|---|---|---|
| Change management (PR + review + CODEOWNERS + branch protection) | [Module 03](modules/03-shiftleft-ci.md), [09](modules/09-team-track.md); shopkit `.github/CODEOWNERS` + required-checks/code-owner branch protection | CC8.1 | A.8.32 | 4 |
| SAST / static analysis | bandit, ruff in pre-commit + CI `security` job | CC7.1, CC8.1 | A.8.28 | 16 |
| Dependency / supply-chain CVEs | pip-audit + npm audit (CI); Dependabot (monthly, grouped) | CC7.1 | A.8.8 | 7 |
| Secrets management | detect-secrets (pre-commit + baseline), Secret Manager in IaC, no creds in code | CC6.1 | A.8.24, A.5.17 | 3 |
| Vulnerability disclosure | `SECURITY.md` (private reporting) | CC2.3 | A.5.5 | — |
| Logging & monitoring (observability) | [Module 04](modules/04-observability.md): OTel traces/metrics, Prometheus, Grafana, Alertmanager | CC7.2 | A.8.15, A.8.16 | 8 |
| SLOs / availability monitoring | `operations/SLOs.md` + recording rules + burn-rate alerts | A1.1 | A.8.6 | — |
| Security audit logging | `backend/app/audit.py` — structured events (auth, profile, account-delete, admin, checkout) | CC7.2 | A.8.15 | 8 |
| Incident response & post-mortems | `operations/runbooks/` (incident-response, rollback, postmortem) | CC7.3, CC7.4 | A.5.24–A.5.27 | 17 |
| Secure SDLC test discipline | [docs/TESTING-STRATEGY.md](docs/TESTING-STRATEGY.md): unit/integration/e2e/security/load/pen, gated in CI | CC8.1 | A.8.25, A.8.29 | 16 |
| DAST / penetration testing | [Module 06](modules/06-security-pentest.md): `manual-checks.sh` (authz/IDOR), ZAP baseline, STRIDE in `SECURITY-FINDINGS.md` | CC4.1 | A.8.29 | 18 |
| Policy-as-code / config governance | [Module 07](modules/07-iac-governance.md): Conftest/OPA over Terraform plans; tfsec | CC7.1 | A.8.9 | 4 |
| Change safety for data (zero-downtime migrations) | `check_migrations.py` expand/contract gate | CC8.1 | A.8.32 | — |
| Container / image security | Trivy on PRs (`docker-build`) **and** at release (`publish.yml`), HIGH/CRITICAL gate | CC7.1 | A.8.8 | 16 |
| Software provenance / integrity | SBOM (CycloneDX) + SLSA provenance + cosign signing in `publish.yml` | CC7.1 | A.8.30 | 7 |
| IaC review & drift detection | `terraform validate`/`plan`, `drift-detection.yml` | CC7.1 | A.8.9 | 4 |
| Data-subject deletion (privacy) | `DELETE /users/me` + token invalidation (GDPR Art. 17 shape) | C1.1 | A.5.34 | — |
| CI reproducibility / pinned toolchain | `.tool-versions`, devcontainer, lockfiles (`package-lock.json`) | CC8.1 | A.8.31 | 2 |

## The organizational controls (process + evidence)

Technical controls are necessary but not sufficient — an auditor also wants
**process and evidence** a repo can't produce on its own. The **[governance/](governance/)
pack now provides an adopt-ready template for each**; what remains is for your
org to fill the `TODO`s and *operate* them on a cadence (the part no artifact can do).

| Control | Template | Still requires (you) |
|---------|----------|----------------------|
| Access management & reviews *(SOC 2 CC6.1–6.3, ISO A.5.15–18)* | [governance/access-control.md](governance/access-control.md) | IdP/SSO+MFA, run the quarterly review |
| Data classification & retention *(ISO A.5.12, A.8.10–12, A.5.34)* | [governance/data-governance.md](governance/data-governance.md) | Set retention values; CMEK; DSAR/export process |
| **Audit-log retention & review** *(CC7.2, ISO A.8.15)* | ✅ **emission now in code** (`backend/app/audit.py`) + [assurance-and-training.md](governance/assurance-and-training.md) | Ship to a tamper-evident store; retention; periodic review |
| Risk assessment *(CC3.x, ISO A.5.7)* | [governance/risk-register.md](governance/risk-register.md) | Score, treat, review quarterly |
| Vendor / 3rd-party risk *(CC9.2, ISO A.5.19–23)* | [governance/third-party-register.md](governance/third-party-register.md) | DPAs; vendor reviews |
| BCP / DR *(A1.2, ISO A.5.29–30)* | [governance/business-continuity-dr.md](governance/business-continuity-dr.md) | Set RTO/RPO; **test** restore on a schedule |
| Incident & breach response *(CC7.3–7.5, ISO A.5.24–27)* | [governance/incident-and-breach-response.md](governance/incident-and-breach-response.md) + `operations/runbooks/` | Run tabletops; maintain contacts |
| Independent penetration test *(CC4.1)* | [governance/assurance-and-training.md](governance/assurance-and-training.md) | Engage a 3rd-party firm annually |
| Security awareness training *(ISO A.6.3)* | [governance/assurance-and-training.md](governance/assurance-and-training.md) | Deliver + record completion |
| Formal policies & evidence | the whole [governance/](governance/) pack + [audit-readiness checklist](governance/assurance-and-training.md) | Approve policies; retain evidence over the period |

> HR security and physical security *(ISO A.6.x, A.7.x)* are wholly
> organizational and out of scope for a software capstone — note them in your ISMS.

## Supply-chain hardening — status & recommendations

| Item | Status | To strengthen |
|------|--------|---------------|
| SBOM (CycloneDX) | ✅ generated in `publish.yml` at build | Publish/attest the SBOM with each release |
| SLSA provenance + signing | ✅ in `publish.yml` (cosign) | Verify signatures at deploy admission |
| Frontend lockfile | ✅ `package-lock.json` (CI uses `npm ci`) | — |
| **Backend lockfile** | ✅ hash-pinned `requirements.txt` (`pip-compile --generate-hashes`); Dockerfile installs `--require-hashes` then the app `--no-deps` | — |
| **Dependency license scanning** | ✅ CI `security` job: `pip-licenses` (fail on GPL/AGPL; LGPL/MPL allowed) + `license-checker` (production deps permissive) | — |
| Image scanning on PRs | ✅ Trivy in the PR `docker-build` job (HIGH/CRITICAL, ignore-unfixed) — caught & fixed 31 CVEs in the frontend base | — |
| Action pinning | ✅ third-party actions (e.g. `trivy-action`) pinned to commit SHA | Renovate/Dependabot keeps SHAs current |

## How to demonstrate it

Run the kit's scorecard: in Claude Code, `/compliance-check` (or
`/compliance-check governance`) produces a pass/fail scorecard across code
quality, security, architecture, governance, observability, docs, containers,
and CI/CD. Pair its output with this mapping and the evidence in
[KIT-VERIFICATION.md](KIT-VERIFICATION.md) for a control walkthrough.
