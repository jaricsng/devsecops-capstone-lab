# Prerequisites

Install these before Module 00. The lab is designed to run **entirely on your
laptop** — no cloud account or paid services are required to pass.

## Required for everyone

| Tool | Why | Check |
|------|-----|-------|
| **Git** | clone the kit, version your work | `git --version` |
| **Docker** + Compose v2 | the kit containerizes everything; observability runs as a Compose overlay | `docker compose version` |
| **Python 3.12** | the kit's tooling (`scaffold.py`, `doctor.py`, …) and the reference backend | `python3 --version` |
| **A clone of the kit** | the lab drives the kit's tools | `git clone https://github.com/jaricsng/platform-starter-kit` |

## Required for the golden-path stack (skip if you swap)

| Tool | Why | Check |
|------|-----|-------|
| **Node 20+** | the reference React/TypeScript frontend | `node --version` |
| **Terraform 1.5+** | Module 07 IaC (`terraform validate` / `plan`) | `terraform version` |
| **conftest** (OPA) | Module 07 policy-as-code gate | `conftest --version` |
| **k6** | Module 05 load testing (Locust is a Python alternative — `pip install locust`) | `k6 version` |
| **pre-commit** | Module 03 shift-left hooks | `pre-commit --version` |
| **detect-secrets** | secrets baseline used by pre-commit | `detect-secrets --version` |

> The kit ships a `.tool-versions` (asdf/mise) and a `.devcontainer/` that pin
> all of the above. If you use [mise](https://mise.jdx.dev/) or
> [asdf](https://asdf-vm.com/), `mise install` / `asdf install` in your
> scaffolded repo gets you the matched toolchain. Teams: see
> [Module 09](modules/09-team-track.md).

## For the Stripe checkout (Module 02 + the webhook exercise)

The reference checkout uses **Stripe's sandbox/test mode** — free, no real
money, no business verification.

1. Create a free account at <https://dashboard.stripe.com/register>.
2. Toggle **Test mode** (top-right).
3. Copy your **test** keys from *Developers → API keys*:
   - Publishable key `pk_test_...` → frontend
   - Secret key `sk_test_...` → backend (`.env`, never committed)
4. For the webhook exercise, install the [Stripe CLI](https://stripe.com/docs/stripe-cli)
   to forward events locally: `stripe listen --forward-to localhost:8000/webhooks/stripe`.

> Test card: `4242 4242 4242 4242`, any future expiry, any CVC.

## Optional — the Claude Code track

If you want to follow the 🤖 track, install **[Claude Code](https://claude.com/claude-code)**.
The 🛠️ manual track requires none of this and reaches the same checkpoints.

## Sanity check

```bash
docker compose version && python3 --version && git --version
# golden path also:
node --version && terraform version && k6 version && pre-commit --version
```

If all print versions, head to [Module 00](modules/00-orientation.md).
