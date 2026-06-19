# Module 01 — Scaffold your repo

> **Goal:** generate a new repo for *your* app from the kit, then read what it
> gave you and what it left for you. Exercises: `tools/scaffold.py`,
> `tools/doctor.py`, the generated `TODO.md` / `PLATFORM-KIT.md`.

The kit is a template, not a framework — you don't `import` it, you *copy from*
it. `scaffold.py` does that copy and resolves the app-name placeholders so you
start from a working skeleton instead of a pile of `your-app` strings.

## Step 1 — Run the scaffolder

Pick a kebab-case app name. Output to a sibling directory — **this becomes your
own repo**, separate from both the kit and this lab.

```bash
python3 <kit>/tools/scaffold.py \
  --app-name shopkit \
  --output ../shopkit \
  --cloud gcp
```

Flags worth knowing (`--help` for all):

| Flag | Effect |
|------|--------|
| `--cloud {none,azure,aws,gcp}` | which IaC + deploy target to include (gcp adds the Terraform module + governance) |
| `--no-observability` / `--no-security` / `--no-load-testing` | drop a capability if your capstone scope excludes it (not recommended here — the rubric needs them) |
| `--no-claude-commands` | skip `.claude/commands/` (manual-track learners can still keep them as docs) |
| `--no-governance` | skip policy-as-code (only relevant with `--cloud gcp`) |
| `--force` | scaffold into a non-empty directory |

> Keep observability, security, and load-testing **on** — every one is a
> required rubric item. Choose `--cloud gcp` to match the reference (the
> Terraform + governance modules assume it). Other clouds: see *Different stack*
> below.

## Step 2 — Look at what you got

```bash
cd ../shopkit
git status          # scaffold ran `git init` for you
cat PLATFORM-KIT.md # records the kit commit SHA you scaffolded from — keep this
cat README.md       # auto-generated, lists the capabilities you enabled
make help           # the paved task interface (doctor/obs-up/sync are real now)
```

What landed (high level): `.github/workflows/` (ci, publish, drift-detection),
`.pre-commit-config.yaml`, `Makefile`, `.devcontainer/`, `.tool-versions`,
`.env.example`, `.gitignore`, `.secrets.baseline`, `observability/`,
`security/`, `load-testing/`, `iac-terraform/gcp-cloud-run/`,
`governance/policy-as-code/`, `operations/`, `tools/`, and (unless skipped)
`.claude/commands/`. **No application code** — that's your job, starting next
module.

## Step 3 — Run the readiness check (and expect it to fail)

```bash
python3 tools/doctor.py .
# or: make doctor
```

On a bare scaffold you should see **3 FAIL**, and that's correct:

- ❌ **Containerized** — no Dockerfile yet
- ❌ **Health/readiness endpoints** — no `/health` or `/ready` yet
- ❌ **Automated tests present** — no test files yet

Plus PASS on secrets hygiene / gitignore + secrets-baseline, and WARNs on OTel
and catalog ownership. `doctor.py` is your north star for Module 02 — your job
is to turn those FAILs green.

## Step 4 — Read your TODO list

```bash
cat TODO.md
```

These are the placeholders `scaffold.py` *couldn't* resolve because they need a
real decision or credential (CI working-directories, GCP project ID, CODEOWNERS
team, OWASP endpoint list, …). You'll knock these off across Modules 02–09 —
don't try to fill them all now.

> ### 🤖 Claude Code track
> From inside `../shopkit`: *"Read PLATFORM-KIT.md, README.md, and TODO.md.
> Summarize what this scaffold gave me, and order the TODO.md items by which
> module of the capstone resolves each."*

> ### 🛠️ Manual track
> Read `TODO.md` top to bottom and jot the module number next to each row using
> the table in [RUBRIC.md](../RUBRIC.md). Nothing to install yet.

> ### Different stack?
> For AWS/Azure use `--cloud aws|azure` (you'll get deploy jobs but no Terraform
> module — the kit only ships GCP Terraform; see
> `<kit>/docs/TECH-STACK-SWAP-GUIDE.md` "IaC" row). For `--cloud none` you skip
> IaC entirely and Module 07 becomes governance + migrations only.

## ✅ Checkpoint

- [ ] `../shopkit` (or your app's repo) exists and is a git repo.
- [ ] `cat PLATFORM-KIT.md` shows a kit commit SHA.
- [ ] `python3 tools/doctor.py .` reports the **3 expected FAILs** and the
      gitignore/secrets-baseline check **PASSES**.
- [ ] You've mapped each `TODO.md` row to a module.

Next: **[Module 02 — Build the app → doctor-green](02-build-app.md)**.
