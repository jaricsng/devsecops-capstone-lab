# Kit Verification Matrix

This document answers a question separate from "did the learner pass": **does
the `platform-starter-kit` itself work as intended for someone building a new
app?**

The principle: *if a learner can complete this lab and land a doctor-green,
CI-green, observability-lit, deploy-planned repo, the kit is verified.* The
[`reference-solution/`](reference-solution/) is the canonical pass — it is a
real app scaffolded from the kit and then wired up exactly as the modules
instruct.

## Capability → Module → Pass criterion

| Kit asset | Lab module | Objective signal that the asset works |
|-----------|-----------|----------------------------------------|
| `tools/scaffold.py` | [01](modules/01-scaffold.md) | Produces a repo with resolved placeholders; `PLATFORM-KIT.md` records the source commit |
| `tools/doctor.py` | [01](modules/01-scaffold.md), [02](modules/02-build-app.md) | Reports the 3 known FAILs on a bare scaffold; reports **0 FAIL** once app code is added |
| `examples/minimal-service/` + `observability/` | [00](modules/00-orientation.md) | Boots via the documented Compose command; `/health` returns 200; Jaeger/Prometheus/Grafana reachable |
| `dev-experience/Makefile` | [02](modules/02-build-app.md)+ | `make help` lists targets; `make doctor`, `make obs-up`, `make sync` run |
| `ci-cd/pre-commit/.pre-commit-config.yaml` | [03](modules/03-shiftleft-ci.md) | `pre-commit run --all-files` passes on a clean tree; detect-secrets/bandit/tfsec fire on bad input |
| `ci-cd/github-actions/ci.yml` | [03](modules/03-shiftleft-ci.md) | CI run green after `working-directory` placeholders filled |
| `observability/*` (Prometheus, Grafana, Jaeger, Alertmanager) | [04](modules/04-observability.md) | Dashboard panels show real traffic; a trace appears; Alertmanager boots (no crash-loop) |
| `observability/recording_rules.yml` vs `grafana/dashboards/starter-dashboard.json` | [04](modules/04-observability.md) | The documented metric-name mismatch is surfaced and resolved by the learner (not silently) |
| `load-testing/k6/*`, `load-testing/locust/*` | [05](modules/05-load-testing.md) | A scenario runs against the app and reports threshold pass/fail |
| `security/manual-checks.sh`, `security/zap-scan.sh` | [06](modules/06-security-pentest.md) | Scripts run against the app's real endpoints and produce findings |
| `iac-terraform/gcp-cloud-run/*` | [07](modules/07-iac-governance.md) | `terraform validate` passes; `plan` runs with the app's `tfvars` |
| `governance/policy-as-code/*` | [07](modules/07-iac-governance.md) | `conftest test` exits 0 on `passing-plan.json`, 1 on `failing-plan.json` |
| `tools/check_migrations.py` | [07](modules/07-iac-governance.md) | Exit 1 on a `DROP COLUMN`; exit 0 on the expand/contract version |
| `operations/*` (SLOs, runbooks) | [08](modules/08-day2-ops.md) | SLO maps to a recording rule; a runbook is adaptable to the app |
| `docs/FEATURE-FLAGS.md` | [08](modules/08-day2-ops.md) | A release is toggled independent of deploy |
| Team assets (CODEOWNERS gen, `publish.yml` concurrency, `backend.tf.example`, `.gitattributes`) | [09](modules/09-team-track.md) | Concurrency group present; remote backend locks state; CODEOWNERS resolves |
| `tools/sync_check.py` | [10](modules/10-sync-and-submit.md) | Classifies each scaffolded file (unchanged / locally-modified / upstream-changed) |
| `claude-commands/*` | every (🤖 track) | Each referenced command runs and produces a useful report |

## Maintainer smoke-run

A fast, end-to-end check that the kit's pieces still work, mirroring the kit's
own `CLAUDE.md` "Validating changes" section. Run from a fresh kit clone:

```bash
KIT=../platform-starter-kit

# 1. Scaffold smoke
rm -rf /tmp/scaffold-smoke
python3 $KIT/tools/scaffold.py --app-name smoke-test --output /tmp/scaffold-smoke --cloud gcp
python3 /tmp/scaffold-smoke/tools/doctor.py /tmp/scaffold-smoke   # expect 3 FAIL (no Dockerfile/health/tests)
test -f /tmp/scaffold-smoke/.gitignore && test -f /tmp/scaffold-smoke/.secrets.baseline && echo "security defaults present"

# 2. Observability + example service boot
docker compose --project-directory $KIT \
  -f $KIT/examples/minimal-service/docker-compose.yml \
  -f $KIT/observability/docker-compose.observability.yml \
  --profile observability up --build -d
curl -sf http://localhost:8000/health && curl -sf http://localhost:8000/ready
docker compose --project-directory $KIT \
  -f $KIT/examples/minimal-service/docker-compose.yml \
  -f $KIT/observability/docker-compose.observability.yml \
  --profile observability down -v

# 3. Governance + migration gates
cd $KIT/governance/policy-as-code
conftest test --policy policy examples/passing-plan.json   # exit 0
conftest test --policy policy examples/failing-plan.json   # exit 1
cd -
printf 'ALTER TABLE t DROP COLUMN c;\n' > /tmp/m.sql
python3 $KIT/tools/check_migrations.py /tmp/m.sql          # exit 1
rm -f /tmp/m.sql /tmp/scaffold-smoke -rf
```

## Observed results

Recorded while building the reference solution against the kit.

