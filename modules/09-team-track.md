# Module 09 — Team track *(optional / additive)*

> **Goal:** make the repo safe for *more than one person* — shared infra state,
> serialized deploys, enforced review, and identical environments. Exercises:
> generated `.github/CODEOWNERS`, `publish.yml` concurrency, `backend.tf.example`,
> `.devcontainer/` + `.tool-versions`, `.gitattributes`.

**Solo learners:** read this so you know what changes with a team, then skip to
Module 10 — none of it is required to pass solo. **Teams:** all four items below
are required (RUBRIC T1–T4). Everything here is *additive* — it layers on the
repo you already built.

The moment a second person commits, new failure modes appear: two people editing
infra state, two merges deploying over each other, a change merged with no
review, "works on my laptop." The kit addresses each.

## T1 — Code ownership + required review

The scaffold generated `.github/CODEOWNERS` with placeholder handles. Resolve
them to real GitHub teams/users per area (e.g. `/iac-terraform/ @org/platform`).
Then turn on **branch protection** on `main`: require PRs, require the CI checks
from Module 03, and require CODEOWNERS review. Now no change reaches `main`
unreviewed or red.

```bash
# CODEOWNERS is just a file — branch protection is a repo setting:
# Settings → Branches → Add rule → require PR + status checks + code owner review
```

## T2 — No racing deploys

Open `.github/workflows/publish.yml` and confirm the `concurrency:` block:

```yaml
concurrency:
  group: publish-${{ github.ref }}
  cancel-in-progress: false
```

This queues deploys instead of letting two merges race the same environment.
`cancel-in-progress: false` matters for deploys (you don't want to abort a
half-finished one). Confirm `ci.yml` similarly serializes/cancels superseded
runs.

## T3 — Shared infrastructure state

A local `terraform.tfstate` on one laptop is a single point of failure and can't
be locked. For a team it's not optional. Configure the remote backend using
`iac-terraform/gcp-cloud-run/backend.tf.example` (a GCS backend) **before a
second person runs Terraform**: it locks state during `apply` (no concurrent
corruption) and makes state shared. Use a separate `prefix` per environment.

```bash
cd iac-terraform/gcp-cloud-run
cp backend.tf.example backend.tf      # then fill bucket + prefix
terraform init                        # migrates state to the remote backend
```

## T4 — Identical environments

Drift between laptops causes "works on mine" bugs. The scaffold shipped
`.devcontainer/devcontainer.json` and `.tool-versions` — commit them and have
every member either open the devcontainer or run `mise install` / `asdf install`
so everyone (and CI) uses the same toolchain. `.gitattributes` normalizes line
endings to LF so a Windows teammate doesn't churn every file (and break shell
scripts / the Makefile's tabs).

## Working agreement (recommended)

Write a short `CONTRIBUTING.md` for your team: branch naming, who reviews what
(mirrors CODEOWNERS), how you handle a failing migration gate, and the deploy
order. The kit's collaboration features enforce mechanics; a working agreement
covers the human parts.

> ### 🤖 Claude Code track
> - *"Read .github/CODEOWNERS and my repo layout; propose per-path ownership for
>   a team of `<roles>`."*
> - `/review-conventions` — check changes against agreed conventions before PR.

> ### 🛠️ Manual track
> - Edit CODEOWNERS + configure branch protection in the GitHub UI.
> - Fill `backend.tf` and run `terraform init` to migrate state; diff against
>   `../reference-solution/iac-terraform/gcp-cloud-run/backend.tf.example`.

> ### Different stack?
> Concurrency groups, CODEOWNERS, devcontainers, and `.gitattributes` are
> stack-agnostic. Remote-state backends are cloud-specific — AWS uses S3+DynamoDB
> locking, Azure uses a storage account; see `<kit>/docs/TECH-STACK-SWAP-GUIDE.md`
> "IaC" row.

## ✅ Checkpoint (teams)

- [ ] `.github/CODEOWNERS` resolved to real handles; branch protection requires
      PR + CI + code-owner review.
- [ ] `publish.yml` has a `concurrency:` group.
- [ ] Terraform uses a **remote backend with locking** (no local `tfstate`).
- [ ] `.devcontainer/` + `.tool-versions` committed; every member builds identically.

Next: **[Module 10 — Stay in sync & submit](10-sync-and-submit.md)**.
