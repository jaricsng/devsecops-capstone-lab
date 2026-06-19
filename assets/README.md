# Lab assets

Pre-written, tricky-bit templates so **manual-track** learners (no Claude Code)
don't get stuck on plumbing. Each folder is referenced from a specific module.
Adapt them to your domain — they're starting points, not drop-in libraries.

| Folder | Used by | What it gives you |
|--------|---------|-------------------|
| [`otel-wiring/`](otel-wiring/) | Module 02, 04 | OpenTelemetry SDK setup (traces + metrics) mirroring the kit's `examples/minimal-service/telemetry.py` |
| [`seed/`](seed/) | Module 02, 05 | Sample catalog seed data so browse/search/load-test have something to hit |
| [`alembic-expand-contract/`](alembic-expand-contract/) | Module 07 | A deliberately **unsafe** migration and its **safe** expand/contract rewrite (runnable against `check_migrations.py`) |
| [`stripe-webhook/`](stripe-webhook/) | Module 06 (exercise) | A signature-verifying, idempotent Stripe webhook handler |
| [`feature-flag/`](feature-flag/) | Module 08 | An OpenFeature-gated decision point (the reference gates checkout) |
