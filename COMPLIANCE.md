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

## What the capstone does **not** cover (your org must add)

Technical controls are necessary but not sufficient. An auditor will also ask
for **process and evidence** that a repo cannot produce on its own:

- **Access management & reviews** — IdP/SSO, least-privilege RBAC, periodic
  access recertification, joiner/mover/leaver. *(SOC 2 CC6.1–CC6.3, ISO A.5.15–A.5.18)*
- **Data classification & retention** — classify PII/order data, retention &
  deletion schedules, encryption-at-rest key management (CMEK). *(ISO A.5.12, A.8.10–A.8.12)*
- **Audit-log retention & review** — ship logs to a tamper-evident store with a
  defined retention period and review cadence (the capstone *emits* telemetry;
  it doesn't *retain/review* it). *(SOC 2 CC7.2, ISO A.8.15)*
- **Risk assessment & vendor/3rd-party risk** — register, risk-rank, review
  subprocessors. *(SOC 2 CC3.x, ISO A.5.19–A.5.23)*
- **BCP / DR** — backups are configured in IaC, but you need tested RTO/RPO and
  DR runbooks exercised on a schedule. *(SOC 2 A1.2, ISO A.5.29–A.5.30)*
- **Security awareness training**, **HR security**, **physical security**. *(ISO A.6.x)*
- **Independent penetration test** — Module 06 teaches self-testing; compliance
  typically wants a periodic **third-party** test. *(SOC 2 CC4.1)*
- **Formal policies & evidence** — written InfoSec policy set, and the *evidence*
  (tickets, approvals, logs) that controls operated over the audit period.

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
