# Governance pack — the organizational controls

The capstone's *technical* controls live in code and CI (see
[../COMPLIANCE.md](../COMPLIANCE.md)). This folder covers the other half: the
**process, policy, and evidence** controls an auditor expects that **no repo can
produce on its own**. These are **templates** — adopt them, fill the `TODO`s with
your org's real owners/dates/values, and (the hard part) *operate* them on a
cadence. A policy you wrote once and never followed fails an audit faster than
not having it.

> Seeded with the ShopKit reference's specifics (PII = email/name, financial =
> orders + Stripe refs, vendors = Stripe/GCP/GitHub/PyPI/npm) so the examples are
> concrete. Swap them for your capstone app's.

| Template | Control area | SOC 2 / ISO |
|----------|--------------|-------------|
| [data-governance.md](data-governance.md) | Data classification, retention, encryption, privacy/DSAR/breach | C1, P-series / A.5.12, A.5.34, A.8.10–12 |
| [access-control.md](access-control.md) | RBAC, least-privilege, joiner/mover/leaver, access reviews, MFA/SSO | CC6.1–6.3 / A.5.15–18 |
| [risk-register.md](risk-register.md) | Risk identification, scoring, treatment, review | CC3.x / A.5.7, Clause 6.1 |
| [third-party-register.md](third-party-register.md) | Vendor / subprocessor inventory + DPA tracking | CC9.2 / A.5.19–23 |
| [business-continuity-dr.md](business-continuity-dr.md) | RTO/RPO, backup/restore, DR test cadence | A1.2 / A.5.29–30 |
| [incident-and-breach-response.md](incident-and-breach-response.md) | IR plan, severity, comms, regulator/customer breach notice | CC7.3–7.5 / A.5.24–27 |
| [assurance-and-training.md](assurance-and-training.md) | Third-party pen-test policy, security training, audit-evidence checklist | CC4.1 / A.6.3, A.5.35 |

## How this fits the capstone

- **Solo learners:** read these to understand what production governance looks
  like beyond the code; you're not expected to operate them.
- **Teams / a real org:** adopt the pack, assign owners, set the review cadences,
  and keep the evidence. [assurance-and-training.md](assurance-and-training.md)'s
  checklist tells you what evidence to retain and where it already comes from
  (CI logs, PR history, this pack).

## Cadence automation (so the reviews actually happen)

A policy that says "review quarterly" only counts if the review happens on time
and is recorded. The reference automates the **prompting, tracking, and the
parts that *can* be automated** via scheduled GitHub Actions (in
`../reference-solution/.github/workflows/`):

| Workflow | Does | Cadence |
|----------|------|---------|
| `compliance-calendar.yml` | Auto-opens a tracked **review issue** (from `.github/compliance/` checklists) for access/risk/vendor/DR/training/pen-test. The closed issue = evidence. | quarterly + annual (+ manual) |
| `dr-restore-test.yml` | **Rebuilds** the stack from code+migrations and checks time-to-ready vs an RTO budget | monthly (+ manual) |
| `compliance-evidence.yml` | Snapshots audits/licenses/SAST/SBOMs into a **retained artifact** | monthly (+ manual) |

What stays human: the **judgment/sign-off inside each issue**, a **real backup
restore**, and the **independent pen-test** — the workflow opens the issue and
times the rebuild, but a person still decides and attests.

## The honest boundary

A capstone (and this pack) gets you **controls + templates + automated cadence +
evidence**. Certification (SOC 2 Type II, ISO 27001) additionally requires an
**independent auditor** to confirm the controls **operated effectively over a
period** — which is people and time, not a repository.
