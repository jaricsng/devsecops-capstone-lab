# Seed data

A browsable catalog and a meaningful load test both need data. This folder
provides sample product rows so [Module 02](../../modules/02-build-app.md)'s
catalog endpoints return something and [Module 05](../../modules/05-load-testing.md)'s
search has rows to hit.

> **Data file:** `products.json` (a few dozen sample products across categories)
> is added in the lab's asset phase. For now, generate your own domain's seed
> data — the *shape* matters more than the contents.

## How to use it

- Load it via a one-shot seed script (`python -m app.seed`) or an Alembic data
  migration, run after your schema migration.
- Keep seed data **out of production** paths — it's for local/dev/test only.
- For load testing, seed enough rows that search/pagination is realistic
  (hundreds, not three).

Adapt the fields to your domain: the reference uses
`{id, name, description, price_cents, category, image_url, stock}`.
