# Assurance: Pen-Testing, Training & Audit Evidence

> Template. Owner: `TODO-security-lead`.

## 1. Independent penetration testing

Module 06 teaches **self**-testing (manual checks + ZAP + threat model). Compliance
additionally expects an **independent, third-party** test.

| Item | Policy |
|------|--------|
| Cadence | At least **annually** + after any major architecture change (`TODO`) |
| Scope | App + API + IaC + auth/payment flows; rules of engagement agreed in writing |
| Vendor | `TODO` (CREST/OSCP-credentialed firm) |
| Remediation SLA | Critical: `TODO`d · High: `TODO`d · report tracked in the [risk register](risk-register.md) |
| Evidence | Signed report + remediation tracker |

The self-test (`security/manual-checks.sh`, ZAP, `SECURITY-FINDINGS.md`) is the
*precursor* — fix what you can find yourself so the paid test finds the hard stuff.

## 2. Security awareness & secure-coding training

| Audience | Training | Cadence |
|----------|----------|---------|
| All staff | Security awareness (phishing, data handling, reporting) | Onboarding + annual |
| Engineers | Secure coding (OWASP Top 10), this kit's `claude-commands` (`/threat-model`, `/security-review`) | Onboarding + annual |
| All | Phishing simulation | `TODO` (e.g. quarterly) |

Evidence: completion records + sim results. (`TODO`: platform — e.g. an LMS.)

## 3. Audit-readiness — evidence checklist

For each control, an auditor wants evidence it **operated**, not just that it exists.
Most of ours is generated automatically:

| Control | Evidence | Where it lives |
|---------|----------|----------------|
| Change mgmt (PR + review + CI) | PR history, required-check + code-owner records | GitHub PRs / branch protection |
| SAST / deps / secrets / licenses | CI run logs (bandit, pip/npm audit, detect-secrets, license scan) | GitHub Actions |
| Image vulnerability scanning | Trivy results on PRs + at release; SBOM artifacts | Actions / release artifacts |
| Migration safety | `check_migrations.py` gate results | Actions |
| Provenance / signing | SBOM (CycloneDX) + SLSA + cosign | `publish.yml` artifacts |
| Audit logging | Structured security events (auth, admin, checkout) | App logs (`app/audit.py`) → log store |
| Observability / SLOs | Dashboards, alerts, recording rules | Grafana / Prometheus |
| Incident response | Post-mortems, incident timelines | `operations/runbooks/` + tickets |
| Access reviews | Completed review tables / IdP exports | [access-control.md](access-control.md) |
| DR | DR test log | [business-continuity-dr.md](business-continuity-dr.md) |
| Risk management | Risk register + review history | [risk-register.md](risk-register.md) |
| Vendor risk | Subprocessor register + DPAs | [third-party-register.md](third-party-register.md) |
| Pen testing | 3rd-party report + remediation tracker | this doc + risk register |

> The capstone makes most evidence a **byproduct of doing the work** (CI logs, PR
> history). The remaining gaps are the human-cadence ones — reviews, tests, and
> training actually performed on schedule.
