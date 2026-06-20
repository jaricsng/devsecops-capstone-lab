# Access Control & Reviews

> Template. Owner: `TODO-security-lead` · Access review cadence: **quarterly** (privileged: monthly).

## 1. Principles

- **Least privilege** — grant the minimum needed; default deny.
- **SSO + MFA** everywhere it's supported (`TODO`: IdP — Google/Okta/Entra).
- **No shared accounts**; named identities only, so actions are attributable.
- **Just-in-time / time-boxed** elevation for production access where possible.

## 2. Access matrix (who can touch what)

| System | Role | Access | Grant via |
|--------|------|--------|-----------|
| GitHub repo | Maintainer | merge to `main` (PR + CI + code-owner review) | org team |
| GitHub repo | Contributor | open PRs | org team |
| Cloud (GCP) prod | Platform | deploy via WIF (keyless) — no human keys | IAM role + WIF |
| Cloud prod data | DBA (break-glass) | read/write, **logged + alerted** | JIT grant |
| App admin role | Admin | product CRUD (`require_admin`) | DB flag `is_admin` (`TODO`: move to IdP groups) |
| CI/CD secrets | Platform | manage repo/Actions secrets | repo admin |

In the app, authorization is enforced by `require_admin` / `get_current_user`
(object-level checks on cart & profile) — see `SECURITY-FINDINGS.md`.

## 3. Joiner / Mover / Leaver (JML)

- **Joiner:** access provisioned from role templates above; MFA enrolled day 1.
- **Mover:** re-baseline to the new role; remove old grants (don't accumulate).
- **Leaver:** revoke **same business day**; rotate any shared/ break-glass creds they could have seen.

## 4. Access review (the evidence an auditor wants)

Each cycle, record: system, who has access, role, justification, decision (keep/revoke), reviewer, date.

| Date | System | Reviewer | # accounts | Removed | Notes |
|------|--------|----------|-----------|---------|-------|
| `TODO` | GitHub | | | | |
| `TODO` | GCP IAM | | | | |
| `TODO` | App admins (`is_admin`) | | | | |

> Keep completed review tables (or exported IdP/IAM reports) as evidence. GitHub
> branch protection + CODEOWNERS already enforce *change* access; this covers
> *standing* access.
