# Module 03 — Shift-left security & CI

> **Goal:** catch problems at commit time (pre-commit) and on every push (GitHub
> Actions), so security and quality are gates, not afterthoughts. Exercises:
> `ci-cd/pre-commit/.pre-commit-config.yaml`, `ci-cd/github-actions/ci.yml`.

"Shift left" means moving checks as early as possible — a secret caught by a
pre-commit hook never reaches the remote; a broken build caught in CI never
reaches `main`. The scaffold already placed both configs; this module activates
them against *your* code.

## Step 1 — Install and run pre-commit

```bash
make setup          # installs hooks + creates .secrets.baseline if missing
pre-commit run --all-files
```

The hooks include: trailing-whitespace, **detect-secrets** (credential scan
against your baseline), **bandit** (Python SAST), **tfsec** (Terraform security)
when `*.tf` is staged, a **check-migrations** hook, and `no-commit-to-branch`.
Fix what they flag. If detect-secrets trips on a false positive (e.g. an example
token), audit and update the baseline: `detect-secrets scan > .secrets.baseline`
then review the diff.

> Prove the secret scanner works: temporarily add `AWS_SECRET=AKIA...` to a file
> and `git add` it — the hook should block the commit. Remove it after.

## Step 2 — Point CI at your source

Open `.github/workflows/ci.yml` and resolve the `working-directory:`
placeholders (the scaffold left these in `TODO.md`):

- backend job → your backend dir (e.g. `backend`)
- frontend job → your frontend dir (e.g. `frontend`), or delete the job if API-only
- the `services: postgres:` block → keep if you use Postgres; swap if not

## Step 3 — Make CI green

Push a branch and open a PR (or run [`act`](https://github.com/nektos/act)
locally). The CI shape is: lint → test → security → docker-build → smoke-test.
Your job is a green run. Common fixes: matching the test command to your
Makefile, ensuring the Dockerfile builds in CI, and making the smoke job's
`/health` curl succeed.

> The kit's `ci.yml` Conftest gate is intentionally **soft**
> (`continue-on-error: true` — report, not block). Leave it; hardening it to
> block is a deliberate choice you can make later. Likewise the deploy jobs in
> `publish.yml` carry `if: false` on purpose — don't remove it until Module 07.

## Step 4 — Security tests in the pipeline (RUBRIC 4d)

The `security` job runs the cross-cutting security tests — **SAST** (bandit),
**secret scan** (detect-secrets, also a pre-commit hook), and **dependency
audit** (pip-audit + npm audit). These must run and pass. Confirm your manifests
are clean (no high-severity CVEs, no flagged code patterns); fix or justify
anything they raise. (`publish.yml` adds Trivy image scanning + SBOM later.)

## Step 5 — End-to-end tests (RUBRIC 4c)

`ci.yml` ships an **`e2e` (Playwright)** job that boots the whole stack and drives
a real browser through a user journey. A job is not a test — you must **write the
e2e tests and make the stack reachable**:

- Add a browser test suite (Playwright in the reference: `frontend/e2e/*.spec.ts`,
  an `e2e` npm script, `playwright.config.ts`).
- The e2e job does `docker compose up` and waits for the **frontend** at `:5173` —
  so your `docker-compose.yml` must actually start a frontend service (the
  reference adds one). A common gotcha: the e2e job exists but the compose file
  has no frontend → it waits forever. Don't ship that.
- Cover at least one full journey: e.g. load home → browse catalog → (register →
  add to cart). Run locally first: `npx playwright test`.

Backend-only capstones: substitute an API-level e2e (drive the full deployed
stack via HTTP through every step of one real journey) and say so in your report.

> ### 🤖 Claude Code track
> - `/check-python` and `/check-frontend` — run the kit's lint/type gates and
>   fix what they report (`/fix-python`, `/fix-frontend` apply safe fixes).
> - `/security-scan` — multi-tool SAST/dependency/secret sweep across tiers.
> - `/check-secrets` — scan tracked files + git history for credentials.
> - Then: *"Read .github/workflows/ci.yml and my repo layout; set the
>   working-directory values and tell me why each job would currently fail."*

> ### 🛠️ Manual track
> - `pre-commit run --all-files` until clean.
> - Edit `ci.yml` working-directories by hand; compare against
>   `../reference-solution/.github/workflows/ci.yml` for a filled-in example.
> - Use `act` or a throwaway branch to iterate on the CI run.

> ### Different stack?
> `ci.yml` assumes pytest + npm test + a Postgres service. To swap the test
> runner, language toolchain, or database service container, follow
> `<kit>/docs/TECH-STACK-SWAP-GUIDE.md` ("CI platform" and "database" rows). The
> *shape* (lint→test→scan→build→smoke) stays; only the commands change.

## ✅ Checkpoint

- [ ] `pre-commit run --all-files` passes; you watched the secret scanner block
      a planted credential.
- [ ] `.secrets.baseline` is committed and current.
- [ ] **Security tests pass** (RUBRIC 4d): bandit (SAST), detect-secrets, and
      pip-audit/npm audit run clean in pre-commit/CI.
- [ ] **E2E tests exist and pass** (RUBRIC 4c): `npm run e2e` (Playwright) drives
      a real journey; your `docker-compose.yml` starts a reachable frontend.
- [ ] CI is **green** on your branch (lint, unit+integration, security, e2e,
      build, smoke all pass).

Next: **[Module 04 — Observability](04-observability.md)**.
