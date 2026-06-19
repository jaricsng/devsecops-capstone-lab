# Module 07 — IaC, governance & migration safety

> **Goal:** describe your infrastructure as code, gate it with policy-as-code,
> and prove your database changes are safe to deploy without downtime.
> Exercises: `iac-terraform/gcp-cloud-run/*`, `governance/policy-as-code/*`,
> `tools/check_migrations.py`.

Clicking in a cloud console doesn't scale and isn't reviewable. This module
turns your deploy target into reviewable Terraform, adds an automated guardrail
that rejects bad infra, and wires the gate that stops a careless migration from
breaking a rolling deploy. **You never need a real cloud account** — `validate`
and `plan` work offline, and the policy/migration gates run on local files.

## Part A — Infrastructure as Code

### Step 1 — Fill in the Terraform variables

```bash
cd iac-terraform/gcp-cloud-run
cp terraform.tfvars.example terraform.tfvars   # if not already present
```

Set `project_id` (any placeholder string is fine for `plan`/`validate`),
confirm `app_name`, and leave `image_tag` as a placeholder. Read `variables.tf`
to see what's parameterized (region, environment, scale-to-zero vs always-on, DB
tier).

### Step 2 — Validate and plan

```bash
terraform init -backend=false
terraform validate
terraform fmt -check -recursive
terraform plan   # runs offline against your tfvars; no apply
```

A clean `validate` + a `plan` that renders without error is the bar. Do **not**
`apply` — deployment to a live Cloud Run is out of scope (and the `publish.yml`
deploy jobs stay `if: false`).

## Part B — Policy as code

### Step 3 — Run Conftest against the fixtures

The kit ships example Rego guardrails plus passing/failing plan fixtures so you
can see the gate work without your own plan:

```bash
cd <kit>/governance/policy-as-code
conftest test --policy policy examples/passing-plan.json   # exit 0 (maybe 1 warning)
conftest test --policy policy examples/failing-plan.json   # exit 1, 2 failures
```

### Step 4 — Run it against your plan

```bash
cd <your repo>/iac-terraform/gcp-cloud-run
terraform plan -out plan.binary && terraform show -json plan.binary > plan.json
conftest test --policy ../../governance/policy-as-code/policy plan.json
```

Read `terraform_guardrails.rego` and adapt at least one rule to your module (or
write one) — e.g. "no public ingress in production", "deletion protection on the
DB". Documenting your guardrail is part of the rubric.

## Part C — Migration safety

### Step 5 — Watch the gate block a dangerous change

The kit's `check_migrations.py` blocks backward-incompatible DDL that would break
a rolling deploy (old pods still running while the new schema lands).

```bash
# the unsafe example shipped with this lab:
python3 <kit>/tools/check_migrations.py ../assets/alembic-expand-contract/unsafe.sql   # exit 1
# the safe expand/contract version:
python3 <kit>/tools/check_migrations.py ../assets/alembic-expand-contract/safe.sql     # exit 0
```

### Step 6 — Apply expand/contract to your own schema

Pick a destructive change you'd realistically make (rename a column, drop one)
and implement it the safe way per `<kit>/docs/DATABASE-MIGRATIONS.md`: **expand**
(add the new shape, write both), deploy, backfill, then **contract** (remove the
old) in a later release. Run `make migrations` (= `check_migrations.py`) and
confirm it passes. If you have a genuinely unavoidable destructive step, use the
documented `migration-safety: ack <reason>` acknowledgment — deliberately, not
reflexively.

> ### 🤖 Claude Code track
> - `/check-gcp` (or `/check-aws`, `/check-azure`) — review your IaC/deploy
>   config against cloud best practices.
> - `/check-db` — SQLAlchemy/Alembic conventions + index coverage.
> - *"Rewrite this migration as expand/contract per docs/DATABASE-MIGRATIONS.md
>   so check_migrations.py passes."*

> ### 🛠️ Manual track
> - Edit `terraform.tfvars` and the Rego by hand; diff against
>   `../reference-solution/iac-terraform/` and `.../governance/`.
> - Hand-write the expand/contract migration following the kit doc; iterate
>   until `check_migrations.py` exits 0.

> ### Different stack?
> The kit only ships **GCP** Terraform. For AWS/Azure you'll write your own IaC
> (or use the deploy jobs without Terraform) — see
> `<kit>/docs/TECH-STACK-SWAP-GUIDE.md` "IaC" row. `check_migrations.py`
> understands raw SQL and Alembic; for other migration tools (Prisma, Flyway,
> Rails), it scans their default dirs — confirm yours is covered or pass the
> path explicitly.

## ✅ Checkpoint

- [ ] `terraform validate` passes and `terraform plan` renders without error.
- [ ] `conftest test` exits **0** on the passing fixture, **1** on the failing one.
- [ ] You adapted/added at least one Rego guardrail.
- [ ] `check_migrations.py` blocks `unsafe.sql` (exit 1) and you implemented an
      expand/contract change on your own schema that passes.

Next: **[Module 08 — Day-2 ops & safe delivery](08-day2-ops.md)**.
