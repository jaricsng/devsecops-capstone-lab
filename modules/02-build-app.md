# Module 02 — Build the app → doctor-green

> **Goal:** write enough of *your* application that `doctor.py` reports **0
> FAIL**. That means: a container, `/health` + `/ready`, OpenTelemetry wiring, a
> database, and at least one test. Exercises: `tools/doctor.py`'s checklist,
> `dev-experience/Makefile`, the `examples/minimal-service/` reference shape.

This is the biggest module. The trick is to let `doctor.py` drive you: each FAIL
it prints maps to one concrete thing to add. Build the *plumbing* first (so the
kit lights up), then the *features*.

## The doctor checklist you're satisfying

`doctor.py` greps your repo for signals. You need, at minimum:

| doctor check | What satisfies it |
|--------------|-------------------|
| Containerized | a `Dockerfile` (or `docker-compose.yml`) |
| Health/readiness endpoints | code that references **both** `/health` and `/ready` |
| OpenTelemetry instrumentation | an OTel dependency in your manifest (`requirements.txt`/`package.json`/…) |
| Automated tests present | a `test_*.py` / `*.test.ts` / `tests/` dir |
| Database engine | a Postgres client (`asyncpg`/`psycopg`) in your manifest → INFO (the kit's default) |
| Gitignore / secrets baseline | already PASS from scaffold — keep `.env` out of git |

## Step 1 — Plumbing: container + health + OTel + a test

Mirror the reference shapes:
- `<kit>/examples/minimal-service/main.py` — `/health`, `/ready` with trace spans
- `<kit>/examples/minimal-service/telemetry.py` — OTel SDK setup reading
  `OTEL_*` / `OTLP_ENDPOINT` env vars
- `<kit>/examples/minimal-service/Dockerfile` — non-root Python 3.12 container

This lab ships the same wiring in **[`../assets/otel-wiring/`](../assets/otel-wiring/)**
so manual-track learners don't get stuck on telemetry boilerplate.

Add a throwaway test (`tests/test_health.py` hitting `/health`) so the tests
check flips green immediately — you'll add real tests alongside each feature.

Re-run after each addition:

```bash
python3 tools/doctor.py .
```

## Step 2 — Database + migrations

Bring in Postgres + a migration tool (Alembic for SQLAlchemy). Define your
schema as the **first** migration. You'll exercise the migration-safety gate
properly in Module 07; for now just get a clean baseline migration and a
`docker-compose.yml` with a `postgres` service so `make up` works.

> Seed data for a browsable catalog lives in
> **[`../assets/seed/`](../assets/seed/)** — adapt it to your domain.

## Step 3 — Features

Build your application's real endpoints. For an e-commerce app (the reference),
the core set is:

- **Auth** — `POST /auth/register`, `POST /auth/login`, `POST /auth/logout` (JWT)
- **Profile** — `GET/PUT/DELETE /users/me` (CRUD your own profile)
- **Catalog** — `GET /products?q=&category=&page=` (browse + search)
- **Cart** — `GET /cart`, `POST /cart/items`, `DELETE /cart/items/{id}`
- **Checkout** — `POST /checkout` creating a Stripe **test-mode** PaymentIntent

The reference solution implements all of these — read
[`../reference-solution/`](../reference-solution/) when you're stuck, but build
*your* domain's equivalents, not a ShopKit clone.

Wire your real routes with tests as you go. Keep `/health` cheap (liveness) and
`/ready` meaningful (e.g. check the DB connection) — Module 04's dashboards and
every deploy job's post-check depend on the difference.

## Step 4 — Unit tests + a real integration test

This module owns the bottom two layers of the test pyramid (see
[docs/TESTING-STRATEGY.md](../docs/TESTING-STRATEGY.md)). Both are required
([RUBRIC](../RUBRIC.md) 4a/4b):

- **Unit tests** — fast, isolated, *many*. Cover each route's logic (happy path +
  the error/authz paths). Enforce a **coverage gate** so it can't silently rot
  (the reference uses `pytest --cov-fail-under=70`).
- **Integration test** — at least one test against the **real database**
  (Postgres), running your migrations and real queries. This is the layer most
  people fake with SQLite/mocks — and faking it means migrations, constraints,
  and dialect-specific SQL are never tested. Don't fake it.

The reference shows the pattern: unit tests use an in-memory override for speed
(`backend/tests/test_*.py`), and a separate **`backend/tests/integration/`** test
marked `@pytest.mark.integration` runs against a real Postgres
(`docker compose up -d db`, then `pytest -m integration`). Copy that split.

## Step 5 — Frontend (golden-path stack)

If you're doing a UI, build it now (React/TypeScript in the reference: light
theme, a navbar, a dashboard landing page, plus the auth/catalog/cart/checkout
screens). Backend-only capstones can skip this and exercise the API via `curl`
and k6 in Module 05. Frontend build/lint must be clean for Module 03's CI.

> ### 🤖 Claude Code track
> Useful prompts, run from `../shopkit`:
> - *"Using examples/minimal-service as the reference shape, scaffold a FastAPI
>   app with /health and /ready (traced), OTel wiring from
>   assets/otel-wiring, and a pytest for /health."*
> - *"Add SQLAlchemy 2.0 models + an Alembic baseline migration for `<your
>   entities>`, plus a Postgres service in docker-compose.yml."*
> - Feature by feature: *"Implement `<endpoint>` with a test."*
> - Then verify with the kit's own command: `/check-python` (and
>   `/check-frontend` if you built a UI) before moving on.

> ### 🛠️ Manual track
> - Copy `examples/minimal-service/{telemetry.py,Dockerfile}` patterns (or
>   `../assets/otel-wiring/`) into your backend; adapt the import paths.
> - Stand up models + an Alembic env yourself; use `../assets/seed/` for data.
> - Diff your endpoints against `../reference-solution/backend/` when unsure of
>   structure.
> - Re-run `python3 tools/doctor.py .` after every change.

> ### Different stack?
> doctor.py recognizes Node/Go/Java/.NET manifests too. For health-check + OTel
> patterns in other languages see `<kit>/docs/TECH-STACK-SWAP-GUIDE.md`
> ("health endpoints" and "observability" rows) and
> `<kit>/dotnet/ServiceDefaults/Extensions.cs`. If you use a non-Postgres DB,
> doctor will WARN and you'll adjust `ci.yml`'s service container in Module 03
> (TECH-STACK-SWAP-GUIDE.md "database" row).

## ✅ Checkpoint

- [ ] `python3 tools/doctor.py .` reports **0 FAIL** (WARNs on OTel/catalog are OK).
- [ ] `docker compose up -d` boots; `curl -sf localhost:8000/health` and
      `/ready` both return 200.
- [ ] **Unit tests pass with a coverage gate** (RUBRIC 4a) — e.g. `pytest --cov-fail-under=70`.
- [ ] **At least one integration test passes against real Postgres** (RUBRIC 4b) —
      e.g. `pytest -m integration` with a Postgres container up. Not SQLite/mocks.
- [ ] At least the core feature set for your domain works end-to-end locally.

Next: **[Module 03 — Shift-left security & CI](03-shiftleft-ci.md)**.