- **Date:** 2026-06-19 – 2026-06-20 (testing-discipline pass added the integration/e2e/pen rows)
- **Kit commit (`PLATFORM-KIT.md`):** `5ba906377347b86bdd41dd561d1b874dc9038cc1`
- **Host:** macOS, Python 3.14 (deps loosened to min-version specifiers; kit
  pins 3.12 via `.tool-versions`), Node 24, Docker present.

| Capability / asset | What was run | Result |
|--------------------|--------------|--------|
| `scaffold.py` | `--app-name shopkit --cloud gcp` | ✅ produced repo; `PLATFORM-KIT.md` recorded the commit |
| `doctor.py` (bare scaffold) | `doctor.py .` | ✅ 3 expected FAIL (no Dockerfile/health/tests) |
| `doctor.py` (built reference) | `doctor.py .` | ✅ **0 FAIL** ("No blocking gaps found") |
| **Unit** (backend) | `pytest --cov` | ✅ **16 passed, 89.86% coverage** (≥70 gate) |
| **Unit** (frontend) | `vitest run` | ✅ **3 passed** |
| **Integration** (real Postgres) | `pytest -m integration` (throwaway PG container) | ✅ **3 passed** — alembic migrations applied, unique constraint + real SQL exercised; default run deselects them |
| **E2E** (Playwright) | `npx playwright test` vs the `frontend` compose service | ✅ **2 passed** — browser drives register→add-to-cart→checkout through nginx→API→Postgres |
| **Security** (lint/SAST/deps) | `ruff`/`black`/`isort`; **`bandit -r app`**; **`pip-audit`**; **`npm audit --audit-level=high`** | ✅ all clean — bandit 0 issues, pip-audit 0 CVEs, npm audit **0** (after bumping vitest→v3 to clear an esbuild/vite dev-tooling CVE chain that was 3 moderate/1 high/2 critical) |
| **Pen / DAST** | `security/manual-checks.sh` vs live ShopKit | ✅ **18 PASS, 7 WARN, 0 FAIL** — authz/IDOR/injection/business-logic all hold; WARNs = accepted defence-in-depth gaps |
| Frontend gates | `tsc -b` / `eslint .` / `vite build` | ✅ typecheck, lint, build all pass |
| Full stack | `docker compose up --build` | ✅ DB→migrate→seed(5)→uvicorn→frontend; register→cart→checkout (order $84.00) |
| `check_migrations.py` | `unsafe.sql` / `safe.sql` | ✅ exit 1 (blocked) / exit 0 (allowed) |
| `conftest` (governance) | passing / failing fixtures | ✅ exit 0 (1 warn) / exit 1 (2 failures) |
| `terraform` (IaC) | — | ⏭️ not run (terraform not installed here); tfvars wired (`shopkit`) |
| **Load** (k6) | `k6 run smoke.js` + `load.js` (15 VUs) vs live ShopKit | ✅ **executed** — smoke: 468 checks 100%, p95 9.9ms, 0% errors; load: 524 checks 100%, every per-route threshold pass (list<400, search<500, cart<600, checkout<800), 0% errors. (`spike.js`/Locust share the same routes; syntax-validated.) |
| **pre-commit** | `pre-commit run --all-files` (reference temp-repo) | ✅ all app hooks pass (detect-secrets after baseline refresh — also **catches a planted AWS key**; bandit, black, isort, ruff, check-migrations, file hooks). terraform_fmt/validate need the terraform binary; tfsec ran and flagged 8 hardening findings on the example IaC module (Module-07 work). |
| **Makefile** | `make help/lint/test/migrations` | ✅ wired to ShopKit (backend pytest+lint, frontend vitest+eslint, `make migrations` → backend/alembic) |
| **Frontend coverage gate** | `vitest run --coverage` thresholds | ✅ enforced (~40% lines / 57% funcs / 65% branches); pages covered by e2e. 13 unit tests. |
| `check_migrations.py` (reference's own migration) | `tools/check_migrations.py backend/alembic/versions` | ✅ exit 0 (baseline downgrade drops acknowledged via `migration-safety: ack`) |
| **observability overlay** | `docker compose -f … -f observability/… --profile observability up` | ✅ all 7 containers healthy (no crash-loop); Prometheus `app`+`readiness` targets **UP**; Jaeger service `shopkit` with traces; Grafana "Service Overview" + Jaeger/Prometheus datasources provisioned; **dashboard panel queries return live data** (req-rate 1.58/s, P95 ≈ 9 ms, per-route series) |
| metric-name mismatch | observed both names against live Prometheus | ✅ confirmed real (app default emitted old `http_server_duration_milliseconds`; dashboard queried new name → 0 series) **and resolved** in the reference toward the stable name (`OTEL_SEMCONV_STABILITY_OPT_IN=http` + reconciled `recording_rules.yml`); see `reference-solution/observability/METRIC-NAME-DECISION.md` |

### Findings about the kit (file upstream, don't paper over)

1. **Dangling doc cross-links in a scaffolded repo.** A `--cloud gcp` scaffold's
   `docs/FEATURE-FLAGS.md` links to `ENTERPRISE-TOOLING.md` and
   `governance/policy-as-code/README.md` links to `../../docs/TECH-STACK-SWAP-GUIDE.md`,
   but `scaffold.py` only copies `DATABASE-MIGRATIONS.md` + `FEATURE-FLAGS.md`
   into `docs/`, so those targets are absent. Cosmetic, but worth either copying
   the referenced docs or rewriting the links to the upstream kit. (Left as-is
   in the reference so the finding is visible.)
2. **Bug caught by the lab itself:** the reference's `seed.py` originally located
   its data file with `parents[3]`, which is out of range inside the container
   image (where the build context is `backend/` only). Fixed in the reference by
   walking parents and falling back to a built-in set — a good example of why
   Module 02's "boot it in Docker" checkpoint matters.
