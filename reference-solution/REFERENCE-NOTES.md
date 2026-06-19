# Reference Solution — ShopKit

A complete worked example of the capstone: a small e-commerce app built on the
kit's golden path, used as an **answer key**. Build *your own* app — consult
this when you're stuck, don't clone it.

> **Status:** populated. The backend is doctor-green with a passing test suite;
> the frontend lints, type-checks, tests, and builds clean. The modules never
> *require* a finished reference to reach their checkpoints — this is here as an
> answer key to diff against.

## Stack

- **Backend:** FastAPI + SQLAlchemy 2.0 + Alembic, Postgres, OpenTelemetry,
  pytest. `/health`, `/ready`, `/metrics`, plus auth / profile / catalog / cart
  / checkout (Stripe **test mode**).
- **Frontend:** React + TypeScript (Vite), light theme, navbar, dashboard, and
  the auth / catalog-search / cart / checkout screens. ESLint + tsc clean.
- **Infra:** scaffolded from the kit with `--cloud gcp` (Terraform Cloud Run
  module, governance policies, observability overlay, CI, pre-commit).

## What's built vs left as a guided exercise

| Feature | In the reference | Where |
|---------|------------------|-------|
| Registration / login / logout (JWT) | ✅ built | `backend/` |
| User profile CRUD | ✅ built | `backend/` |
| Catalog browse + search | ✅ built | `backend/`, `frontend/` |
| Cart | ✅ built | `backend/`, `frontend/` |
| Stripe-sandbox checkout (PaymentIntent) | ✅ built | `backend/`, `frontend/` |
| Feature-flag-gated checkout | ✅ built (`FEATURE_CHECKOUT_ENABLED`) | `backend/app/routers/checkout.py` |
| Admin authz + product create | ✅ partial (`require_admin` + `POST /products`) | `backend/app/routers/products.py` |
| Admin product update/delete UI | 📝 guided exercise | RUBRIC "Stretch" |
| Stripe webhook (signature + idempotency) | 📝 guided exercise | `../assets/stripe-webhook/` |

## How it maps to the modules

It was produced by walking Modules 01 → 08 exactly as written, so each module's
Checkpoint is satisfied here. `CAPSTONE-REPORT.md` (when present) is the model
submission.

## ⚠️ Not production code

This is a teaching artifact. It uses test keys, permissive local CORS, and
intentionally simple choices to keep the focus on the DevSecOps wrapper, not
e-commerce edge cases.
