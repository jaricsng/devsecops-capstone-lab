# Business Continuity & Disaster Recovery

> Template. Owner: `TODO-platform-lead` · **DR test cadence: at least annually** (test, don't assume).

## Objectives (set with the business)

| Metric | Target | Meaning |
|--------|--------|---------|
| **RTO** (recovery time) | `TODO` (e.g. 4h) | Max acceptable downtime |
| **RPO** (recovery point) | `TODO` (e.g. 1h) | Max acceptable data loss |

## What's already in place (ShopKit/IaC)

- **Backups:** Cloud SQL automated backups (7d staging / 30d prod) + point-in-time recovery in prod — see `iac-terraform/gcp-cloud-run/main.tf`.
- **Stateless app:** Cloud Run scales/rebuilds from the container image; no state on instances.
- **IaC:** environment is reproducible from Terraform (rebuild from code, not snowflakes).
- **Rollback:** `operations/runbooks/rollback.md` + feature flags decouple deploy from release.

## Gaps to close for real continuity (`TODO`)

- **Tested restore:** prove a backup actually restores within RTO/RPO — run it, record the time. An untested backup is a hope, not a control.
- **Cross-region / multi-AZ:** define failover if the region is lost.
- **Dependency outage plan:** graceful degradation when Stripe/GCP is down (queue orders? read-only mode?).
- **Off-platform copy:** export of critical data outside the single cloud account (guards against account compromise/deletion).

## DR test log (evidence)

| Date | Scenario tested | RTO actual | RPO actual | Pass? | Notes |
|------|-----------------|-----------|-----------|-------|-------|
| `TODO` | Restore prod DB from backup | | | | |
| `TODO` | Rebuild env from Terraform | | | | |
| `TODO` | Region failover | | | | |
