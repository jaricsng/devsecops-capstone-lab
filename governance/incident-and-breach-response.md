# Incident & Breach Response

> Template. Owner: `TODO-incident-commander` · Test: tabletop exercise at least annually.
> Pairs with the technical runbooks in the reference: `operations/runbooks/`
> (incident-response, rollback, postmortem).

## Severity levels

| Sev | Definition | Response |
|-----|------------|----------|
| **SEV1** | Outage or confirmed data breach | Page on-call immediately; incident commander; all-hands |
| **SEV2** | Major degradation / SLO burn / suspected breach | Page; commander assigned |
| **SEV3** | Minor / single-component | Ticket; next business day |

## Lifecycle

1. **Detect** — alert (Alertmanager burn-rate / `ServiceUnreachable`), report, or finding.
2. **Triage** — assign severity + incident commander; open an incident channel/ticket.
3. **Contain** — stop the bleeding (feature flag off, rotate creds, block IP, scale).
4. **Eradicate & recover** — fix root cause; restore service (rollback runbook / DR).
5. **Notify** — see breach notification below.
6. **Post-mortem** — blameless, within `TODO` (e.g. 5 business days); track action items to done (`operations/runbooks/postmortem-template.md`).

## Breach notification (when PII/financial data is exposed)

Time limits are legal, not best-effort — know them in advance:

| Who | When | Notes |
|-----|------|-------|
| **Supervisory authority** (GDPR Art. 33) | **≤ 72h** of awareness | Unless unlikely to risk rights/freedoms |
| **Affected individuals** (GDPR Art. 34) | "Without undue delay" if high risk | Clear language, what/impact/remediation |
| **Customers / partners** | Per contract (`TODO`) | Often 24–72h SLAs |
| **Payment processor (Stripe)** | Per agreement | If card-flow involved |
| **Regulators (e.g. state breach laws)** | Per jurisdiction (`TODO`) | |

Maintain notification templates + a contact list in advance — you don't want to
draft these during a SEV1.

## Roles

| Role | Who | Responsibility |
|------|-----|----------------|
| Incident Commander | `TODO` | Owns the incident, decisions, comms |
| Comms lead | `TODO` | Internal + external messaging |
| Scribe | `TODO` | Timeline for the post-mortem (evidence) |
| Legal/Privacy | `TODO` | Breach-notification obligations |
