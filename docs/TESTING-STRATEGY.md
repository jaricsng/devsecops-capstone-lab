# Testing Strategy — the capstone's testing discipline

A core habit this capstone builds: **every layer of confidence has its own test
type, and each maps to a stage of the DevSecOps lifecycle.** Shipping an app
with only unit tests (or only a happy-path click-through) is not "tested" — it's
*partially* tested. This doc is the contract for what "tested" means here.

You must build **all six** categories for *your* app. The ShopKit
[reference solution](../reference-solution/) demonstrates a **minimal real
example of each** — copy the *pattern*, then build a *comprehensive* set for
your own surfaces. Each is a graded [RUBRIC](../RUBRIC.md) item with an
objective signal.

## The shape: a pyramid + specialized gates

```
            /\        E2E  — few, slow, whole-system, real browser
           /  \
          /----\      Integration — real DB/deps, narrower
         /      \
        /--------\    Unit — many, fast, isolated
       /__________\

   cross-cutting gates (run in CI, not "more tests"):
   Security (SAST/deps/secrets/IaC/image) · Load · Pen/DAST
```

- **Lots of unit tests**, fewer integration, fewest e2e (the classic pyramid —
  fast feedback at the bottom, realistic confidence at the top).
- **Security, load, and pen tests are gates**, not pyramid layers. They answer
  different questions ("is it safe / fast enough / attackable?") and run at
  specific lifecycle stages.

## The six categories → lifecycle stage → what "done" means

| # | Category | Question it answers | Lifecycle stage / Module | "Done" signal |
|---|----------|---------------------|--------------------------|---------------|
| 1 | **Unit** | Does each function/route behave in isolation? | Build — [Module 02](../modules/02-build-app.md) | Test runner green; a coverage gate enforced (e.g. `--cov-fail-under`) |
| 2 | **Integration** | Do the real pieces (DB, migrations, deps) work *together*? | Build — [Module 02](../modules/02-build-app.md) | A test runs against the **real engine** (Postgres), not a stub/SQLite, exercising migrations + real queries |
| 3 | **E2E** | Does a real user journey work through the whole stack + UI? | CI gate — [Module 03](../modules/03-shiftleft-ci.md) | A browser test (Playwright/Cypress) drives the running app end-to-end and passes in CI |
| 4 | **Security** (SAST/deps/secrets/IaC/image) | Is the code/supply-chain free of known-bad patterns? | Shift-left — [Module 03](../modules/03-shiftleft-ci.md) | SAST + dependency-audit + secret-scan + (IaC + image scan) run and pass in pre-commit/CI |
| 5 | **Load** | Does it meet latency/error SLOs under traffic? | Perf — [Module 05](../modules/05-load-testing.md) | A load tool hits **your** routes and **declared thresholds pass**; correlated with traces/metrics |
| 6 | **Pen / DAST** | Can an attacker break authz, payments, inputs? | Security testing — [Module 06](../modules/06-security-pentest.md) | Authz/IDOR + DAST checks run against **your** endpoints; findings recorded + remediated |

## Anti-patterns this catches (don't do these)

- **"Integration" tests that swap the real DB for SQLite/mocks.** That's a unit
  test wearing a costume — it never validates migrations, constraints, or
  dialect-specific SQL. At least one test must hit real Postgres.
- **A green E2E *job* with no E2E *tests*** (an empty Playwright job that always
  passes, or one that can't reach the app). The reference's CI even waits for a
  frontend container — if it isn't there, the job is theater.
- **Load scripts pointed at example routes** you deleted — they 404 and "pass"
  by hitting nothing. Point every scenario at your real journeys.
- **A security/pen step that's documented but never executed.** A finding you
  never ran for is not a finding.

## How the reference models each (minimal, copyable)

| Category | Where in ShopKit |
|----------|------------------|
| Unit | `backend/tests/test_*.py` (pytest), `frontend/src/**/*.test.ts` (vitest) |
| Integration | `backend/tests/integration/test_db_integration.py` (real Postgres, `@pytest.mark.integration`) |
| E2E | `frontend/e2e/*.spec.ts` (Playwright) + the `frontend` service in `docker-compose.yml` |
| Security | pre-commit (bandit/detect-secrets/ruff) + `ci.yml` security job (pip-audit/npm audit) + `publish.yml` (Trivy/SBOM) |
| Load | `load-testing/k6/{smoke,load,spike}.js`, `load-testing/locust/locustfile.py` (all on ShopKit routes) |
| Pen / DAST | `security/manual-checks.sh` (ShopKit authz/IDOR) + `security/zap-scan.sh` + `SECURITY-FINDINGS.md` |

> The reference shows *one* of each so you can see the shape. Your capstone is
> graded on building a *comprehensive* set for your own app — that's the habit.
